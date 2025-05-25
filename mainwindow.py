# This Python file uses the following encoding: utf-8
import sys
import json
import re

from PySide6 import QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QDateTime
from qasync import QEventLoop, asyncSlot
import pyperclip
from aiogram.utils.token import TokenValidationError

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from uis.ui_form import Ui_MainWindow

from sender.social_media_poster import SocialMediaPoster
from hf_handler import HfHandler


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.poster = None
        self.files = None
        self.hf_inference = None
        self.configure(settings_path='settings/settings_test.json')

    def configure(self, settings_path):
        self.setupUi(self)
        app_icon = QIcon('icon256.png')
        self.setWindowIcon(app_icon)
        self.setAcceptDrops(True)

        # Moves window to the center of the screen
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.images_file_dialog.clicked.connect(self.open_file_dialog)
        self.send_button.clicked.connect(self.send_to_social_media)
        self.clear_all_button.clicked.connect(self.clear_all)
        self.remember_links_button.clicked.connect(self.view_results)
        self.about.triggered.connect(self.about_window)
        self.format_text_button.clicked.connect(self.format_text)

        self.delete_file_button.clicked.connect(self.remove_file)
        self.delete_file_button.setEnabled(False)

        self.file_listWidget.itemSelectionChanged.connect(self.update_file_buttons_state)
        self.file_order_up.setEnabled(False)
        self.file_order_up.clicked.connect(self.move_file_up)
        self.file_order_down.setEnabled(False)
        self.file_order_down.clicked.connect(self.move_file_down)

        self.delayed_time.setDateTime(QDateTime.currentDateTime())
        self.delayed_time.setEnabled(False)
        self.delayed_post_check.stateChanged.connect(self.delayed_date_state_changed)

        create_tg, create_vk, create_ok, create_hf = (False, False, False, False)
        with open(settings_path, encoding='utf_8_sig') as f:
            try:
                smp_settings = json.load(f)
            except json.decoder.JSONDecodeError:
                smp_settings = None

        if smp_settings:
            create_tg = 'telegram' in smp_settings and all((
                'bot_token' in smp_settings['telegram'] and smp_settings['telegram']['bot_token'],
                'chat_id' in smp_settings['telegram'],
                'group_name' in smp_settings['telegram']))

            create_vk = 'vk' in smp_settings and all((
                'token' in smp_settings['vk'],
                'group_id' in smp_settings['vk']))

            create_ok = 'ok' in smp_settings and all((
                'access_token' in smp_settings['ok'],
                'application_key' in smp_settings['ok'],
                'application_secret_key' in smp_settings['ok'],
                'group_id' in smp_settings['ok']))

            create_hf = 'hf' in smp_settings and all((
                'token' in smp_settings['hf'],
                'model' in smp_settings['hf'],
                'system_prompt' in smp_settings['hf']))

        try:
            self.poster = SocialMediaPoster(telegram=create_tg, vk=create_vk, ok=create_ok, settings=smp_settings)
        except TokenValidationError:
            create_tg = False
            self.poster = SocialMediaPoster(telegram=create_tg, vk=create_vk, ok=create_ok, settings=smp_settings)

        if not create_tg:
            self.telegram_checkbox.setEnabled(False)
            self.telegram_checkbox.setChecked(False)
            tg_font = self.telegram_checkbox.font()
            tg_font.setStrikeOut(True)
            self.telegram_checkbox.setFont(tg_font)
        if not create_vk:
            self.vk_checkbox.setEnabled(False)
            self.vk_checkbox.setChecked(False)
            vk_font = self.vk_checkbox.font()
            vk_font.setStrikeOut(True)
            self.vk_checkbox.setFont(vk_font)
        if not create_ok:
            self.ok_checkbox.setEnabled(False)
            self.ok_checkbox.setChecked(False)
            ok_font = self.ok_checkbox.font()
            ok_font.setStrikeOut(True)
            self.ok_checkbox.setFont(ok_font)
        if create_hf:
            self.hf_inference = HfHandler(smp_settings['hf'])
            self.add_emojis_button.clicked.connect(self.add_emojis_and_tags)
        else:
            hf_font = self.add_emojis_button.font()
            hf_font.setStrikeOut(True)
            self.add_emojis_button.setFont(hf_font)
            self.add_emojis_button.setEnabled(False)

        if not all((create_tg, create_vk, create_ok)):
            self.send_button.setEnabled(False)

        self.files = list()

    @asyncSlot()
    async def send_to_social_media(self) -> None:
        self.poster.title = self.article_title.text().strip()
        self.poster.text = self.article_text.toPlainText().strip()
        self.poster.files = self.files.copy()
        self.poster.delayed_post_date = self.get_timestamp() if self.delayed_post_check.isChecked() else None

        if self.poster.title == '' and self.poster.text == '' and self.poster.files == []:
            await self.error_window('Минимум одно поле должно быть заполнено!')
            return

        if self.delayed_post_check.isChecked() and QDateTime.currentDateTime() > self.delayed_time.dateTime():
            await self.error_window('Заданное время меньше чем настоящее!')
            return

        self.send_button.setEnabled(False)
        self.send_button.setText('Отправляю...')

        to_telegram = self.telegram_checkbox.isChecked() if not self.delayed_post_check.isChecked() else False
        to_vk = self.vk_checkbox.isChecked()
        to_ok = self.ok_checkbox.isChecked()

        await self.poster.send_article(telegram=to_telegram, vk=to_vk, ok=to_ok)
        await self.view_results(header='Результат отправки')

        # Preventive clean-up in poster object because of dupping media
        self.poster.clear_files()

        self.send_button.setEnabled(True)
        self.send_button.setText('Отправить')

    @asyncSlot()
    async def view_results(self, header=None) -> None:
        header = 'Спокуха, всё под контролем' if header is None else header
        results = self.get_results()

        result_dlg = QMessageBox(self)
        if any(results):
            result_dlg.setWindowTitle(header)
            result_dlg.setText('\n'.join(results))
        else:
            result_dlg.setWindowTitle(header + ' (наверное?)')
            result_dlg.setText('Ссылки, как истинные мудрецы, предпочитают оставаться в тени, '
                               'чтобы не подвергаться искажениям и неверным интерпретациям. (ง ͠ಥ_ಥ)ง')
        copy_button = result_dlg.addButton('Копировать результаты', QMessageBox.ActionRole)
        result_dlg.addButton('Закрыть', QMessageBox.RejectRole)
        copy_button.clicked.connect(self.copy_results)
        copy_button.setDefault(True)
        result_dlg.setIcon(QMessageBox.Information)
        result_dlg.exec()

    @asyncSlot()
    async def copy_results(self) -> None:
        if any(results := self.get_results()):
            result = '\n'.join(results)
            pyperclip.copy(result)
        else:
            await self.error_window('Нет данных для копирования')

    @asyncSlot()
    async def add_emojis_and_tags(self):
        self.add_emojis_button.setEnabled(False)
        self.add_emojis_button.setText('Думаю...')

        title = self.article_title.text()
        text = self.article_text.toPlainText()
        article = title + text if title else text
        try:
            if self.legacy_hf_method_checkbox.isChecked():
                out_article = self.hf_inference.add_emojis_and_tags(article)
            else:
                out_article = await self.hf_inference.add_emojis_and_tags_async(article)

            if title:
                out_title, out_text = out_article.split('\n\n', maxsplit=1)
                self.article_title.setText(out_title)
                self.article_text.setPlainText(out_text)
            else:
                self.article_text.setPlainText(out_article)
        except Exception as e:
            await self.error_window(f'Проблема соединения с Huggingface:\n{repr(e)}')

        self.add_emojis_button.setEnabled(True)
        self.add_emojis_button.setText('Обработать ИИ')

    def get_results(self) -> list:
        results = []
        if hasattr(self.poster, 'tg') and self.poster.tg.result:
            results.append(self.poster.tg.result)
        if hasattr(self.poster, 'vk') and self.poster.vk.result:
            results.append(self.poster.vk.result)
        if hasattr(self.poster, 'ok') and self.poster.ok.result:
            results.append(self.poster.ok.result)

        return results

    def open_file_dialog(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Медиа (*.png *.jpg *.jpeg *.mp4 *.avi *.3gp)")

        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            self.update_img_paths(filenames)

    def dragEnterEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            filenames = [url.toLocalFile() for url in event.mimeData().urls()]
            self.update_img_paths(filenames)
            event.accept()
        else:
            event.ignore()

    def update_img_paths(self, filenames: list) -> None:
        # For the uniqueness of uploaded files
        [self.files.append(i) for i in filenames if i not in self.files]
        self.files.sort()

        self.file_listWidget.clear()
        self.file_listWidget.addItems(self.files)

    def remove_file(self) -> None:
        selected_item = self.file_listWidget.currentItem()
        if selected_item:
            self.file_listWidget.takeItem(self.file_listWidget.row(selected_item))
            self.files.remove(selected_item.text())

    def update_file_buttons_state(self) -> None:
        is_selected_items = len(self.file_listWidget.selectedItems()) > 0
        self.delete_file_button.setEnabled(is_selected_items)
        self.file_order_up.setEnabled(is_selected_items)
        self.file_order_down.setEnabled(is_selected_items)

    def move_file_up(self) -> None:
        current_row = self.file_listWidget.currentRow()
        if current_row > 0:
            current_item = self.file_listWidget.takeItem(current_row)
            self.file_listWidget.insertItem(current_row - 1, current_item)
            self.file_listWidget.setCurrentRow(current_row - 1)
            self.files.insert(current_row - 1, self.files.pop(current_row))

    def move_file_down(self) -> None:
        current_row = self.file_listWidget.currentRow()
        if current_row < self.file_listWidget.count() - 1:
            current_item = self.file_listWidget.takeItem(current_row)
            self.file_listWidget.insertItem(current_row + 1, current_item)
            self.file_listWidget.setCurrentRow(current_row + 1)
            self.files.insert(current_row + 1, self.files.pop(current_row))

    def delayed_date_state_changed(self) -> None:
        if self.delayed_post_check.isChecked():
            self.delayed_time.setEnabled(True)
            self.telegram_checkbox.setEnabled(False)
        else:
            self.delayed_time.setEnabled(False)
            if hasattr(self.poster, 'tg'):
                self.telegram_checkbox.setEnabled(True)

    def get_timestamp(self) -> float:
        return self.delayed_time.dateTime().toPython().timestamp()

    @asyncSlot()
    async def about_window(self) -> None:
        about_dlg = QMessageBox(self)
        about_dlg.setWindowTitle('Об авторе')
        about_dlg.setText('Разработчик: Косицин Илья\n'
                          'Специально для газеты \"ПРИЗЫВ\"\n'
                          '2023 год')
        about_dlg.addButton('Мне очень интересно, правда', QMessageBox.RejectRole)
        about_dlg.setIcon(QMessageBox.Information)
        about_dlg.exec()

    @asyncSlot()
    async def error_window(self, text='Неизвестная ошибка'):
        about_dlg = QMessageBox(self)
        about_dlg.setWindowTitle('Ошибка')
        about_dlg.setText(text)
        about_dlg.addButton('Прости, программочка!!', QMessageBox.RejectRole)
        about_dlg.setIcon(QMessageBox.Critical)
        about_dlg.exec()

    def format_text(self) -> None:
        many_spaces_pattern = re.compile(r' {2,}|\t+')                  # 2 and more whitespaces or one and more tabs
        formatted_text = re.sub(many_spaces_pattern, ' ', self.article_text.toPlainText().strip())
        formatted_text = re.sub(r'^\s+', '', formatted_text, flags=re.MULTILINE)   # spaces after newline
        formatted_text = re.sub(r'\s+\n', '\n', formatted_text)                   # spaces before newline
        formatted_text = re.sub(r'\n+', '\n\n', formatted_text)  # newlines(1 or more) to double newlines
        self.article_text.setPlainText(formatted_text)
        self.article_title.setText(re.sub(many_spaces_pattern, ' ', self.article_title.text().strip()))

    def clear_all(self) -> None:
        self.article_text.setPlainText('')
        self.article_title.setText('')
        self.file_listWidget.clear()
        self.files.clear()
        self.poster.clear_files()

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)

    widget = MainWindow()
    widget.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()

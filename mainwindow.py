# This Python file uses the following encoding: utf-8
import sys
import json

from PySide6 import QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QDateTime
from qasync import QEventLoop, asyncSlot
import pyperclip

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from uis.ui_form import Ui_MainWindow

from social_media_poster import SocialMediaPoster


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
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

        with open('settings/settings.json') as f:
            smp_settings = json.load(f)
        self.poster = SocialMediaPoster(settings=smp_settings)
        self.files = list()

    @asyncSlot()
    async def send_to_social_media(self):
        self.poster.title = self.article_title.text().strip()
        self.poster.text = self.article_text.toPlainText().strip()
        self.poster.files = self.files
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
        self.poster.files.clear()
        self.poster.photos.clear()
        self.poster.videos.clear()

        self.send_button.setEnabled(True)
        self.send_button.setText('Отправить')

    @asyncSlot()
    async def view_results(self, header=None):
        header = 'Спокуха, всё под контролем' if header is None else header

        result_dlg = QMessageBox(self)
        if self.poster.tg.result or self.poster.vk.result or self.poster.ok.result:
            result_dlg.setWindowTitle(header)
            result_dlg.setText(f'{self.poster.tg.result}\n'
                               f'{self.poster.vk.result}\n'
                               f'{self.poster.ok.result}'
                               )
        else:
            result_dlg.setWindowTitle(header+' (наверное?)')
            result_dlg.setText('Ссылки, как истинные мудрецы, предпочитают оставаться в тени, '
                               'чтобы не подвергаться искажениям и неверным интерпретациям. (ง ͠ಥ_ಥ)ง')
        copy_button = result_dlg.addButton('Копировать результаты', QMessageBox.ActionRole)
        result_dlg.addButton('Закрыть', QMessageBox.RejectRole)
        copy_button.clicked.connect(self.copy_results)
        copy_button.setDefault(True)
        result_dlg.setIcon(QMessageBox.Information)
        result_dlg.exec()

    def copy_results(self):
        result = f'{self.poster.tg.result}\n{self.poster.vk.result}\n{self.poster.ok.result}'
        pyperclip.copy(result)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Медиа (*.png *.jpg *.jpeg *.mp4 *.avi *.3gp)")

        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            self.update_img_paths(filenames)

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            filenames = [url.toLocalFile() for url in event.mimeData().urls()]
            self.update_img_paths(filenames)

            event.accept()
        else:
            event.ignore()

    def update_img_paths(self, filenames):
        # For the uniqueness of uploaded files
        [self.files.append(i) for i in filenames if i not in self.files]
        self.files.sort()

        self.file_listWidget.clear()
        self.file_listWidget.addItems(self.files)

    def remove_file(self):
        selected_item = self.file_listWidget.currentItem()
        if selected_item:
            self.file_listWidget.takeItem(self.file_listWidget.row(selected_item))
            self.files.remove(selected_item.text())

    def update_file_buttons_state(self):
        is_selected_items = len(self.file_listWidget.selectedItems()) > 0
        self.delete_file_button.setEnabled(is_selected_items)
        self.file_order_up.setEnabled(is_selected_items)
        self.file_order_down.setEnabled(is_selected_items)

    def move_file_up(self):
        current_row = self.file_listWidget.currentRow()
        if current_row > 0:
            current_item = self.file_listWidget.takeItem(current_row)
            self.file_listWidget.insertItem(current_row - 1, current_item)
            self.file_listWidget.setCurrentRow(current_row - 1)
            self.files.insert(current_row - 1, self.files.pop(current_row))

    def move_file_down(self):
        current_row = self.file_listWidget.currentRow()
        if current_row < self.file_listWidget.count() - 1:
            current_item = self.file_listWidget.takeItem(current_row)
            self.file_listWidget.insertItem(current_row + 1, current_item)
            self.file_listWidget.setCurrentRow(current_row + 1)
            self.files.insert(current_row + 1, self.files.pop(current_row))

    def delayed_date_state_changed(self):
        if self.delayed_post_check.isChecked():
            self.delayed_time.setEnabled(True)
            self.telegram_checkbox.setEnabled(False)
        else:
            self.delayed_time.setEnabled(False)
            self.telegram_checkbox.setEnabled(True)

    def get_timestamp(self):
        return self.delayed_time.dateTime().toPython().timestamp()

    @asyncSlot()
    async def about_window(self):
        about_dlg = QMessageBox(self)
        about_dlg.setWindowTitle('Об авторе')
        about_dlg.setText('Разработчик: Косицин Илья\n' +
                          'Специально для газеты \"ПРИЗЫВ\"\n' +
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

    def clear_all(self):
        self.article_text.setPlainText('')
        self.article_title.setText('')
        self.file_listWidget.clear()
        self.files.clear()
        self.poster.photos.clear()
        self.poster.videos.clear()


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)

    widget = MainWindow()
    widget.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()

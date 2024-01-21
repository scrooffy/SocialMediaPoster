# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
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

        self.poster = SocialMediaPoster()
        # For the uniqueness of uploaded files
        self.files_set = set()

    @asyncSlot()
    async def send_to_social_media(self):
        self.send_button.setEnabled(False)
        self.send_button.setText('Отправляю...')

        self.poster.title = self.article_title.text().strip()
        self.poster.text = self.article_text.toPlainText().strip()
        self.poster.files = list(self.files_set)

        to_telegram = self.telegram_checkbox.isChecked()
        to_vk = self.vk_checkbox.isChecked()
        to_ok = self.ok_checkbox.isChecked()

        await self.poster.send_article(telegram=to_telegram, vk=to_vk, ok=to_ok)
        await self.view_results(header='Результат отправки')

        self.send_button.setEnabled(True)
        self.send_button.setText('Отправить')

    @asyncSlot()
    async def view_results(self, header=None):
        header = 'Спокуха, всё под контролем' if header is None else header

        result_dlg = QMessageBox(self)
        result_dlg.setWindowTitle(header)
        result_dlg.setText(f'{self.poster.tg.result}\n'
                           f'{self.poster.vk.result}\n'
                           f'{self.poster.ok.result}'
                           )
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
        [self.files_set.add(i) for i in filenames]
        self.img_paths.setPlainText('\n'.join(self.files_set))

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

    def clear_all(self):
        self.article_text.setPlainText('')
        self.article_title.setText('')
        self.img_paths.setPlainText('Или перетащите сюда')
        self.files_set.clear()
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

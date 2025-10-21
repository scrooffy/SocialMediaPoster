from qasync import asyncSlot
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIcon
from uis.repost_w import Ui_Form


class RepostWindow(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(RepostWindow, self).__init__(parent)
        self.setupUi(self)
        app_icon = QIcon('icon256.png')
        self.setWindowIcon(app_icon)
        self.main_window = parent

        # When the button is clicked, this code passes False to header value instead of None
        # self.remember_links_btn.clicked.connect(self.view_results)
        self.remember_links_btn.clicked.connect(lambda: self.view_results())
        self.make_repost_btn.clicked.connect(self.make_repost)

    @asyncSlot()
    async def make_repost(self) -> None:
        vk_link = self.vk_link_line.text().strip()
        ok_link = self.ok_link_line.text().strip()

        if vk_link == '' and ok_link == '':
            await self.main_window.error_window('Минимум одно поле должно быть заполнено!')
            return

        invalid_links = []
        if vk_link and not vk_link.startswith('https://vk.'):
            invalid_links.append('VK')
        if ok_link and not ok_link.startswith('https://ok.ru/'):
            invalid_links.append('OK.ru')
        if invalid_links:
            self.error_window(f'Некорректная ссылка: {", ".join(invalid_links)}!')
            return

        self.make_repost_btn.setEnabled(False)
        self.make_repost_btn.setText('Делаю репосты...')

        await self.main_window.poster.do_repost(vk_link=vk_link, ok_link=ok_link)
        self.view_results(header='Результат репоста')

        self.make_repost_btn.setEnabled(True)
        self.make_repost_btn.setText('Сделать репосты')

    def view_results(self, header=None):
        self.main_window.view_results(header=header, parent=self)

    def error_window(self, text='Неизвестная ошибка'):
        self.main_window.error_window(text=text, parent=self)

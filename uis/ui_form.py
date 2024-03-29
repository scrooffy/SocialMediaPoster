# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(540, 648)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(540, 648))
        MainWindow.setMaximumSize(QSize(540, 648))
        self.about = QAction(MainWindow)
        self.about.setObjectName(u"about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setMaximumSize(QSize(800, 16777215))
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 550, 521, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 511, 521))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.send_to_label = QLabel(self.layoutWidget)
        self.send_to_label.setObjectName(u"send_to_label")

        self.gridLayout.addWidget(self.send_to_label, 3, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer_2, 9, 1, 1, 1)

        self.file_listWidget = QListWidget(self.layoutWidget)
        self.file_listWidget.setObjectName(u"file_listWidget")
        self.file_listWidget.setMaximumSize(QSize(16777215, 80))

        self.gridLayout.addWidget(self.file_listWidget, 7, 2, 3, 2)

        self.send_to_layout = QVBoxLayout()
        self.send_to_layout.setObjectName(u"send_to_layout")
        self.telegram_checkbox = QCheckBox(self.layoutWidget)
        self.telegram_checkbox.setObjectName(u"telegram_checkbox")
        self.telegram_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.telegram_checkbox)

        self.vk_checkbox = QCheckBox(self.layoutWidget)
        self.vk_checkbox.setObjectName(u"vk_checkbox")
        self.vk_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.vk_checkbox)

        self.ok_checkbox = QCheckBox(self.layoutWidget)
        self.ok_checkbox.setObjectName(u"ok_checkbox")
        self.ok_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.ok_checkbox)


        self.gridLayout.addLayout(self.send_to_layout, 4, 1, 1, 1)

        self.article_title = QLineEdit(self.layoutWidget)
        self.article_title.setObjectName(u"article_title")
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(10)
        font.setBold(True)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.article_title.setFont(font)
        self.article_title.setAcceptDrops(False)

        self.gridLayout.addWidget(self.article_title, 0, 2, 1, 2)

        self.article_title_label = QLabel(self.layoutWidget)
        self.article_title_label.setObjectName(u"article_title_label")

        self.gridLayout.addWidget(self.article_title_label, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.images_file_dialog = QPushButton(self.layoutWidget)
        self.images_file_dialog.setObjectName(u"images_file_dialog")

        self.gridLayout.addWidget(self.images_file_dialog, 7, 1, 1, 1)

        self.article_text = QPlainTextEdit(self.layoutWidget)
        self.article_text.setObjectName(u"article_text")
        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(10)
        self.article_text.setFont(font1)
        self.article_text.setAcceptDrops(False)

        self.gridLayout.addWidget(self.article_text, 1, 2, 6, 2)

        self.article_text_label = QLabel(self.layoutWidget)
        self.article_text_label.setObjectName(u"article_text_label")
        self.article_text_label.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.article_text_label, 1, 1, 1, 1)

        self.delete_file_button = QPushButton(self.layoutWidget)
        self.delete_file_button.setObjectName(u"delete_file_button")
        self.delete_file_button.setCheckable(False)
        self.delete_file_button.setFlat(False)

        self.gridLayout.addWidget(self.delete_file_button, 8, 1, 1, 1)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 570, 501, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.clear_all_button = QPushButton(self.layoutWidget1)
        self.clear_all_button.setObjectName(u"clear_all_button")

        self.horizontalLayout.addWidget(self.clear_all_button)

        self.remember_links_button = QPushButton(self.layoutWidget1)
        self.remember_links_button.setObjectName(u"remember_links_button")

        self.horizontalLayout.addWidget(self.remember_links_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.send_button = QPushButton(self.layoutWidget1)
        self.send_button.setObjectName(u"send_button")

        self.horizontalLayout.addWidget(self.send_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 540, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.about)

        self.retranslateUi(MainWindow)

        self.delete_file_button.setDefault(False)
        self.send_button.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Social Media Poster", None))
        self.about.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431 \u0430\u0432\u0442\u043e\u0440\u0435", None))
        self.send_to_label.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0432:", None))
        self.telegram_checkbox.setText(QCoreApplication.translate("MainWindow", u"Telegram", None))
        self.vk_checkbox.setText(QCoreApplication.translate("MainWindow", u"VK", None))
        self.ok_checkbox.setText(QCoreApplication.translate("MainWindow", u"OK.ru", None))
        self.article_title_label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0441\u0442\u0430\u0442\u044c\u0438:", None))
        self.images_file_dialog.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043c\u0435\u0434\u0438\u0430\u0444\u0430\u0439\u043b", None))
        self.article_text_label.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0441\u0442 \u0441\u0442\u0430\u0442\u044c\u0438:", None))
        self.delete_file_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.clear_all_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.remember_links_button.setText(QCoreApplication.translate("MainWindow", u" \u0410\u0410\u0410\u0410\u0410\u0410 \u042f \u0417\u0410\u0411\u042b\u041b \u0421\u0421\u042b\u041b\u041a\u0418\u0418!!!!!11!", None))
        self.send_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi


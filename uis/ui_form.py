# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QAction, QFont)
from PySide6.QtWidgets import (QCheckBox, QDateTimeEdit, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListWidget,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(540, 648)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(540, 648))
        MainWindow.setMaximumSize(QSize(1024, 1024))
        self.about = QAction(MainWindow)
        self.about.setObjectName(u"about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 1, 1, 1)

        self.send_to_label = QLabel(self.centralwidget)
        self.send_to_label.setObjectName(u"send_to_label")

        self.gridLayout.addWidget(self.send_to_label, 9, 1, 1, 1)

        self.format_text_button = QPushButton(self.centralwidget)
        self.format_text_button.setObjectName(u"format_text_button")

        self.gridLayout.addWidget(self.format_text_button, 2, 1, 1, 1)

        self.article_text_label = QLabel(self.centralwidget)
        self.article_text_label.setObjectName(u"article_text_label")
        self.article_text_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout.addWidget(self.article_text_label, 1, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.delete_file_button = QPushButton(self.centralwidget)
        self.delete_file_button.setObjectName(u"delete_file_button")
        self.delete_file_button.setMaximumSize(QSize(16777215, 16777215))
        self.delete_file_button.setCheckable(False)
        self.delete_file_button.setFlat(False)

        self.gridLayout_4.addWidget(self.delete_file_button, 2, 2, 1, 1)

        self.images_file_dialog = QPushButton(self.centralwidget)
        self.images_file_dialog.setObjectName(u"images_file_dialog")
        self.images_file_dialog.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_4.addWidget(self.images_file_dialog, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 3, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_4, 17, 1, 3, 1)

        self.article_title_label = QLabel(self.centralwidget)
        self.article_title_label.setObjectName(u"article_title_label")

        self.gridLayout.addWidget(self.article_title_label, 0, 1, 1, 1)

        self.file_listWidget = QListWidget(self.centralwidget)
        self.file_listWidget.setObjectName(u"file_listWidget")
        self.file_listWidget.setMaximumSize(QSize(16777215, 80))

        self.gridLayout.addWidget(self.file_listWidget, 17, 2, 1, 1)

        self.delayed_time = QDateTimeEdit(self.centralwidget)
        self.delayed_time.setObjectName(u"delayed_time")

        self.gridLayout.addWidget(self.delayed_time, 8, 1, 1, 1)

        self.legacy_hf_method_checkbox = QCheckBox(self.centralwidget)
        self.legacy_hf_method_checkbox.setObjectName(u"legacy_hf_method_checkbox")

        self.gridLayout.addWidget(self.legacy_hf_method_checkbox, 4, 1, 1, 1)

        self.delayed_post_check = QCheckBox(self.centralwidget)
        self.delayed_post_check.setObjectName(u"delayed_post_check")

        self.gridLayout.addWidget(self.delayed_post_check, 7, 1, 1, 1)

        self.send_to_layout = QVBoxLayout()
        self.send_to_layout.setObjectName(u"send_to_layout")
        self.telegram_checkbox = QCheckBox(self.centralwidget)
        self.telegram_checkbox.setObjectName(u"telegram_checkbox")
        self.telegram_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.telegram_checkbox)

        self.vk_checkbox = QCheckBox(self.centralwidget)
        self.vk_checkbox.setObjectName(u"vk_checkbox")
        self.vk_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.vk_checkbox)

        self.ok_checkbox = QCheckBox(self.centralwidget)
        self.ok_checkbox.setObjectName(u"ok_checkbox")
        self.ok_checkbox.setChecked(True)

        self.send_to_layout.addWidget(self.ok_checkbox)


        self.gridLayout.addLayout(self.send_to_layout, 10, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.file_order_up = QPushButton(self.centralwidget)
        self.file_order_up.setObjectName(u"file_order_up")
        self.file_order_up.setMaximumSize(QSize(20, 40))
        font = QFont()
        font.setPointSize(16)
        self.file_order_up.setFont(font)

        self.verticalLayout.addWidget(self.file_order_up)

        self.file_order_down = QPushButton(self.centralwidget)
        self.file_order_down.setObjectName(u"file_order_down")
        self.file_order_down.setMaximumSize(QSize(20, 40))
        self.file_order_down.setFont(font)

        self.verticalLayout.addWidget(self.file_order_down)


        self.gridLayout.addLayout(self.verticalLayout, 17, 4, 1, 1)

        self.add_emojis_button = QPushButton(self.centralwidget)
        self.add_emojis_button.setObjectName(u"add_emojis_button")

        self.gridLayout.addWidget(self.add_emojis_button, 3, 1, 1, 1)

        self.article_text = QPlainTextEdit(self.centralwidget)
        self.article_text.setObjectName(u"article_text")
        self.article_text.setAcceptDrops(False)

        self.gridLayout.addWidget(self.article_text, 1, 2, 12, 3)

        self.article_title = QLineEdit(self.centralwidget)
        self.article_title.setObjectName(u"article_title")
        font1 = QFont()
        font1.setBold(True)
        self.article_title.setFont(font1)
        self.article_title.setAcceptDrops(False)

        self.gridLayout.addWidget(self.article_title, 0, 2, 1, 3)

        self.make_repost_button = QPushButton(self.centralwidget)
        self.make_repost_button.setObjectName(u"make_repost_button")

        self.gridLayout.addWidget(self.make_repost_button, 5, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clear_all_button = QPushButton(self.centralwidget)
        self.clear_all_button.setObjectName(u"clear_all_button")
        self.clear_all_button.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.clear_all_button)

        self.remember_links_button = QPushButton(self.centralwidget)
        self.remember_links_button.setObjectName(u"remember_links_button")
        self.remember_links_button.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.remember_links_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.send_button = QPushButton(self.centralwidget)
        self.send_button.setObjectName(u"send_button")
        self.send_button.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.send_button)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

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
        self.format_text_button.setText(QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0440\u043c\u0430\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0442\u0435\u043a\u0441\u0442", None))
        self.article_text_label.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043a\u0441\u0442 \u0441\u0442\u0430\u0442\u044c\u0438:", None))
        self.delete_file_button.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.images_file_dialog.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0444\u0430\u0439\u043b(\u044b)", None))
        self.article_title_label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0441\u0442\u0430\u0442\u044c\u0438:", None))
#if QT_CONFIG(tooltip)
        self.legacy_hf_method_checkbox.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0437\u0430\u043f\u0440\u043e\u0441\u0430 \u0432 Huggingface \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u043d\u044b\u043c \u043c\u0435\u0442\u043e\u0434\u043e\u043c (\u0435\u0441\u043b\u0438 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u043c\u0435\u0442\u043e\u0434)", None))
#endif // QT_CONFIG(tooltip)
        self.legacy_hf_method_checkbox.setText(QCoreApplication.translate("MainWindow", u"Legacy \u043c\u0435\u0442\u043e\u0434", None))
        self.delayed_post_check.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043d\u044b\u0439 \u043f\u043e\u0441\u0442", None))
        self.telegram_checkbox.setText(QCoreApplication.translate("MainWindow", u"Telegram", None))
        self.vk_checkbox.setText(QCoreApplication.translate("MainWindow", u"VK", None))
        self.ok_checkbox.setText(QCoreApplication.translate("MainWindow", u"OK.ru", None))
        self.file_order_up.setText(QCoreApplication.translate("MainWindow", u"\u2191", None))
        self.file_order_down.setText(QCoreApplication.translate("MainWindow", u"\u2193", None))
        self.add_emojis_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c \u0418\u0418", None))
        self.make_repost_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0440\u0435\u043f\u043e\u0441\u0442\u044b", None))
        self.clear_all_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0432\u0441\u0451", None))
        self.remember_links_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0441\u044b\u043b\u043a\u0438", None))
        self.send_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi


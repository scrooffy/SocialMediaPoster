# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'repost_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(440, 120)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(440, 120))
        Form.setMaximumSize(QSize(700, 120))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.vk_label = QLabel(Form)
        self.vk_label.setObjectName(u"vk_label")
        self.vk_label.setMinimumSize(QSize(50, 0))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.vk_label)

        self.vk_link_line = QLineEdit(Form)
        self.vk_link_line.setObjectName(u"vk_link_line")
        self.vk_link_line.setAcceptDrops(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.vk_link_line)

        self.ok_label = QLabel(Form)
        self.ok_label.setObjectName(u"ok_label")
        self.ok_label.setMinimumSize(QSize(50, 0))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ok_label)

        self.ok_link_line = QLineEdit(Form)
        self.ok_link_line.setObjectName(u"ok_link_line")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ok_link_line)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(2, QFormLayout.LabelRole, self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.remember_links_btn = QPushButton(Form)
        self.remember_links_btn.setObjectName(u"remember_links_btn")
        self.remember_links_btn.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.remember_links_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.make_repost_btn = QPushButton(Form)
        self.make_repost_btn.setObjectName(u"make_repost_btn")
        self.make_repost_btn.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.make_repost_btn)


        self.formLayout.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0440\u0435\u043f\u043e\u0441\u0442", None))
        self.vk_label.setText(QCoreApplication.translate("Form", u"VK", None))
        self.vk_link_line.setInputMask("")
        self.vk_link_line.setText("")
        self.vk_link_line.setPlaceholderText(QCoreApplication.translate("Form", u"https://vk.com/wall-228_1337", None))
        self.ok_label.setText(QCoreApplication.translate("Form", u"OK.ru", None))
        self.ok_link_line.setPlaceholderText(QCoreApplication.translate("Form", u"https://ok.ru/group/228/topic/1337", None))
        self.remember_links_btn.setText(QCoreApplication.translate("Form", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0441\u0441\u044b\u043b\u043a\u0438", None))
        self.make_repost_btn.setText(QCoreApplication.translate("Form", u"\u0421\u0434\u0435\u043b\u0430\u0442\u044c \u0440\u0435\u043f\u043e\u0441\u0442\u044b", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'front.ui'
##
# Created by: Qt User Interface Compiler version 6.5.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
                               QWidget)
from images import icons_rc


class Ui_form(object):
    def setupUi(self, form):
        if not form.objectName():
            form.setObjectName(u"form")
        form.resize(834, 664)
        self.openFileButton = QPushButton(form)
        self.openFileButton.setObjectName(u"openFileButton")
        self.openFileButton.setGeometry(QRect(70, 420, 141, 41))
        self.label = QLabel(form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 150, 171, 181))
        self.label.setPixmap(QPixmap(u"images/file_icon.png"))
        self.label.setScaledContents(True)
        self.file_info_label = QLabel(form)
        self.file_info_label.setObjectName(u"file_info_label")
        self.file_info_label.setGeometry(QRect(90, 340, 101, 16))
        self.separateFileButton = QPushButton(form)
        self.separateFileButton.setObjectName(u"pushButton")
        self.separateFileButton.setGeometry(QRect(340, 90, 121, 41))
        self.joiFileButtom = QPushButton(form)
        self.joiFileButtom.setObjectName(u"joiFileButtom")
        self.joiFileButtom.setGeometry(QRect(340, 140, 121, 41))
        self.pushButton_3 = QPushButton(form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(340, 400, 121, 41))
        self.cpfToTxtButton = QPushButton(form)
        self.cpfToTxtButton.setObjectName(u"cpfToTxtButton")
        self.cpfToTxtButton.setGeometry(QRect(340, 450, 121, 41))
        self.label_2 = QLabel(form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(340, 50, 121, 41))
        font = QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_3 = QLabel(form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(340, 360, 121, 41))
        self.label_3.setFont(font)

        self.retranslateUi(form)

        QMetaObject.connectSlotsByName(form)
    # setupUi

    def retranslateUi(self, form):
        form.setWindowTitle(QCoreApplication.translate(
            "form", u"ManipuladorDePlanilha", None))
        self.openFileButton.setText(QCoreApplication.translate(
            "form", u"Selecionar arquivo", None))
        self.label.setText("")
        self.file_info_label.setText(
            QCoreApplication.translate("form", u"NULL", None))
        self.separateFileButton.setText(
            QCoreApplication.translate("form", u"Separar", None))
        self.joiFileButtom.setText(
            QCoreApplication.translate("form", u"Juntar", None))
        self.pushButton_3.setText(
            QCoreApplication.translate("form", u"CSV para XLSX", None))
        self.cpfToTxtButton.setText(
            QCoreApplication.translate("form", u"CPF para TXT", None))
        self.label_2.setText(QCoreApplication.translate(
            "form", u"Manipulador", None))
        self.label_3.setText(QCoreApplication.translate(
            "form", u"Conversor", None))
    # retranslateUi

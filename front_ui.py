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

        self.retranslateUi(form)

        QMetaObject.connectSlotsByName(form)
    # setupUi

    def retranslateUi(self, form):
        form.setWindowTitle(QCoreApplication.translate(
            "form", u"ManipuladorDePlanilha", None))
        self.openFileButton.setText(QCoreApplication.translate(
            "form", u"Selecionar arquivo", None))
        self.label.setText("")
    # retranslateUi

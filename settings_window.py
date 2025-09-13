# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'settings_window.ui'
##
# Created by: Qt User Interface Compiler version 6.8.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
                               QLineEdit, QMainWindow, QMenuBar, QPushButton,
                               QSizePolicy, QSpinBox, QStatusBar, QTextEdit,
                               QVBoxLayout, QWidget)


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(260, 330)
        Settings.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(Settings)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 3, 0, 1, 1)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")

        self.gridLayout.addWidget(self.spinBox, 5, 0, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 9, 0, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading |
                                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 6, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout.addWidget(self.checkBox_2, 7, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout.addWidget(self.checkBox_3, 8, 0, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        Settings.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Settings)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 260, 22))
        Settings.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Settings)
        self.statusbar.setObjectName(u"statusbar")
        Settings.setStatusBar(self.statusbar)

        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate(
            "Settings", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate(
            "Settings", u"Automatic message:", None))
        self.label_3.setText(QCoreApplication.translate(
            "Settings", u"Wait time:", None))
        self.pushButton.setText(
            QCoreApplication.translate("Settings", u"apply", None))
        self.label.setText(QCoreApplication.translate(
            "Settings", u"Message title:", None))
        self.checkBox.setText(QCoreApplication.translate(
            "Settings", u"Force Visible (Debug)", None))
        self.checkBox_2.setText(
            QCoreApplication.translate("Settings", u"Log", None))
        self.checkBox_3.setText(QCoreApplication.translate(
            "Settings", u"Check Messages", None))
    # retranslateUi

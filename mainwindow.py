# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(276, 262)
        self.actionBrowser = QAction(MainWindow)
        self.actionBrowser.setObjectName(u"actionBrowser")
        self.actionBrowser.setCheckable(False)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 40))
        font = QFont()
        font.setFamilies([u"URW Bookman"])
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.pushButton.setFont(font)

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"URW Bookman"])
        font1.setPointSize(20)
        font1.setBold(True)
        font1.setItalic(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 276, 23))
        self.menusettings = QMenu(self.menubar)
        self.menusettings.setObjectName(u"menusettings")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menusettings.menuAction())
        self.menusettings.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionBrowser.setText(QCoreApplication.translate("MainWindow", u"Browser", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Click here", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.menusettings.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


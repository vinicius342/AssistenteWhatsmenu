import time
import qdarkstyle
from whatsapp import Whatsapp
from whatsmenu import Whatsmenu
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from threading import Thread
from mainwindow import Ui_MainWindow
from settings_window import Ui_Settings
from utils import SETTINGS_PROFILE_PATH, WINDOW_ICON_PATH, STYLE
import json


class Interface(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, parameters: dict = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.settings = SettingWindow(parameters=parameters)
        self.pushButton.clicked.connect(self.button_click)
        self.actionSettings.triggered.connect(self.settings.show)
        self.config_drivers(parameters)
        self.settings.applied.connect(self.config_drivers)
        self.label.setObjectName('status_label')

    def config_drivers(self, parameters: dict):
        self.msg_title = parameters['msg_title']
        self.automatic_msg = parameters['automatic_msg']
        self.browser_headless = parameters['browser']
        self.wait_time = parameters['wait_time']
        self.log_on = parameters['log_on']
        self.mythread = Thread(target=self.browsers)
        self.chat = Whatsapp(msg_title=self.msg_title,
                             automatic_msg=self.automatic_msg,
                             headless=self.browser_headless)
        self.chat.log_on = self.log_on
        self.whatsmenu = Whatsmenu(
            self.chat, self.browser_headless, self.wait_time)

    def browsers(self):
        self.chat.start()
        if self.chat.active_start:
            self.whatsmenu.start()

    def button_click(self):
        if self.label.text() == 'OFF':
            self.mythread.start()
            self.label.setText('ON')
            self.label.setStyleSheet('color: #2dff88')
            self.pushButton.setDisabled(True)
        else:
            self.whatsmenu.window_signal = True
            try:
                self.whatsmenu.driver.close()
            except Exception as e:
                print('whatsmenu close()', e.__class__.__name__)

            try:
                self.chat.driver.close()
            except Exception as e:
                print('chat close()', e.__class__.__name__)

            self.mythread = Thread(target=self.browsers)
            self.chat = Whatsapp(msg_title=self.msg_title,
                                 automatic_msg=self.automatic_msg,
                                 headless=self.browser_headless)
            self.whatsmenu = Whatsmenu(
                self.chat, self.browser_headless, self.wait_time)

            self.label.setText('OFF')

    def closeEvent(self, _):

        if self.chat.driver != None:
            try:
                self.chat.close()
            except Exception as e:
                print('chat close()', e.__class__.__name__)

        if self.whatsmenu.driver != None:
            try:
                self.whatsmenu.close()
            except AttributeError as e:
                print('whatsmenu close()', e.__class__.__name__)

    def adjustsizefixed(self) -> None:
        self.setFixedSize(self.width(), self.height())


class SettingWindow(Ui_Settings, QMainWindow):
    applied = Signal(dict)

    def __init__(self, parent=None, parameters=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.apply_clicked)
        self.settings_dict = parameters
        self.lineEdit.setText(parameters['msg_title'])
        self.textEdit.setText(parameters['automatic_msg'])
        self.checkBox.setChecked(parameters['browser'])
        self.checkBox_2.setChecked(parameters['log_on'])
        self.spinBox.setSpecialValueText(parameters['wait_time'])

    def apply_clicked(self) -> None:
        self.lineEdit.text()
        self.settings_dict['msg_title'] = self.lineEdit.text()
        self.settings_dict['automatic_msg'] = self.textEdit.toPlainText()
        self.settings_dict['wait_time'] = self.spinBox.text()
        self.settings_dict['browser'] = self.checkBox.isChecked()
        self.settings_dict['log_on'] = self.checkBox_2.isChecked()
        with open(SETTINGS_PROFILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(self.settings_dict, file, ensure_ascii=False)
        self.applied.emit(self.settings_dict)
        self.close()


if __name__ == '__main__':

    app = QApplication()

    settings_json = {'msg_title': '', 'automatic_msg': '',
                     'browser': True, 'wait_time': '10', 'log_on': False}
    try:
        with open(SETTINGS_PROFILE_PATH, 'r', encoding='utf8') as file:
            settings_json = json.load(file)
    except Exception as e:
        print('json', e.__class__.__name__)

    # Changing the theme
    icon = QIcon(str(WINDOW_ICON_PATH))
    app.setWindowIcon(icon)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    app.setStyleSheet(STYLE)
    mainwindow = Interface(parameters=settings_json)
    mainwindow.setWindowIcon(icon)
    mainwindow.settings.setWindowIcon(icon)

    mainwindow.adjustsizefixed()
    mainwindow.show()
    app.exec()

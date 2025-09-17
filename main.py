import json
import time
from threading import Thread

import qdarkstyle
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from selenium.common.exceptions import NoSuchElementException

from mainwindow import Ui_MainWindow
from settings_window import Ui_Settings
from utils import SETTINGS_PROFILE_PATH, STYLE, WINDOW_ICON_PATH
from whatsapp import Whatsapp
from whatsmenu import Whatsmenu


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
        self.interface_closed = False

    def config_drivers(self, parameters: dict):
        self.msg_title = parameters['msg_title']
        self.automatic_msg = parameters['automatic_msg']
        self.force_visible = parameters.get('force_visible', False)
        self.wait_time = parameters['wait_time']
        self.log_on = parameters['log_on']
        self.check_messages = parameters['check_messages']
        self.mythread = Thread(target=self.browsers)
        self.chat = Whatsapp(msg_title=self.msg_title,
                             automatic_msg=self.automatic_msg,
                             force_visible=self.force_visible,
                             check_messages=self.check_messages)
        self.chat.log_on = self.log_on
        self.whatsmenu = Whatsmenu(
            self.chat, self.force_visible, self.wait_time)

    def browsers(self):
        try:
            self.chat.start()
        except NoSuchElementException as e:
            print('start chat canceled', e.__class__.__name__)
            return
        except Exception as e:
            print('start chat canceled', e.__class__.__name__)
            return
        if not self.interface_closed:
            try:
                self.whatsmenu.start()
            except Exception as e:
                print('start whatsmenu canceled', e.__class__.__name__)

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
                                 force_visible=self.force_visible,
                                 check_messages=self.check_messages)
            self.whatsmenu = Whatsmenu(
                self.chat, self.force_visible, self.wait_time)

            self.label.setText('OFF')

    def closeEvent(self, _):
        self.interface_closed = True

        if self.chat.driver is not None:
            try:
                self.chat.close()
                self.chat.driver.quit()
            except Exception as e:
                print('chat close()', e.__class__.__name__)
        if self.whatsmenu.driver is not None:
            try:
                self.whatsmenu.close()
                self.whatsmenu.driver.quit()
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
        force_visible = (parameters.get('force_visible', False)
                         if parameters else False)
        self.checkBox.setChecked(force_visible)
        log_on = parameters['log_on'] if parameters else False
        self.checkBox_2.setChecked(log_on)
        check_msg = parameters['check_messages'] if parameters else True
        self.checkBox_3.setChecked(check_msg)
        wait_time = parameters['wait_time'] if parameters else '10'
        self.spinBox.setSpecialValueText(wait_time)

    def apply_clicked(self) -> None:
        if self.settings_dict is None:
            self.settings_dict = {}
        self.lineEdit.text()
        self.settings_dict['msg_title'] = self.lineEdit.text()
        self.settings_dict['automatic_msg'] = self.textEdit.toPlainText()
        self.settings_dict['wait_time'] = self.spinBox.text()
        self.settings_dict['force_visible'] = self.checkBox.isChecked()
        self.settings_dict['log_on'] = self.checkBox_2.isChecked()
        self.settings_dict['check_messages'] = self.checkBox_3.isChecked()
        with open(SETTINGS_PROFILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(self.settings_dict, file, ensure_ascii=False)
        self.applied.emit(self.settings_dict)
        self.close()


if __name__ == '__main__':

    app = QApplication()

    # Configurações padrão (sempre atualizadas)
    default_settings = {
        'msg_title': '',
        'automatic_msg': '',
        'force_visible': False,
        'wait_time': '10',
        'log_on': False,
        'check_messages': True
    }

    settings_json = default_settings.copy()

    try:
        with open(SETTINGS_PROFILE_PATH, 'r', encoding='utf8') as file:
            loaded_settings = json.load(file)

            # === MIGRAÇÃO DE CONFIGURAÇÕES ANTIGAS ===
            # Migrar 'browser' para 'force_visible' (versão antiga)
            if ('browser' in loaded_settings and
                    'force_visible' not in loaded_settings):
                old_browser = loaded_settings.pop('browser')
                loaded_settings['force_visible'] = old_browser
                print("Migrado: 'browser' → 'force_visible'")

            # === ADIÇÃO DE NOVAS CONFIGURAÇÕES ===
            # Adiciona qualquer configuração nova que não existir
            for key, default_value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = default_value
                    print(f"Adicionado: '{key}' = {default_value}")

            # Remove configurações obsoletas (opcional)
            obsolete_keys = ['browser']  # Lista de chaves antigas
            for old_key in obsolete_keys:
                if old_key in loaded_settings:
                    loaded_settings.pop(old_key)
                    print(f"Removido: '{old_key}' (obsoleto)")

            # Aplica as configurações carregadas/migradas
            settings_json.update(loaded_settings)

            # Salva o arquivo atualizado com as migrações
            save_path = SETTINGS_PROFILE_PATH
            with open(save_path, 'w', encoding='utf-8') as save_file:
                json.dump(settings_json, save_file, ensure_ascii=False,
                          indent=2)

    except FileNotFoundError:
        print("Arquivo de configurações não encontrado - usando padrões")
        # Cria o arquivo com configurações padrão
        with open(SETTINGS_PROFILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(settings_json, file, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        print("Arquivo de configurações corrompido - recriando com padrões")
        # Backup do arquivo corrompido
        import shutil
        shutil.copy(SETTINGS_PROFILE_PATH, f"{SETTINGS_PROFILE_PATH}.backup")
        # Cria novo arquivo
        with open(SETTINGS_PROFILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(settings_json, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Erro carregando configurações:', e.__class__.__name__)
        print("Usando configurações padrão")

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

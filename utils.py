from pathlib import Path

ROOT_DIR = Path(__file__).parent
PROFILE_WHATSAPP_PATH = ROOT_DIR / 'profile_whatsapp' / 'wpp'
PROFILE_WHATSMENU_PATH = ROOT_DIR / 'profile_whatsmenu' / 'whatsmenu'
SETTINGS_PROFILE_PATH = ROOT_DIR / 'settings.json'
WINDOW_ICON_PATH = ROOT_DIR / 'icon' / 'hamburguer.ico'
FILE_LOG = ROOT_DIR / 'log.txt'


STYLE = '''
/* Janela principal */
QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #f0f0f0;
    font-family: "Segoe UI", "Arial";
    font-size: 14px;
}

/* Botões */
QPushButton {
    background-color: #3a3a3a;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #505050;
}

QPushButton:pressed {
    background-color: #2d8cff;
    color: white;
}

/* Labels */
QLabel {
    color: #f0f0f0;
}

/* Caixas de texto */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #2c2c2c;
    color: #ffffff;
    border: 1px solid #444;
    border-radius: 4px;
}

/* SpinBox e ComboBox */
QSpinBox, QComboBox {
    background-color: #2c2c2c;
    color: #ffffff;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 4px;
}

QComboBox QAbstractItemView {
    background-color: #2c2c2c;
    color: #ffffff;
    selection-background-color: #2d8cff;
}

/* Checkboxes */
QCheckBox {
    color: #f0f0f0;
}

QCheckBox::indicator {
    border: 1px solid #666;
    background-color: #3a3a3a;
    width: 14px;
    height: 14px;
}

QCheckBox::indicator:checked {
    background-color: #2d8cff;
    border: 1px solid #2d8cff;
}

QLabel#status_label {
    background-color: #2c2c2c;
    color: #ff5f5f;  /* vermelho suave pra 'OFF', pode usar verde pra 'ON' */
    border: 2px solid #444;
    border-radius: 12px;
    font-size: 25px;
    font-weight: bold;
    padding: 8px 20px;
    qproperty-alignment: AlignCenter;
} '''

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Rejestracja")
        self.showFullScreen()
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        screen_width = QApplication.primaryScreen().size().width()
        box_width = screen_width // 3

        # Przycisk wyjścia z programu
        self.exit_btn = QPushButton("Powrót")
        self.exit_btn.clicked.connect(self.back_to_login)
        self.exit_btn.setFixedSize(80, 50)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #EE0000;
                color: #DADFDA;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4c4c;
            }
        """)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("images/logo_invy.png")
        pixmap = pixmap.scaledToWidth(box_width - 40, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Login
        login_label = QLabel("Login")
        login_label.setAlignment(Qt.AlignLeft)
        self.username = QLineEdit()

        # Hasło
        password_label = QLabel("Hasło")
        password_label.setAlignment(Qt.AlignLeft)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # Powtórz Hasło
        repeat_password_label = QLabel("Powtórz hasło")
        repeat_password_label.setAlignment(Qt.AlignLeft)
        self.repeat_password = QLineEdit()
        self.repeat_password.setEchoMode(QLineEdit.Password)

        # Guzik logowania
        self.login_btn = QPushButton("Zarejestruj")
        self.login_btn.clicked.connect(self.register)

        # Komunikaty
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("color: #e74c3c; font-size: 14px;")

        # Top layout z przyciskiem Wyjdź
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 0)
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        top_layout.addWidget(self.exit_btn)

        # Layout centralny z boxem logowania
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(40, 40, 40, 40)
        login_layout.setSpacing(20)
        login_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        login_layout.addWidget(logo_label)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.username)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password)
        login_layout.addWidget(repeat_password_label)
        login_layout.addWidget(self.repeat_password)
        login_layout.addWidget(self.login_btn)
        login_layout.addWidget(self.message)
        login_layout.addStretch(1)

        # Centralny widget boxa logowania
        login_widget = QWidget()
        login_widget.setFixedWidth(box_width)
        login_widget.setLayout(login_layout)

        # Center layout do wyśrodkowania boxa
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(login_widget)

        # Główny layout okna
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(center_layout)
        outer_layout.addStretch(1)

        self.setLayout(outer_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #221D1D;
                color: #ffffff;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #E1E1E1;
                color: #0D2540;
                border: 2px solid #221D1D;
                border-radius: 20px;
                padding: 10px;
                height: 25px;
            }
            QLineEdit:focus {
                border: 4px solid #3daee9;
            }
            QPushButton {
                background-color: #959393;
                color: #0D2540;
                border: none;
                border-radius: 20px;
                padding: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5bc0ff;
            }
            QLabel {
                font-weight: bold;
                font-size: 25px;
            }
        """)

    def register(self):
        # ---------------------------------------------------------------------------       CZESC SERWEROWA
        # trzeba dodać sprawdzenie czy istnieje już taki użytkownik oraz utworzenie nowego użytkownika w bazie
        # trzeba też dodać więcej komunikatów
        if self.password.text() != self.repeat_password.text():
            self.message.setText("Hasła nie są zgodne.")

    def back_to_login(self):
        self.login_window.showNormal()
        self.login_window.raise_()
        self.login_window.activateWindow()
        self.login_window.setWindowState(Qt.WindowFullScreen)
        self.close()
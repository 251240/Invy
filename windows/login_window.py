from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from windows.main_window import MainWindow
from windows.register_window import RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logowanie")
        self.showFullScreen()
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        screen_width = QApplication.primaryScreen().size().width()
        box_width = screen_width // 3

        # Przycisk wyjścia z programu
        self.exit_btn = QPushButton("Wyjdź")
        self.exit_btn.clicked.connect(QApplication.quit)
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

        # Guzik logowania
        self.login_btn = QPushButton("Zaloguj")
        self.login_btn.clicked.connect(self.check_login)

        # Guzik rejestracji
        self.register_btn = QPushButton("Zarejestruj się")
        self.register_btn.clicked.connect(self.open_register_window)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #004AAD;
                color: #D8DBD5;
            }
            QPushButton:hover {
                background-color: #197CFF;
            }
        """)

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
        login_layout.setAlignment(Qt.AlignHCenter)
        login_layout.addWidget(logo_label)
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.username)
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password)
        login_layout.addWidget(self.login_btn)
        login_layout.addWidget(self.register_btn)
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
                background-color: #eeeeee;
            }
            QLabel {
                font-weight: bold;
                font-size: 25px;
            }
        """)

    def check_login(self):
        # trzeba też dodać więcej komunikatów np. wpisz hasło
        # należy dodać logikę czy użytkownik istnieje i czy jest dobre hasło
        # ------------------------------------------------------------------------- DODAĆ SERWER
        if self.username.text() == "admin" and self.password.text() == "123":
            self.open_main_window()
        else:
            self.message.setText("Nieprawidłowy login lub hasło!")

    def open_register_window(self):
        self.register_window = RegisterWindow(login_window=self)
        self.register_window.raise_()
        self.register_window.activateWindow()
        self.hide()

    def open_main_window(self):
        # -----------------------------------------------------------DODAĆ SERWEROWE
        #MainWindow musi trzymać dane o asortymencie, pobieramy dane z serwera i dajemy do obiektu
        #placeholder, to powinno być dodawane z serwera                                                         !!!!!!!!!!!!!!!!
        products = [
            {"name": "Laptop", "price": 2500, "category": "Elektronika", "available": True},
            {"name": "Telefon", "price": 1800, "category": "Elektronika", "available": True},
            {"name": "Słuchawki", "price": 300, "category": "Elektronika", "available": False},
            {"name": "Krzesło", "price": 450, "category": "Dom i ogród", "available": True},
            {"name": "Lampa", "price": 120, "category": "Dom i ogród", "available": False},
            {"name": "Kurtka", "price": 600, "category": "Moda", "available": True},
            {"name": "Buty", "price": 400, "category": "Moda", "available": False},
            {"name": "Buty", "price": 400, "category": "Moda", "available": False},
            {"name": "Buty", "price": 400, "category": "Moda", "available": False},
            {"name": "Buty", "price": 400, "category": "Moda", "available": False},
        ]
        self.main_window = MainWindow(login_window=self, products=products)
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.hide()



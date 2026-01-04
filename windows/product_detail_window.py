from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QApplication, QGridLayout
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class ProductDetailWindow(QWidget):
    def __init__(self, product):
        super().__init__()
        self.product = product
        self.setWindowTitle("Szczegóły produktu")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setFixedSize(600, 400)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # przy otwieraniu też trzeba dodać odczyt danych z serwera
        # -------------------------------------------------------------------- SERWER

        # --- Main grid layout ---
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- Back button ---
        self.back_btn = QPushButton("Powrót")
        self.back_btn.setFixedSize(60, 30)
        self.back_btn.clicked.connect(self.close_and_save)
        layout.addWidget(self.back_btn, 0, 0, 1, 1)

        # --- Labels and editable fields ---
                                                        #powinno wczytać dane z bazy, trzeba też ustalić metodę wpisywania adresu
        self.name_edit = QLineEdit("placeholder")
        self.id_edit = QLineEdit("placeholder")
        self.price_edit = QLineEdit("placeholder")
        self.address_edit = QLineEdit("placeholder")

        layout.addWidget(QLabel("Nazwa produktu"), 1, 0)
        layout.addWidget(self.name_edit, 2, 0)

        layout.addWidget(QLabel("Id produktu"), 1, 1)
        layout.addWidget(self.id_edit, 2, 1)

        # --- Image upload ---
        #dodać logikę zapisywania zdjęcia z serwera                                                                         !!!!
        self.image_btn = QPushButton()
        self.image_btn.setFixedSize(100, 50)
        self.image_btn.setIconSize(self.image_btn.size())
        self.image_btn.setText("Dodaj zdjęcie")
        self.image_btn.clicked.connect(self.select_image)
        layout.addWidget(QLabel("Zdjęcie"), 1, 2)
        layout.addWidget(self.image_btn, 2, 2)

        layout.addWidget(QLabel("Adres produktu"), 1, 3)
        layout.addWidget(self.address_edit, 2, 3)

        # --- Quantity & unit selection ---
        #self.quantity_edit = QLineEdit(str(self.product.get("quantity", "")))   to było, ale trzeba dodać wczytanie ilości z serwera
        self.quantity_edit = QLineEdit("placeholder")
        self.quantity_unit = QComboBox()
        self.quantity_unit.addItems(["kg", "szt"])
        self.quantity_unit.setCurrentText(self.product.get("quantity_unit", "kg"))

        layout.addWidget(QLabel("Ilość"), 3, 0)
        layout.addWidget(self.quantity_edit, 4, 0)

        layout.addWidget(QLabel("Jednostka ilości"), 3, 1)
        layout.addWidget(self.quantity_unit, 4, 1)

        layout.addWidget(QLabel("Cena"), 3, 2)
        layout.addWidget(self.price_edit, 4, 2)

        # --- Sales unit selection ---
        self.sales_unit = QComboBox()
        self.sales_unit.addItems(["kg", "szt"])
        # self.sales_unit.setCurrentText(self.product.get("sales_unit", "kg"))                  tak było ale trzeba zmienić
        self.sales_unit.setCurrentText("placeholder")

        layout.addWidget(QLabel("Jednostka sprzedaży"), 3, 3)
        layout.addWidget(self.sales_unit, 4, 3)

        self.setLayout(layout)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz zdjęcie", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            pixmap = QPixmap(path).scaled(self.image_btn.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_btn.setIcon(QIcon(pixmap))
            self.image_btn.setText("")

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Segoe UI;
            }
            QLabel {
                font-size: 13px;
            }
            QLineEdit {
                background-color: #2e2e2e;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 5px 10px;
                color: white;
            }
            QPushButton {
                background-color: #d0d0d0;
                color: #000000;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #aaaaaa;
            }
            QComboBox {
                background-color: #2e2e2e;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 5px;
                color: white;
            }
        """)

    def close_and_save(self):
        #dodać zapisanie zmian do bazy danych
        # ----------------------------------------------------------------- SERWER
        self.close()


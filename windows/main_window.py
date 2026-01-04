from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QGroupBox, QCheckBox, QSpinBox, QScrollArea
)
from PyQt5.QtCore import Qt
from windows.product_detail_window import ProductDetailWindow


class MainWindow(QMainWindow):
    def __init__(self, login_window, products):
        super().__init__()
        self.login_window = login_window
        self.products = products

        self.setWindowTitle("Produkty")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.showFullScreen()
        self.setup_ui()
        self.apply_styles()
        self.update_product_list(self.products)

    def setup_ui(self):
        #UWAGA, TRZEBA DODAĆ LOGIKĘ FILTRÓW, CZYLI JEŻELI DODAJEMY NOWĄ NP. PÓŁKĘ TO POJAWIA SIĘ NOWY GUZIK
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ===================== TOP BAR =====================
        top_bar = QHBoxLayout()

        self.logout_btn = QPushButton("Wyloguj")
        self.logout_btn.setFixedSize(80, 50)
        self.logout_btn.setStyleSheet("""
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
        self.logout_btn.clicked.connect(self.back_to_login)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Wyszukaj produkt")

        self.search_btn = QPushButton("Szukaj")
        self.search_btn.setFixedSize(80, 50)
        self.search_btn.clicked.connect(self.apply_filters)

        top_bar.addWidget(self.logout_btn)
        top_bar.addWidget(self.search_input, 1)
        top_bar.addWidget(self.search_btn)

        main_layout.addLayout(top_bar)

        # ===================== CONTENT =====================
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # ---------- LEFT SIDE ----------
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        self.add_product_btn = QPushButton("Dodaj nowy produkt   +")
        self.add_product_btn.setFixedHeight(60)
        left_layout.addWidget(self.add_product_btn)

        self.products_list = QListWidget()
        self.products_list.verticalScrollBar().setSingleStep(10)
        self.products_list.verticalScrollBar().setPageStep(60)
        self.products_list.setSpacing(10)
        self.products_list.itemClicked.connect(self.show_product_detail)

        left_layout.addWidget(self.products_list)

        # ---------- RIGHT SIDE (FILTERS SCROLL) ----------
        filters_container = QWidget()
        filters_layout = QVBoxLayout(filters_container)
        filters_layout.setAlignment(Qt.AlignTop)
        filters_layout.setSpacing(20)
        filters_layout.setContentsMargins(10, 10, 10, 10)

        # Działy
        dept_group = QGroupBox("Działy")
        dept_layout = QVBoxLayout()
        dept_layout.addWidget(QPushButton("Dział 1"))
        dept_layout.addWidget(QPushButton("Dział 2"))
        dept_layout.addWidget(QPushButton("Dział 3"))
        dept_group.setLayout(dept_layout)

        # Regały
        rack_group = QGroupBox("Regały")
        rack_layout = QVBoxLayout()
        rack_layout.addWidget(QPushButton("Regał 1"))
        rack_layout.addWidget(QPushButton("Regał 2"))
        rack_layout.addWidget(QPushButton("Regał 3"))
        rack_group.setLayout(rack_layout)

        # Półki
        shelf_group = QGroupBox("Półki")
        shelf_layout = QVBoxLayout()
        shelf_layout.addWidget(QPushButton("Półka 1"))
        shelf_group.setLayout(shelf_layout)

        filters_layout.addWidget(dept_group)
        filters_layout.addWidget(rack_group)
        filters_layout.addWidget(shelf_group)
        filters_layout.addStretch()

        filters_scroll = QScrollArea()
        filters_scroll.setWidget(filters_container)
        filters_scroll.setWidgetResizable(True)
        filters_scroll.setFixedWidth(300)

        # ---------- ADD TO CONTENT ----------
        content_layout.addLayout(left_layout, 4)
        content_layout.addWidget(filters_scroll, 1)

        main_layout.addLayout(content_layout)

    # ===================== STYLES =====================
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #221D1D;
                color: #ffffff;
                font-family: Segoe UI;
            }

            QLineEdit {
                background-color: #e0e0e0;
                color: #000;
                border-radius: 18px;
                padding: 10px;
                font-size: 16px;
            }

            QPushButton {
                background-color: #959393;
                color: #0D2540;
                border-radius: 20px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #eeeeee;
            }

            QListWidget {
                background: transparent;
                border: none;
            }

            QListWidget::item {
                background-color: #9e9e9e;
                border-radius: 25px;
                padding: 18px;
                margin-bottom: 12px;
                color: #000;
                font-size: 16px;
            }

            QGroupBox {
                border: none;
                font-size: 18px;
                font-weight: bold;
                margin-top: 20px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
            }
            
            
            QGroupBox QPushButton {
                border-radius: 11px;
                min-height: 22px;
                background-color: #484242;
                color: #FFFFEE;
            }

            QScrollArea {
                border: none;
            }
        """)

    # ===================== LOGIC =====================
    def back_to_login(self):
        self.login_window.showNormal()
        self.login_window.raise_()
        self.login_window.activateWindow()
        self.login_window.setWindowState(Qt.WindowFullScreen)
        self.close()

    def apply_filters(self):
        # DODAĆ LOGIKĘ FILTROWANIA, POD SPODEM JEST PRZYKŁADOWA ALE NIE PASUJĄCA DO NASZEJ LOGIKI
        ''' query = self.search_input.text().lower()
        min_price = self.min_price.value()
        max_price = self.max_price.value() or float("inf")

        selected_categories = set()
        if self.cat_electronics.isChecked(): selected_categories.add("Elektronika")
        if self.cat_home.isChecked(): selected_categories.add("Dom i ogród")
        if self.cat_fashion.isChecked(): selected_categories.add("Moda")

        availability = set()
        if self.avail_yes.isChecked(): availability.add(True)
        if self.avail_no.isChecked(): availability.add(False)
        filtered = []
        for p in self.products:
            if query and query not in p["name"].lower():
                continue
            if not (min_price <= p["price"] <= max_price): continue
            if selected_categories and p["category"] not in selected_categories: continue
            if availability and p["available"] not in availability: continue
            filtered.append(p)
        self.update_product_list(filtered) '''


        # tutaj zawarta też jest logika przycisku szukaj, czyli kiedy wpiszę nazwę i kliknę szukaj to tak jakby dodaje nowy filtr,
        #
        pass

    def update_product_list(self, products):
        # UWAGA, TO TYLKO PRZYKŁADOWE TRZEBA ZMIENIĆ LOGIKĘ ABY ZGADZAŁA SIĘ Z BAZĄ DANYCH
        self.products_list.clear()
        for p in products:
            status = "Dostępny" if p["available"] else "Na zamówienie"
            item = QListWidgetItem(
                f"{p['name']}\nCena: {p['price']} zł/kg\n"
            )
            item.setSizeHint(item.sizeHint() * 2)
            self.products_list.addItem(item)

    def show_product_detail(self, item):
        # UWAGA, TRZEBA SPRAWDZIĆ CZY PO USTALENIU LOGIKI TO NADAL JEST OK CZY NALEŻY ZMIENIĆ
        name = item.text().split("\n")[0]
        for p in self.products:
            if p["name"] == name:
                self.detail_window = ProductDetailWindow(p)
                self.detail_window.show()
                break

import socket
import threading
import json
import sqlite3


#nie potrzeba korzystac z zadnych funkcji tutaj server ogolnie jak sie odpali to dziala
#odbiera od klienta informacje i odsyla co trzeba
class Server:
    def __init__(self, host='0.0.0.0', port=12345, db_name="users.db"):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def start(self):
        print(f"Serwer działa na: {self.host}:{self.port}")
        self.init_db(self.db_name)
        try:
            while True:
                conn, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        finally:
            self.close()

    def handle_client(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                try:
                    request = json.loads(data.decode())
                    response = self.process_request(request)
                    conn.sendall(json.dumps(response).encode())
                except Exception as e:
                    conn.sendall(json.dumps({"status": "error", "message": str(e)}).encode())

    def process_request(self, request):
        login = request.get("login")
        haslo = request.get("haslo")

        if not login or not haslo:
            return {"status": "error", "message": "Brak login/hasło"}

        ok, result = self.authenticate(login, haslo)
        if not ok:
            return {"status": "error", "message": result}

        id_klienta = result

        if "products" in request:
            self.update_products(id_klienta, request["products"])
            return {"status": "success", "message": "Produkty zapisane"}

        products = self.get_products(id_klienta)
        return {"status": "success", "products": products}

    def init_db(self, db_name):
        with sqlite3.connect(db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE,
                    haslo TEXT
                )
            """)

    def authenticate(self, login, haslo):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id_klienta, haslo FROM clients WHERE login=?", (login,))
            row = cur.fetchone()

            if row:
                if row[1] != haslo:
                    return False, "Złe hasło"
                self.create_products_table(row[0])
                return True, row[0]
            else:
                cur.execute("INSERT INTO clients(login, haslo) VALUES(?,?)", (login, haslo))
                conn.commit()
                id_klienta = cur.lastrowid
                self.create_products_table(id_klienta)
                return True, id_klienta

    def create_products_table(self, id_klienta):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS produkty_{id_klienta} (
                    id_produktu INTEGER,
                    nazwa TEXT,
                    zdjecie TEXT,
                    cena INTEGER,
                    jednostka_sprzedazy TEXT,
                    ilosc INTEGER,
                    jednostka_ilosci TEXT,
                    dzial INTEGER,
                    regal INTEGER,
                    polka INTEGER
                )
            """)

    def get_products(self, id_klienta):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM produkty_{id_klienta}")
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def update_products(self, id_klienta, products):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM produkty_{id_klienta}")

            for p in products:
                cur.execute(f"""
                    INSERT INTO produkty_{id_klienta}
                    (id_produktu, nazwa, zdjecie, cena,
                     jednostka_sprzedazy, ilosc, jednostka_ilosci,
                     dzial, regal, polka)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get("id_produktu"),
                    p.get("nazwa"),
                    p.get("zdjecie"),
                    p.get("cena"),
                    p.get("jednostka_sprzedazy"),
                    p.get("ilosc"),
                    p.get("jednostka_ilosci"),
                    p.get("dzial"),
                    p.get("regal"),
                    p.get("polka")
                ))
            conn.commit()

    def close(self):
        self.server_socket.close()


if __name__ == "__main__":
    Server().start()

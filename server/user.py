import socket
import json


#klasa dla uzytkownika
#poza rzeczami do serwera to liczy sie login, haslo, produkty
#login i haslo to dane ktore przechowuje baza danych
#jak podamy login ktorego nie ma w bazie to zostanie on dodany z podanym haslem
#jak podamy login ktory juz jest z blednym haslem to jest blad
#noi produkty trzeba przechowywac jako tablica slownikow o okreslonych nazwach zeby serwer wiedzial o co chodzi
#przyklad wpisu w tablicy produkty:
#{"nazwa": "Mleko 3.2%","zdjecie": "mleko.png","cena": 4,"jednostka_sprzedazy": "szt","ilosc": 3,"jednostka_ilosci": "l","dzial": "nabial","regal": "B","polka": "2"}
#w trakcie dzialania programu edytujemy ta liste i potem tylko funkcja  close ktora odsyla zmieniona liste do serwera
class User:
    def __init__(self, login, password, host="127.0.0.1", port=12345):
        self.login = login
        self.password = password
        self.produkty = []
        self.host = host
        self.port = port
        self.socket = None

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send(self, data):
        self.socket.sendall(json.dumps(data).encode("utf-8"))
        response = self.socket.recv(4096)
        return json.loads(response.decode("utf-8"))


    def login_user(self):
        self._connect()
        request = {
            "login": self.login,
            "haslo": self.password
        }

        response = self._send(request)

        if response.get("status") != "success":
            print("[ERROR] Logowanie nieudane:", response.get("message"))
            self.socket.close()
            self.socket = None
            return False

        self.produkty = response.get("products", [])
        print(f"[OK] Zalogowano jako {self.login}")
        print(f"[INFO] Pobrano {len(self.produkty)} produktów")

        return True


    def close(self):
        if not self.socket:
            return

        request = {
            "login": self.login,
            "haslo": self.password,
            "products": self.produkty
        }

        response = self._send(request)

        if response.get("status") == "success":
            print("[OK] Produkty zapisane w bazie")
        else:
            print("[ERROR] Nie udało się zapisać produktów:", response)

        self.socket.close()
        self.socket = None

def main():
    user = User("test", "123")

    user.login_user()

    user.produkty.append({
        "nazwa": "Mleko 3.2%",
        "zdjecie": "mleko.png",
        "cena": 4,
        "jednostka_sprzedazy": "zl",
        "ilosc": 3,
        "jednostka_ilosci": "l",
        "dzial": "nabial",
        "regal": "B",
        "polka": "2"
    })
    user.produkty.append({
        "nazwa": "Pomidor",
        "zdjecie": "./Images/pomidor.png",
        "cena": 2,
        "jednostka_sprzedazy": "zl",
        "ilosc": 100,
        "jednostka_ilosci": "kg",
        "dzial": "warzywa",
        "regal": "A",
        "polka": "1"
    })


    user.close()


if __name__ == "__main__":
    main()

import socket
import threading
import hashlib

# ЗБЕРІГАННЯ ДАНИХ КОРИСТУВАЧІВ
# має бути замінено базою даних
USER_CREDENTIALS = {
    "kyryl": hashlib.sha256("raccoon".encode()).hexdigest()
}

# функція гешування паролю
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# словник відстеження невдалих спроб входу
failed_attempts = {}

# функція оброблення кожного клієнтського запиту
def handle_client(client_socket):
    try:
        # отримання автентифікаційних даних користувача/-ки
        auth_data = client_socket.recv(1024).decode()
        print(f"[СЕРВЕР] Отримані автентифікаційні дані: {auth_data}")
        
        # перевірка чи отримані дані містять як прізвисько, так і пароль
        if ',' in auth_data:
            username, raw_password = auth_data.split(',')
            print(f"[СЕРВЕР] Спроба автентифікації на профіль: '{username}'")
            print(f"[СЕРВЕР] Отриманий пароль від користувача/-ки: '{raw_password}'")

            # гешування отриманого паролю
            hashed_password = hash_password(raw_password)
            print(f"[СЕРВЕР] Загешована версія отриманого паролю: '{hashed_password}'")

            # отримання збереженого загешованого пароля з внутрішньої бази
            stored_hash = USER_CREDENTIALS.get(username)
            print(f"[СЕРВЕР] Загешована версія збереженого паролю: '{stored_hash}'")

            # обмеження спроб ввійти за тим же прізвиськом на певного/-у користувача/-ку
            print(failed_attempts)
            if failed_attempts.get(username, 0) >= 5:
                print(f"[СЕРВЕР] Забагато провалених спроб ввійти для '{username}'. Заблоковано.")
                client_socket.send("AUTH_FAIL".encode())
                client_socket.close()
                return

            # валідація даних користувача/-ки
            if username in USER_CREDENTIALS:
                print(f"[СЕРВЕР] Користувача/-ку '{username}' знайдено у системі.")
                if stored_hash == hashed_password:
                    print(f"[СЕРВЕР] Пароль профіля '{username}' правильний.")
                    client_socket.send("AUTH_SUCCESS".encode())
                    print(f"[СЕРВЕР] Доступ до '{username}' забезпечено.")
                else:
                    print(f"[СЕРВЕР] Пароль профіля '{username}' невідповідний.")
                    failed_attempts[username] = failed_attempts.get(username, 0) + 1
                    print(f"[СЕРВЕР] Провалених спроб увійти на '{username}': {failed_attempts[username]}")
                    client_socket.send("AUTH_FAIL".encode())
            else:
                print(f"[СЕРВЕР] Користувача/-ку '{username}' не знайдено в системі.")
                client_socket.send("AUTH_FAIL".encode())
        else:
            # запит обчислення для вже автентифікованих користувача/-ки
            username = auth_data
            print(f"[СЕРВЕР] Отримано запит на обчислення від автентифікованих користувача/-ки: '{username}'")

            if username in USER_CREDENTIALS:
                print(f"[СЕРВЕР] Користувача/-ку '{username}' автентифіковано для обчислень.")
                client_socket.send("AUTH_SUCCESS".encode())

                # отримання математичного виразу
                expression = client_socket.recv(1024).decode()
                print(f"[СЕРВЕР] Отриманий вираз від користувача/-ки '{username}': {expression}")

                # ОБЧИСЛЕННЯ з eval()
                # • використовувати лише для тестових середовищ
                try:
                    result = eval(expression)
                    print(f"[СЕРВЕР] Розрахунок для виразу '{expression}': {result}")
                except Exception as e:
                    result = f"Помилка: {str(e)}"
                    print(f"[СЕРВЕР] Помилка під час спроби обчислити вираз '{expression}': {e}")

                # відправити результат назад до клієнта
                client_socket.send(str(result).encode())
            else:
                print(f"[СЕРВЕР] Користувач/-ка '{username}' не автентифіковані для обчислення.")
                client_socket.send("AUTH_FAIL".encode())
    except Exception as e:
        print(f"[СЕРВЕР] Коїлася помилка: {str(e)}")
        client_socket.send(f"Помилка: {str(e)}".encode())
    finally:
        print(f"[СЕРВЕР] Завершення з'єднання з користувачем/-кою '{username}'")
        client_socket.close()

# функція запуску сокет-сервера
def start_socket_server():
    while True:
        client, addr = server.accept()
        print(f"[СЕРВЕР] Нове з'єднання з {addr}")

        # створення окремого потоку для клієнта
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# створення сокету та прив'язка адреси
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)
print("[СЕРВЕР] Прослуховування 0.0.0.0:9999")

# запуск сервера для прийняття з'єднань
start_socket_server()

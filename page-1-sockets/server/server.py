import socket
import threading

# функція обміну даними з одним клієнтом
def handle_client(client_socket):
    # отримання виразу від клієнта
    request = client_socket.recv(1024).decode()
    try:
        # eval(): лише для тестових проєктів
        # розбір та розрахунок отриманого виразу
        result = eval(request)
    except Exception as e:
        # виявлення будь-яких помилок
        result = f"Помилка: {str(e)}"
    
    # надіслати результат на клієнтський бік
    client_socket.send(str(result).encode())
    # закрити з'єднання з клієнтом
    client_socket.close()

# функція запуску сокетового серверу та виловлення запитів
def start_socket_server():
    while True:
        client, addr = server.accept()
        print(f"[*] Прийнято з'єднання від {addr}")

        # створити новий потік для нового клієнта
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# створення сокету
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# прив'язка сервера до всіх доступ адрес на порті
server.bind(("0.0.0.0", 9999))
# почати приймати вхідні з'єднання (черга на макс. 5 клієнтів)
server.listen(5)
print("[*] Прослуховування 0.0.0.0:9999")

# запустити сервер та почати приймати запити
start_socket_server()
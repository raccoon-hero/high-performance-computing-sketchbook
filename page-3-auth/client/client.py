from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import socket

# ініціалізація Flask-застосунку
app = Flask(__name__)

# секретний ключ для забезпечення роботи сесій/реп'яшків
app.secret_key = "your_secret_key" 

# шлях до початкової сторінки
@app.route('/')
def index():
    # якщо користувач/-ка автентифіковані, то спрямувати на обчислення
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('calculator'))
    # якщо не автентифіковані, то спрямувати на сторінку автентифікації
    return render_template('login.html')

# шлях до сторінки автентифікації
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    print(f"[КЛІЄНТ] Надсилання спроби автентифікації для '{username}'")

    # встановлення сокетового з'єднання з сервером для валідації даних
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    # надсилання даних на сервер без оброблення
    auth_data = f"{username},{password}"
    client.send(auth_data.encode())

    # отримати відповідь щодо автентифікації
    auth_response = client.recv(1024).decode()
    print(f"[КЛІЄНТ] Отриманий результат автентифікації: {auth_response}")

    if auth_response == "AUTH_SUCCESS":
        # якщо автентифікація успішна, визначити змінні сесії та спрямувати на калькулятор
        session['logged_in'] = True
        session['username'] = username
        print(f"[КЛІЄНТ] Користувачу/-ці '{username}' забезпечено доступ.")
        client.close()
        return redirect(url_for('calculator'))
    else:
        # якщо автентифікація неуспішна, повернутись на сторінку автентифікації з повідомленням про помилку
        client.close()
        print(f"[КЛІЄНТ] Користувача/-ку '{username} не вдалося автентифікувати.")
        error_message = "Невідповідне прізвисько чи пароль. Спробуй знову."
        return render_template('login.html', error=error_message)

# шлях до сторінки обчислення
@app.route('/calculator')
def calculator():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('index'))
    return render_template('index.html')

# шлях до виходу зі системи
@app.route('/logout')
def logout():
    print(f"[CLIENT] User '{session.get('username')}' logged out.")
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# шлях до процесу обчислення
@app.route('/calculate', methods=['POST'])
def calculate():
    # перевірка на автентифікованість перед початком процесу
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify(result="Помилка: У доступі відмовлено"), 403

    data = request.json
    expression = data.get('expression')

    # під'єднатися до сервера
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    # надіслати прізвисько із запису сесії для автентифікації обчислення
    # пароль для подальших автентифікаційних запитів не потрібен
    username = session['username'] 
    auth_data = f"{username}"  
    print(f"[КЛІЄНТ] Надсилання автентифікаційних даних для обчислення: {auth_data}")
    client.send(auth_data.encode())

    # отримати відповідь щодо автентифікації
    auth_response = client.recv(1024).decode()
    print(f"[КЛІЄНТ] Отриманий результат автентифікації: {auth_response}")

    if auth_response == "AUTH_SUCCESS":
        # надіслати математичний вираз після автентифікації
        print(f"[КЛІЄНТ] Надсилання виразу: {expression}")
        client.send(expression.encode())
        response = client.recv(4096).decode()
        print(f"[КЛІЄНТ] Отриманий результат: {response}")
    else:
        response = "Помилка: Автентифікація не була успішною."
        print(f"[КЛІЄНТ] Автентифікація не вдалася під час обчислення.")

    client.close()
    return jsonify(result=response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

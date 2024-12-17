from flask import Flask, render_template, request, jsonify
import socket

# ініціаліалізація Flask-застосунку
app = Flask(__name__)

# визначення головної сторінки
@app.route('/')
def index():
    return render_template('index.html')

# визначення запиту для обчислень
@app.route('/calculate', methods=['POST'])
def calculate():
    # отримання вхідних даних у json-форматі
    data = request.json
    # зберігання безспосередньо виразу
    expression = data.get('expression')
    
    # приєднатись до сервера обчислення з допомогою TCP-сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    # відправлення математичного виразу на сервер
    client.send(expression.encode())

    # отримання відповіді від сервера
    response = client.recv(4096).decode()
    # закрити сокетове з'єднання
    client.close()

    # повернути відповідь у json-форматі на клієнтську частину
    return jsonify(result=response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
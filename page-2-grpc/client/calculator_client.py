from flask import Flask, render_template, request, jsonify
import grpc
import calculator_pb2
import calculator_pb2_grpc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form.get('expression')
    if not expression:
        return jsonify({"помилка": "Невідповідний математичний вираз."}), 400

    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            response = stub.Calculate(calculator_pb2.CalculationRequest(expression=expression))

            if response.result:
                return jsonify({"result": response.result})
            else:
                return jsonify({"помилка": "Невідомий результат від сервера."}), 500
    except Exception as e:
        return jsonify({"помилка": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
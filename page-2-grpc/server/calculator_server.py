from concurrent import futures
import grpc
import calculator_pb2
import calculator_pb2_grpc
import math

# клас для обчислення виразу використовуючи згенеровані підсистеми
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Calculate(self, request, context):
        expression = request.expression
        try:
            result = eval(expression) 
        except Exception as e:
            result = f"Помилка: {str(e)}"
        return calculator_pb2.CalculationResponse(result=str(result))

# функція запуску gRPC-сервера
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Сервер запущено, очікування на порті 50051.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

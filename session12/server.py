from concurrent import futures
import grpc
import calculator_pb2
import calculator_pb2_grpc
import math

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Cube(self, request, context):
        """Calculates the cube of a number."""
        number = request.number
        result = math.pow(number, 3)
        if not result.is_integer():
            # This case should ideally not happen with int32 input,
            # but good to handle potential float precision issues if any.
            # Alternatively, raise an error or handle as per specific requirements.
            print(f"Warning: Cubing {number} resulted in a non-integer {result}. Truncating.")
            result = int(result)
        else:
            result = int(result)

        print(f"Received number: {number}, sending cube: {result}")
        return calculator_pb2.NumberResponse(result=result)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:' + port)
    print(f"Server started, listening on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

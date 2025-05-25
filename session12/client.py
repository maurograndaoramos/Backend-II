import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    # NOTE: The server address must match the address the server is listening on.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        # Test with a few numbers
        numbers_to_cube = [2, 3, 5, -4, 0]
        
        for num in numbers_to_cube:
            try:
                request = calculator_pb2.NumberRequest(number=num)
                response = stub.Cube(request)
                print(f"Cube of {num} is {response.result}")
            except grpc.RpcError as e:
                print(f"Error cubing {num}: {e.details()} (status: {e.code()})")
            except Exception as e:
                print(f"An unexpected error occurred while processing {num}: {e}")


if __name__ == '__main__':
    run()

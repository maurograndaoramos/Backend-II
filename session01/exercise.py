from time import perf_counter

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    input_number = input("Enter a number to calculate its factorial: ")
    n = int(input_number)
    start_time = perf_counter()
    result = factorial(n)
    end_time = perf_counter()
    print(f"Factorial of {n} is {result}")
    print(f"Execution time: {end_time - start_time:.6f} seconds")

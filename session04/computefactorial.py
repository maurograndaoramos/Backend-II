import multiprocessing
import time

def factorial(n):
    """Compute the factorial of a number recursively."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def compute_factorial(n):
    """Function to compute factorial and print the result."""
    time.sleep(1)  # Simulate a heavy computation
    result = factorial(n)
    print(f"Factorial of {n} is {result}")

if __name__ == "__main__":
    numbers = [5, 6, 7, 8]
    processes = []
    
    for number in numbers:
        p = multiprocessing.Process(target=compute_factorial, args=(number,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
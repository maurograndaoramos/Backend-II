import multiprocessing
import time

def compute_square(n):
    time.sleep(1)  # Simulate a heavy computation
    print(f"Square of {n} is {n*n}")

if __name__ == "__main__":
    numbers = [2, 3, 4, 5]
    processes = []
    for number in numbers:
        p = multiprocessing.Process(target=compute_square, args=(number,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
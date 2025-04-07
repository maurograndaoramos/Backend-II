from time import perf_counter

def test():
    start = perf_counter()
    for i in range(1000000):
        pass
    end = perf_counter()

    print(f"Execution time: {end - start:.6f} seconds")

if __name__ == "__main__":
    test()
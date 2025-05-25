from time import perf_counter

start = perf_counter()
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1) 

end = perf_counter()
print(f"duration: {(end-start)*1000}ms")


if __name__ == "__main__":
    print(factorial(4))
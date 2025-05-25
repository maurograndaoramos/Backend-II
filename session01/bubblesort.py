from time import perf_counter

n = [3,5,9,7,1,2]

def bubble(n):
    start = perf_counter()
    for i in range(len(n) - 1):
        sorted = True
        for o in range(len(n) - 1):
            if n[o] > n[o + 1]:
                n[o], n[o + 1] = n[o + 1], n[o]
                print("Troca: ", n[o], "com", n[o + 1])
                sorted = False
        if sorted:
            break
    end = perf_counter()
    print(f"Duração do Sort: {(end-start)*1000}ms")
    print("Resultado:", n)


if __name__ == "__main__":
    bubble(n)
from time import perf_counter

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                print(f"Swapped {arr[j]} and {arr[j+1]}: {arr}")
        if not swapped: 
            break

if __name__ == "__main__":
    input_list = input("Enter a list of numbers separated by spaces: ")
    arr = list(map(int, input_list.split()))
    start_time = perf_counter()
    bubble_sort(arr)
    end_time = perf_counter()
    print(f"Sorted list: {arr}")
    print(f"Execution time: {end_time - start_time:.6f} seconds")

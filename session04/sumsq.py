import multiprocessing

def sum_of_squares(numbers):
    """Compute the sum of squares of a list of numbers."""
    return sum(x * x for x in numbers)

if __name__ == "__main__":
    large_list = list(range(1, 1001))

    num_processes = multiprocessing.cpu_count()

    chunk_size = len(large_list) // num_processes
    sublists = [large_list[i:i + chunk_size] for i in range(0, len(large_list), chunk_size)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(sum_of_squares, sublists)

    total_sum_of_squares = sum(results)

    print(f"Total sum of squares from 1 to 1000 is: {total_sum_of_squares}")
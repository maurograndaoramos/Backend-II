import concurrent.futures
import time

print("Lista de compras:")
def process_item(item):
    time.sleep(1)
    return f"Processed {item}"

items = ['item1', 'item2', 'item3', 'item4', 'item5']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_item, item) for item in items]

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        print(result)

print("Example 2 completed!")
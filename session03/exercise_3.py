import threading
import time

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            current = self.count
            time.sleep(0.1)
            self.count = current + 1
            return self.count

def worker(counter, worker_id):
    for _ in range(3):
        value = counter.increment()
        print(f"Worker {worker_id}: counter = {value}")

counter = Counter()

threads = []
for i in range(3):
    thread = threading.Thread(target=worker, args=(counter, i))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final counter value: {counter.count}")
print("Example 3 completed!")
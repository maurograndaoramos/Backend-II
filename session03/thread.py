import threading

def thread_job(number):
    print(f"Started thread for number {number}")
    for x in range(number):
        print(x)
    print(f"Finished thread for number {number}")

if __name__ == "__main__":
    threads = [threading.Thread(target=thread_job, args=(x,)) for x in range(1, 5)]

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
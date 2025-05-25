import logging
import threading
import time
import random

def download_file(file_id):
    """Simulate a long-running file download."""
    logging.info(f"Started downloading file {file_id}")
    download_time = random.randint(3, 7)
    time.sleep(download_time)
    logging.info(f"Finished downloading file {file_id} in {download_time} seconds")

if __name__ == "__main__":
    format = "%(threadName)s-%(asctime)s:%(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    logging.info("Starting the application...")
    
    file_ids = [1, 2, 3, 4, 5]
    
    download_threads = []
    for file_id in file_ids:
        thread = threading.Thread(target=download_file, args=(file_id,))
        logging.info(f"Main  : create and start thread for downloading file {file_id}.")
        download_threads.append(thread)
        thread.start()
    
    for i in range(5):
        logging.info(f"Main thread is doing other work... {i + 1}")
        time.sleep(1)
    
    for index, thread in enumerate(download_threads):
        logging.info(f"Main  : before joining download thread for file {file_ids[index]}.")
        thread.join()
        logging.info(f"Main  : download thread for file {file_ids[index]} done.")
    
    logging.info("Application finished.")
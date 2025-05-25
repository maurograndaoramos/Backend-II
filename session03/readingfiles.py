import logging
import threading
import time
import os

def create_sample_files(file_names):
    """Create sample text files with some content."""
    for file_name in file_names:
        with open(file_name, 'w') as f:
            f.write(f"This is the content of {file_name}.\n")
            f.write("This file is created for testing multithreading file reading.\n")

def read_file(file_name):
    """Read the content of a file and log the process."""
    logging.info(f"Started reading {file_name}")
    time.sleep(1)
    with open(file_name, 'r') as f:
        content = f.read()
    logging.info(f"Finished reading {file_name}. Content:\n{content}")

if __name__ == "__main__":
    format = "%(threadName)s-%(asctime)s:%(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    files = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt",
        "file5.txt"
    ]
    
    create_sample_files(files)
    
    threads = [threading.Thread(target=read_file, args=(file,)) for file in files]

    for index, thread in enumerate(threads):
        logging.info("Main  : create and start thread %d.", index)
        thread.start()
    
    for index, thread in enumerate(threads):
        logging.info("Main  : before joining thread %d.", index)
        thread.join()
        logging.info("Main  : thread %d done", index)

    for file_name in files:
        os.remove(file_name)
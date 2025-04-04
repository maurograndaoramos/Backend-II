import os
from queue import Queue
import threading
import time
from PIL import Image, ImageFilter

import logging


logging.basicConfig(level=logging.DEBUG,format="[%(processName)s-%(threadName)s] - %(message)s")



class ImageProcessor:
    def __init__(self, input_dir,output_dir,num_threads):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.num_threads = num_threads
        self.image_queue = Queue()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def process_image(self):
        while True:
            image_file = self.image_queue.get()
            logging.info(f"got {image_file}")
            if image_file is None:
                self.image_queue.task_done()
                logging.warning("image file var is None. task Done")
                break
            try:
                input_path = os.path.join(self.input_dir, image_file)
                output_path = os.path.join(self.output_dir, image_file)
                with Image.open(input_path) as image:
                    processed = image.convert("L")
                    processed = processed.filter(ImageFilter.GaussianBlur(2))
                    processed = processed.filter(ImageFilter.EDGE_ENHANCE)

                    processed.save(output_path)
                    logging.info(f"new {image_file} in output dir saved!")

            except Exception as e:
                logging.error(e)
            finally:
                self.image_queue.task_done()
    def run(self):
        start = time.perf_counter()
        images = [
            file for file in os.listdir(self.input_dir)
        ]

        if not images:
            raise Exception()


        threads = []
        for thread_id in range(self.num_threads):
            thread = threading.Thread(target=self.process_image)
            thread.daemon = True 
            thread.start()      
            logging.info(f"thread {thread_id} started") 
            threads.append(thread)

        for image in images:
            self.image_queue.put(image)

        for _ in range(self.num_threads):
            self.image_queue.put(None)

        self.image_queue.join()

        for thread in threads:
            thread.join()
            logging.info(f"thread {thread} finished!")

        
        elapsed_time = time.perf_counter() - start
        logging.info(f"program took {elapsed_time}ms")


if __name__ == "__main__":
    processor = ImageProcessor(
        input_dir="/workspaces/backend_ii/multithread_multiprocess/assets",
        output_dir="/workspaces/backend_ii/multithread_multiprocess/result",
        num_threads=4
    )
    processor.run()
        

import requests
import logging
import threading

def fetch_product_data(quantity=1, price_min=0.01, price_max=None, taxes=12, categories_type='uuid'):
    url = f"https://fakerapi.it/api/v2/products?_quantity={quantity}&_price_min={price_min}"
    
    if price_max is not None:
        url += f"&_price_max={price_max}"
    
    url += f"&_taxes={taxes}&_categories_type={categories_type}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def display_products(products):
    if products and products['status'] == 'OK':
        for product in products['data']:
            print(f"Product ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Description: {product['description']}")
            print(f"Price: €{product['price']:.2f}")
            print(f"Net Price: €{product['net_price']:.2f}")
            print(f"Image URL: {product['image']}")
            print("Tags:", ", ".join(product['tags']))
            print("-" * 40)
    else:
        logging.warning("No products found or an error occurred.")

def thread_function(quantity, price_min, price_max, taxes):
    thread_name = threading.current_thread().name
    logging.info(f"{thread_name}: Thread starting to fetch {quantity} products.")
    
    product_data = fetch_product_data(quantity=quantity, price_min=price_min, price_max=price_max, taxes=taxes)
    
    if product_data:
        logging.info(f"{thread_name}: Successfully fetched product data.")
        display_products(product_data)
    else:
        logging.error(f"{thread_name}: Failed to fetch product data.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    threads = []
    num_threads = 5 
    for i in range(num_threads):
        thread = threading.Thread(target=thread_function, args=(1, 10.00, 100.00, 12))
        threads.append(thread)
        logging.info("Main  : create and start thread %d.", i)
        thread.start()
    
    for thread in threads:
        logging.info("Main  : before joining thread %d.", i)
        thread.join()
        logging.info("Main  : thread %d done", i)
    
    logging.info("All threads have completed.")
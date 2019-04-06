import time
import re
import ast
from customer import Customer
from sale import Sale
from sales_man import Salesman
from sale_item import SaleItem
from constants import IN_DIRECTORY, OUT_DIRECTORY
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from concurrent.futures import ThreadPoolExecutor
from operator import itemgetter
from pathlib import Path

salesman_list = []
customer_list = []
executor = ThreadPoolExecutor()

def process_sales(attributes):
    sale_id = attributes[0]
    salesman_name = attributes[2]
    data_list = attributes[1][1:-1].split(',')
    items_list = [SaleItem.from_list(x.split('-')) for x in data_list]
    sale = Sale(sale_id, salesman_name, items_list)
    for salesman in salesman_list:
        if salesman.name == salesman_name:
            salesman.add_sale(sale)
            break


def write_report(path, id_biggest_sale, worst_salesman):
    file_name = Path(path).stem
    output = f'Amount of Clients: {len(customer_list)}\nAmount of Salesman: {len(salesman_list)}\nID of most expensive sale: {id_biggest_sale}\nWorst Salesman ever: {worst_salesman}'
    Path(OUT_DIRECTORY).mkdir(parents=True, exist_ok=True)
    full_output_path = OUT_DIRECTORY + file_name + '.done.dat'
    output_file = open(full_output_path, 'w+')
    output_file.write(output)
    output_file.flush()
    output_file.close()


def generate_results(path):
    worst_salesman = ''
    sale_totals_list = []
    salesman_totals_list = []

    for salesman in salesman_list:
        salesman_total = 0
        for sale in salesman.sales_list:
            sale_total = sum(item.quantity * item.price for item in sale.items_list)
            salesman_total += sale_total
            sale_totals_list.append({'id' : sale.id, 'total' : sale_total})
        
        salesman_totals_list.append({'name' : salesman.name, 'total' : salesman_total})
    
    highest_total = max(sale_totals_list, key=itemgetter('total'))
    id_biggest_sale = highest_total['id']
    lowest_total = min(salesman_totals_list, key=itemgetter('total'))
    worst_salesman = lowest_total['name']

    write_report(path, id_biggest_sale, worst_salesman)


def process_file(path):
    data = open(path, 'r')
    for line in data:
        line = line.replace('\n', '')
        entitys = re.split(r'[ ](?=[0-9])', line)
        for entity in entitys:
            attributes = entity.split('ç')
            if attributes[0] == '001':
                salesman = Salesman.from_list(attributes[1:])
                salesman_list.append(salesman)
            elif attributes[0] == '002':
                customer = Customer.from_list(attributes[1:])
                customer_list.append(customer)
            elif attributes[0] == '003':
                process_sales(attributes[1:])

    generate_results(path)



class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, IN_DIRECTORY, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    patterns = ["*.dat"]

    def on_created(self, event):
        executor.submit(process_file, event.src_path)


if __name__ == '__main__':
    Path(IN_DIRECTORY).mkdir(parents=True, exist_ok=True)
    w = Watcher()
    w.run()
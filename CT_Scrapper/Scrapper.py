import threading
import time
from drivers import *
from utils import *
from concurrent.futures.thread import ThreadPoolExecutor
from registry import RegistryArray
import concurrent


data_registry = RegistryArray()
data_registry = data_registry.getInstance()

driver = driver_0

def scrap_pair(index, origin_name, destination_name, origin_id, destination_id, origin_country, destination_country, USD_RATE):

#    driver = None
    url = f'https://www.rome2rio.com/map/{origin_name} {origin_country}/{destination_name} {destination_country}'

#    driver = driver_0
#    if index % 5 == 0:
#        driver = driver_0
#    if index % 5 == 1:
#        driver = driver_1
#    if index % 5 == 2:
#        driver = driver_2
#    if index % 5 == 3:
#        driver = driver_3
#    if index % 5 == 4:
#        driver = driver_4

    driver.get(url)
    time.sleep(1.5)  # TODO: we need to think if to change that

    # we giving our driver the location of the transportation list in the html page
    rome2rio_transportation_list = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]')

    # this line will take all the 'div' html tags from 'rome2rio_transportation_list' and put them in a list
    rome2rio_transportation_divs_list = rome2rio_transportation_list.find_elements_by_tag_name('div')  # bus,car etc

    # the final output of every pair
    all_data = {'from_id': origin_id,
                'to_id': destination_id,
                'r2r_min_euro_price': None,
                'data': []
                }
    all_prices_list = []


    # iterate route list
    for item in rome2rio_transportation_divs_list:

        current_data = {}
        route, duration, clean_price = None, None, None

        if item.get_attribute('data-test') != None:

            # route: train or bus or flight etc (1)
            route = clean_route_field(item.get_attribute('data-test'))

            # duration (2)
            duration = clean_duration_field(item.find_element_by_class_name('route__duration').text)

            # price (3)
            spans = item.find_elements_by_tag_name('span')
            for span in spans:
                if span.get_attribute('class') == 'route__price tip-west':
                    clean_price = clean_price_field(span.get_attribute('innerHTML'), USD_RATE)
                    break

        if clean_price != None:
            current_data['from_id'] = origin_id
            current_data['from_name'] = origin_name
            current_data['to_id'] = destination_id
            current_data['to_name'] = destination_name
            current_data['transportation_types'] = route
            current_data['duration'] = duration
            current_data['euro_price'] = clean_price
            all_prices_list.append(clean_price)
            current_data['response_page_link'] = url
            current_data['scraping_date'] = get_date()
            print(current_data)
            all_data['data'].append(current_data)
        else:
            continue
    all_data['r2r_min_euro_price'] = min(all_prices_list)
#    data_registry.append_item(all_data)
#    driver.close()


# this will be the main operation
def main_operation(data):
    futures = []
    data_size = len(data)
    USD_RATE = get_current_USD_rate()
    executor = ThreadPoolExecutor(2)
    lock = threading.Lock()

    for index in range(0, data_size):

        # lock.acquire()

        f =  executor.submit(scrap_pair, index, data[index]["from_name"], data[index]["to_name"],
                                 data[index]["from_id"], data[index]["to_id"], data[index]["origin_country"],
                                 data[index]["destination_country"], USD_RATE)
        # lock.release()
        futures.append(f)
    for future in concurrent.futures.as_completed(futures):
        future.result()

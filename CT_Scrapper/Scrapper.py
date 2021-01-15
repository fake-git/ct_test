import threading
import time
from drivers import *
from utils import *
from concurrent.futures.thread import ThreadPoolExecutor


def scrap_pair(index, origin_name, destination_name, origin_id, destination_id, origin_country, destination_country, USD_RATE):

    print(index)
    driver = None
    url = f'https://www.rome2rio.com/map/{origin_name} {origin_country}/{destination_name} {destination_country}'


    if index % 5 == 0:
        driver = driver_0
    if index % 5 == 1:
        driver = driver_1
    if index % 5 == 2:
        driver = driver_2
    if index % 5 == 3:
        driver = driver_3
    if index % 5 == 4:
        driver = driver_4

    driver.get(url)
    time.sleep(1.5)  # TODO: we need to think if to change that
    # lock.acquire()

    # we giving our driver the location of the transportation list in the html page
    rome2rio_transportation_list = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]')

    # this line will take all the 'div' html tags from 'rome2rio_transportation_list' and put them in a list
    rome2rio_transportation_divs_list = rome2rio_transportation_list.find_elements_by_tag_name('div')  # bus,car etc

    all_prices_list = []
    data = {}

    for item in rome2rio_transportation_divs_list:

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
            data['from_id'] = origin_id
            data['from_name'] = origin_name
            data['to_id'] = destination_id
            data['to_name'] = destination_name
            # from_id_r2r = not possible right now
            # from_name_r2r = not possible right now
            # to_id_r2r = not possible right now
            # to_name_r2r = not possible right now
            data['transportation_types'] = route
            data['duration'] = duration
            data['euro_price'] = clean_price
            all_prices_list.append(clean_price)
            # data['route_link'] = not possible right now
            data['response_page_link'] = url
            data['scraping_date'] = get_date()
            print(data)
            # print('\n')
        else:
            continue

    # lock.release()


# this will be the main operation
def main_operation(data):

    data_size = len(data)
    USD_RATE = get_current_USD_rate()
    executor = ThreadPoolExecutor(5)
    lock = threading.Lock()

    for index in range(0, data_size):

        # lock.acquire()

        executor.submit(scrap_pair, index, data[index]["from_name"], data[index]["to_name"],
                                 data[index]["from_id"], data[index]["to_id"], data[index]["origin_country"],
                                 data[index]["destination_country"], USD_RATE)
        # lock.release()



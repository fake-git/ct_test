import datetime
import json
import requests


#
def clean_price_field(price_field, ILS_RATE):

    sub_string = ''
    try:
        for char in price_field:
            if char.isnumeric() or char == '-':
                sub_string = sub_string + char
        unconverted_prices_list = sub_string.split('-')

        prices_list = []

        for price in unconverted_prices_list:
            converted_price = convert_price_to_euro(ILS_RATE, float(price))
            prices_list.append(converted_price)

        return min(prices_list)

    except:
        print("Exception in clean_price_field function")


#
def clean_duration_field(duration_field):
    sub_string = duration_field[4:]
    duration_list = sub_string.split(' ')
    total_minutes = convert_duration_to_minutes(duration_list)
    return total_minutes


#
def clean_route_field(route_field):
    sub_string = route_field[6:]
    route_list = sub_string.split(',')

    for i in range(len(route_list)):
        if route_list[i] == 'flight':
            route_list[i] = 1
        if route_list[i] == 'bus':
            route_list[i] = 2
        if route_list[i] == 'train':
            route_list[i] = 3
        if route_list[i] == 'car':
            route_list[i] = 4
        if route_list[i] == 'taxi':
            route_list[i] = 5
        if route_list[i] == 'walk':
            route_list[i] = 6
        if route_list[i] == 'towncar':
            route_list[i] = 7
        if route_list[i] == 'rideshare':
            route_list[i] = 8
        if route_list[i] == 'shuttle':
            route_list[i] = 9
        if route_list[i] == 'carferry':
            route_list[i] = 10
        if route_list[i] == 'subway':
            route_list[i] = 11
        if route_list[i] == 'tram':
            route_list[i] = 12

    return route_list


#
def convert_price_to_euro(ILS_current_rate, price_in_ILS):
    return "%.0f" % float(price_in_ILS / ILS_current_rate)


#
def convert_duration_to_minutes(duration_list):
    days = 0
    hours = 0
    minutes = 0

    for item in duration_list:
        if 'd' in item:
            days = days + int(item.replace('d', ''))
        if 'h' in item:
            hours = hours + int(item.replace('h', ''))
        if 'm' in item:
            minutes = minutes + int(item.replace('m', ''))

    total_minutes = (days*24*60) + (hours*60) + minutes
    return total_minutes


#
def get_current_USD_rate():

    request = requests.get('http://api.openrates.io/latest')
    data = json.loads(request.content)
    current_USD_rate = float(data['rates']['USD'])
    return current_USD_rate


#
def get_date():
    # year / month / day
    current_date = datetime.datetime.now()
    return f'{current_date.strftime("%Y")}{current_date.strftime("%m")}{current_date.strftime("%d")}'


# this function will get path(string) to json file and convert it to dictionary
def get_data(json_path):
    json_file = open(json_path)
    data = json_file.read()
    converted_data = json.loads(data)
    return converted_data
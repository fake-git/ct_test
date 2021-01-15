from utils import *
from Scrapper import main_operation

# from here we will run the program (threads)

if __name__ == "__main__":

    data = get_data("Input/usa_and_canada.json")
    main_operation(data)

    # TODO: (2) save to json
    # TODO: (4) make sure that there isn't problem with the threads and json saving

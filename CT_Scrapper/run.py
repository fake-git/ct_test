from utils import *
from Scrapper import main_operation
from registry import RegistryArray

# from here we will run the program (threads)

if __name__ == "__main__":

    # start the scrapping
    data_to_scrap = get_data("Input/usa_and_canada.json")
    main_operation(data_to_scrap)


    # import the data instance
    data_registry = RegistryArray()
    data_registry = data_registry.getInstance()


    # save the data on json file
    new_json_file = open('Data/test.json', 'a')
    final_data = json.dumps(data_registry.get_items())
    new_json_file.write(final_data)
    new_json_file.close()



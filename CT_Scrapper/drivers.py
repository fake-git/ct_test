from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# all the drivers path will be here


# drivers path
driver_path_0 = "Drivers/chromedriver0"
driver_path_1 = "Drivers/chromedriver1"
driver_path_2 = "Drivers/chromedriver2"
driver_path_3 = "Drivers/chromedriver3"
driver_path_4 = "Drivers/chromedriver4"


# set selenium browser without UI
options = Options()
options.headless = True


# drivers
driver_0 = webdriver.Chrome(executable_path=driver_path_0, chrome_options=options)
driver_1 = webdriver.Chrome(executable_path=driver_path_1, chrome_options=options)
driver_2 = webdriver.Chrome(executable_path=driver_path_2, chrome_options=options)
driver_3 = webdriver.Chrome(executable_path=driver_path_3, chrome_options=options)
driver_4 = webdriver.Chrome(executable_path=driver_path_4, chrome_options=options)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import *
from time import sleep
import pandas as pd

class RaceCalc:
    def __init__(self):
        self.main_horse = input("Enter the horse you want to race with: ")

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
        self.main_horse_data = self.get_horse_data(self.main_horse)
    
    def get_horse_data(self, name):
        self.driver.get(HAWKU_LINK)

        search_bar = self.driver.find_element(by=By.ID, value="query")
        search_bar.click()
        search_bar.send_keys(name + Keys.ENTER)

        sleep(2)

        self.driver.find_element(by=By.CSS_SELECTOR, value=".p-2 div h3").click()

        sleep(2)

        graphs = self.driver.find_elements(by=By.CSS_SELECTOR, value=".p-2 .w-full .shadow .line .w-full")[:9]
        headers = self.driver.find_elements(by=By.CSS_SELECTOR, value=".p-2 .w-full .shadow h2")[:9]

        performance_dict = {}

        for i in range(len(graphs)):
            length = int(headers[i].text[:4])
            record = graphs[i].text.strip().split("\n")[:3]
            races = int(headers[i].text[5:].strip().split(" ")[3])
            record = [round(float(num) / races, 4)  for num in record]
            record.append(sum(record))
            record.append(int(races))
            performance_dict[length] = pd.Series(record, index=["1st", "2nd", "3rd", "Win Rate", "Num"])

        self.driver.quit()

        data = pd.DataFrame(performance_dict)
        return data
    
    def test(self):
        print(self.main_horse_data)


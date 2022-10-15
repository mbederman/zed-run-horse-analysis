from selenium import webdriver
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

target_horse = input("Enter the name of a horse: ")

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
driver.get(HAWKU_LINK)

search_bar = driver.find_element(by=By.ID, value="query")
search_bar.click()
search_bar.send_keys(target_horse + Keys.ENTER)

sleep(3)

driver.find_element(by=By.CSS_SELECTOR, value=".p-2 div h3").click()

sleep(2)

graphs = driver.find_elements(by=By.CSS_SELECTOR, value=".p-2 .w-full .shadow .line .w-full")[:9]
headers = driver.find_elements(by=By.CSS_SELECTOR, value=".p-2 .w-full .shadow h2")[:9]

performance_dict = {}

for i in range(len(graphs)):
    length = int(headers[i].text[:4])
    record = graphs[i].text.strip().split("\n")[:3]
    races = int(headers[i].text[5:].strip().split(" ")[3])
    record = [round(float(num) / races, 4)  for num in record]
    record.append(sum(record))
    record.append(int(races))
    performance_dict[length] = pd.Series(record, index=["1st", "2nd", "3rd", "Win Rate", "Num"])

driver.quit()

data = pd.DataFrame(performance_dict)

print(data)

choice = input("Would you like to calculate expected profits? Enter 'N' to stop. ")

if not choice == "N":
    race_type = int(input("Enter length of race: "))
    cost = float(input("Enter cost of race: "))
    prize_1 = float(input("Enter first place price: "))
    prize_2 = float(input("Enter second place price: "))
    prize_3 = float(input("Enter third place price: "))

    total_cost = NUM_RACES * cost
    expected_revenue = prize_1 * data[race_type][0] + prize_2 * data[race_type][1] + prize_3 * data[race_type][2]
    expected_revenue *= NUM_RACES

    expected_profit = expected_revenue - total_cost

    print(f"\nTotal cost for {NUM_RACES} races: ${round(total_cost, 2)}")
    print(f"Expected revenue for {NUM_RACES} races: ${round(expected_revenue, 2)}\n")
    print(f"Expected profit for {NUM_RACES} races: ${round(expected_profit, 2)}")

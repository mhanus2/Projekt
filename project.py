from sqlite3 import enable_shared_cache
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime
import mysql.connector
import sqlite3
import csv
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ["enable-logging"])
s = Service('C:/Users/marta/Project/drivers/chromedriver.exe')

today = datetime.today()
today_format = today.strftime("%m/%d/%Y %H:%M:%S")
search_query = 'https://contextures.com/xlsampledata01.html#data'
driver = webdriver.Chrome(service=s, options=options)
driver.get(search_query)

driver.maximize_window()

order_date = driver.find_elements(By.XPATH,"//table/tbody/tr/td[1]")
region = driver.find_elements(By.XPATH,"//table/tbody/tr/td[2]")
rep = driver.find_elements(By.XPATH,"//table/tbody/tr/td[3]")
item = driver.find_elements(By.XPATH,"//table/tbody/tr/td[4]")
units = driver.find_elements(By.XPATH,"//table/tbody/tr/td[5]")
unitcost = driver.find_elements(By.XPATH,"//table/tbody/tr/td[6]")
total = driver.find_elements(By.XPATH,"//table/tbody/tr/td[7]")
total_discout = []
final_price = []
creation_date = []

order_date_final = []
region_final = []
rep_final = []
item_final = []
units_final = []
unitcost_final = []
total_final = []

for i in range(1,len(order_date)):
    if region[i].text == "Central":
        b = 0.23 * int(units[i].text)
    elif region[i].text == "East" and int(units[i].text) > 50:
        b = (0.12 * int(units[i].text)) + 7.2
    else:
        b = 0.12 * int(units[i].text)
    order_date_format = datetime.strptime((order_date[i].text),'%m/%d/%Y')
    region_final.append(region[i].text)
    rep_final.append(rep[i].text) 
    item_final.append(item[i].text)
    units_final.append(units[i].text) 
    total_discout.append(round(b,2))
    final_price.append(round(float((total[i].text).replace(",","")) - b,2))
    creation_date.append(today_format)
    order_date_final.append(order_date_format.strftime("%m/%d/%Y"))

dict = {'Region': region_final, 'Rep': rep_final, 'Item': item_final, 'Units': units_final,
'Total discount': total_discout,'Final Price':final_price,'Creation date':creation_date,'OrderDate': order_date_final}  

df = pd.DataFrame(dict) 

# df.to_csv('orders_file.csv') 

# connection = sqlite3.connect('orders.db')
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE order_pokus (Region,Rep,Item,Units,'Total discount','Final Price','Creation date',OrderDate);")

# with open('orders_file.csv','r') as fin:
#     dr = csv.DictReader(fin)
#     to_db = [(i['Region'], i['Rep'],i['Item'],i['Units'],i['Total discount'],i['Final Price']
#     ,i['Creation date'],i['OrderDate']) for i in dr]

# cursor.executemany("INSERT INTO order_pokus (Region,Rep,Item,Units,'Total discount','Final Price','Creation date',OrderDate) VALUES (?, ?,?,?,?,?,?,?);", to_db)
# connection.commit()
# connection.close()
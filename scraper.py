#!/usr/bin/env python
# coding: utf-8

import requests
import csv
from bs4 import BeautifulSoup
import re

def price_calc(price):
    prc = price.split(" ")
    result = ''
    if len(prc) > 1 or price == " حواله ":
        result = 0
    else:
        result = re.sub(",","",price)
    return int(result)
    

def generate(html):

    try:
        soup = BeautifulSoup(str(html),"html.parser")
        div = soup.find("div", attrs={"class":"title"})
        title = re.split("\|", div.text.strip())
        name = title[0]
        model = re.sub(r"\u200f","",title[1])
        price = soup.find(attrs={"itemprop":"price"})
        price = price_calc(price.text.strip())
        funcs = soup.find("div",attrs={"class":"car-func-details"})
        funcs = re.split(r"\|",funcs.text.strip())
        wrk = re.split(" ",funcs[0])[1].strip()
        color = funcs[1].strip()
        rep = funcs[2].strip()
        gear = funcs[3].strip()
        ready = [name, model, wrk, color, rep, gear, price]
        ready = map(lambda x: re.sub("\u06cc", "ي", str(x)),ready)
        with open("data.csv",'a' , newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list(ready))
    except:
        print("Wrong format")

def main(link):
    req = requests.get(link)
    print(req.status_code)
    soup = BeautifulSoup(req.text, 'html.parser')
    lst = soup.find_all("li", attrs={"class":"car-list-item-li"})
    for i in lst:
        generate(i)
 

link = "https://bama.ir/car/all-brands/all-models/all-trims?manucountryid=9&page="
pages = 200
for i in range(1,pages+1):
    main(link+str(i))
input("Process Ended successfully")

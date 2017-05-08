#!/usr/bin/python3

'''
Author: Adam Frederik Ingwersen Linnemann
Date: March, 2017

This module intends to keep the fixed parts of the webcrawlers built seperate from the moving parts.

Why?
    1) Consistency
    2) Error-avoidance
    3) Readability
    4) Replication

Big Dollar Data Cloud ftw
'''

### Import libraries
import json, time, re
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


### Regular expression for pattern matching on strings: 
regx_numeric = re.compile('([0-9].*?(?=[\s]))')
regx_numeric_simple = re.compile('[0-9]*')
regx_numeric_d = re.compile('\d+')
regx_price = re.compile('([0-9]{2}.*(?=[\s]))')
regx_left = re.compile('(^.*?(?=[\n]))')
regx_right = re.compile('(?<=[\n]).*')
regx_gb = re.compile('(\n[0-9].*[\sGB])')
regx_name = re.compile('(^.*?(?=[\n]))')
regx_gb_lookbehind = re.compile('(.*?(?=[data]))')

### Regex for splitting html by tags:
regx_br = re.compile(r'<br>')
regx_p = re.compile(r'.*?(?=[</p>]|[<p>])')

### Utilize the numeric regex from TWU and cast string to int:
def cast_numeric(text):
    try:
        return(float(regx_numeric_d.search(text).group()))
    except ValueError:
        return(0)

### Define a driver object to be used for dynamic javascript rendering (does pretty much what it says)
def init_driver(): 
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
    driver.wait = WebDriverWait(driver, 10) 
    driver.maximize_window()
    return(driver)

# Create json-dict, print to console and insert into predefined collection (this is done for each script atm)
def dbInsert(mongoCollection, name, gb, price, talk, min_price, des, vas, brand_name, domain, vas_list):
    json = {"product_name"  : name,
            "gb_included"   : gb,
            "talk_included" : talk,
            "vas_included"  : vas,
            "sub_price"     : price,
            "min_price"     : min_price,
            "description"   : des,
            "provider"      : brand_name,
            "domain"        : domain,
            "vas_wildcard"  : vas_list,
            "timestamp"     : datetime.now().strftime('%Y-%m-%d %H:%M:%S')}    
    print(json)        
    mongoCollection.insert_one(json).inserted_id


### Sanity checking the number of subscriptions:
def checkBrand(html, _subscription_count, extra):    
    if((len(html) + extra) < _subscription_count): 
        print("\nOBS: Does ", brand_name,  " have less than", str(_subscription_count), " mobilephone products?")
    else: 
        print("\nSucces!") 



import os
import time
import pickle
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from utils import make_pickle, check_num


# set url, find driver and instantiate selenium
url_to_parse = "https://runtime.fivem.net/doc/natives/"
driver = str(os.getcwd()) + "\\bin\\chromedriver.exe"
browser = webdriver.Chrome(driver)
browser.get(url_to_parse)

# Give time to render
time.sleep(2)


def ScrollAndParse():
    # First get current html, parse and find all native entry divs
    soup = BeautifulSoup(browser.page_source, features="html.parser")
    divs = soup.find_all('div', {"class": "native entry"})
    # Get the last id obtained
    last_id = divs[-1].get('id')
    new_id = False
    # Remove parenthesis from strings
    natives = [re.sub("\((.*?)\)", "", div.getText())
               for div in divs]
    hasEnded = False
    ScrollPause = 0.6
    while not hasEnded:
        # find last element and scroll into view
        last_el = browser.find_element(By.ID, last_id)
        ActionChains(browser).move_to_element(last_el).perform()
        time.sleep(ScrollPause)
        # Parse html and find native entrys
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        divs = soup.find_all('div', {"class": "native entry"})
        # Store new_id and add new functions to natives list
        new_id = divs[-1].get('id')
        for div in divs:
            func = re.sub("\((.*?)\)", "", div.getText())
            # if the function starts with 0 it's not probably documented
            if not func.startswith("0"):
                if func not in natives:
                    natives.append(func)
                    #hasEnded = True
        if not (last_id == new_id):
            last_id = new_id
            continue
        else:
            hasEnded = True
    make_pickle(list, "natives.pckl")
    return natives


def pretty(list):
    final_str = ""
    for line in list:
        if line.startswith("_"):
            to_clean = line.replace("_", "")
            lower = to_clean.lower()
            splt = lower.split("_")
            upper = "".join([c.capitalize() for c in splt])
            final_str = final_str + "'{}'".format(upper) + ", "
        else:
            lower = line.lower()
            splt = lower.split("_")
            upper = "".join([c.capitalize() for c in splt])
            final_str = final_str + "'{}'".format(upper) + ", "
    with open("natives.log", "w") as f:
        f.write(final_str)
    make_pickle(final_str, "pretty_natives.pckl")
    return final_str


try:
    print("Starting")
    pretty(ScrollAndParse())
    print("Done")
except Exception as e:
    print(e)
    browser.quit()

browser.quit()

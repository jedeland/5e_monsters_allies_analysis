import pandas as pd; import numpy as np;
import requests; import os.path; import re
from bs4 import BeautifulSoup
'''
This section of the monster analysis pack focused on using the NLTK (or similar tools) to analyse
The text found inside of the monsters know, a website dedicated to monster tactics http://themonstersknow.com/
This can be done by using beautiful soup to scrape information from each article
'''

def read_blogs():
    page_urls = ["cr-1-4", "cr-1-2"]
    url_list, entry_dict = [], {} #list will be passed to another function to read sub pages
    for i in range(21):
        page_urls.append("cr-{}".format(i+1)) #Automating target pages
    print(page_urls)

    for i in range(len(page_urls)-15): #Is currently set to the first 6 entries for speed
        address = "http://themonstersknow.com/tag/{}/".format(page_urls[i])
        file = requests.get(address)
        print(address)
        soup = BeautifulSoup(file.content, "html.parser")
        read_data = soup.find_all("div", class_="entry-content")
        #Needs to follow link found in <a > tag, so that complete page is shown
        b = 0 #Local Iterator
        for item in read_data:
            b = b + 1; x = b
            print(x, item.get_text(), "\n ", item.a)
            if item.a is None:
                entry_dict[str(item.strong.text)] =  str(item.get_text()) #This should make keys and values that work without the need to manually assign them

            elif item.a is not None:
                print(item.a.get("href"))
                if "http://" not in item.a.get("href"):
                    pass
                else:
                    url_list.append(item.a.get("href"))
    print("Reading sub lists")
    url_list, entry_dict = read_sublinks(url_list, entry_dict)

    url_list = list(dict.fromkeys(url_list))
    print("Testing: {}".format(url_list), "\n ")
    print("formed dictionary of articles ", entry_dict.keys())
    data = {"Article": [entry_dict.keys()], "Text": [entry_dict.values()]}
    print(entry_dict.values())
    df_mk = pd.DataFrame.from_dict(data)
    print(df_mk)


def read_sublinks(func_list, entry_dict):
    for link in func_list:
        print(link)
        if "themonstersknow" in link:
            print("valid url")
            file = requests.get(link)
            soup = BeautifulSoup(file.content, "html.parser")
            title = soup.find("h1", class_="entry-title")
            print(title.string)
            read_data = soup.find_all("div", class_="entry-content")
            for item in read_data:
                entry_dict[title.string] = item.get_text()
        else:
            print("invalid url")
            pass
    return func_list, entry_dict









read_blogs()
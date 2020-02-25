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
    for i in range(21):
        page_urls.append("cr-{}".format(i+1))
    print(page_urls)

    for i in range(len(page_urls)-15): #Is currently set to the first 6 entries for levities sake
        address = "http://themonstersknow.com/tag/{}/".format(page_urls[i])
        file = requests.get(address)
        print(address)
        soup = BeautifulSoup(file.content, "html.parser")
        read_data = soup.find_all("div", class_="entry-content")
        #Needs to follow link found in <a > tag, so that complete page is shown
        b = 0 #Crude Iterator
        for item in read_data:
            b = b + 1
            x = b
            #print(x, item.p, "\n", item.a)
            if item.a is not None:
                print(item.a.get("href"))







read_blogs()
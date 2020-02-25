import pandas as pd; import numpy as np;
import requests; import os.path
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

    for i in range(len(page_urls)):
        address = "http://themonstersknow.com/tag/{}/".format(page_urls[i])
        file = requests.get(address)
        print(address)
        soup = BeautifulSoup(file.content, "html.parser")
        read_data = soup.find_all("div", class_="entry-content")
        print(read_data)
        for item in read_data:
            print(item)



read_blogs()
import pandas as pd; import numpy as np;
import requests; import os.path; import re
import tensorflow as tf
from bs4 import BeautifulSoup
'''
This section of the monster analysis pack focused on using the NLTK (or similar tools) to analyse
The text found inside of the monsters know, a website dedicated to monster tactics http://themonstersknow.com/
This can be done by using beautiful soup to scrape information from each article, forming a dataframe containing said information
And pushing that through a machine learning function
'''
#https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1

def summarise_data(df):
    print("Starting up the machine learning, this should either be done by scrapping the site using beautiful soup, or via an SQL or CSV file that has been printed to and read from")
    df_targ = df.loc[df["article_id"] == "Angel Tactics"] #Test case using one article, future case will use for loop and iteration, reminder https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    article = str(df_targ["text"].values)
    pretty_article = article
    print(pretty_article, type(pretty_article))#Not perfect but better and more readable
    sections = article.split(".Next: ")
    print(sections[1])
    text = str(sections[0])

    #Line divides the article in two, removing the "share, save ect ect" part

def read_blogs():
    page_urls = ["cr-1-4", "cr-1-2"]
    print("Reading blogs this may take a while.")
    url_list, entry_dict = [], {} #list will be passed to another function to read sub pages
    for i in range(21):
        page_urls.append("cr-{}".format(i+1)) #Automating target pages
    print(page_urls)

    for i in range(len(page_urls)): #Is currently set to the first 6 entries for speed
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
                text_entry = item.get_text()
                text_entry = text_entry.replace("\n", "")
                entry_dict[str(item.strong.text)] =  text_entry #This should make keys and values that work without the need to manually assign them

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
    df = form_df(entry_dict)
    summarise_data(df)


def form_df(entry_dict):
    df_mk = pd.DataFrame(columns=["article_id", "text"])
    for k, v in sorted (entry_dict.items()):
        print(k, "is the key for: ", v)
        df_mk = df_mk.append({"article_id": k, "text": v}, ignore_index=True)
    print(df_mk)
    return df_mk


def read_sublinks(func_list, entry_dict):
    print("Reading blogs in detail, this may take a while.")
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
                text_entry = item.get_text()
                text_entry = text_entry.replace("\n", "")
                entry_dict[title.string] = text_entry
        else:
            print("invalid url")
            pass
    return func_list, entry_dict









read_blogs()
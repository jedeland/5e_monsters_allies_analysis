from __future__ import absolute_import, division, print_function
import pandas as pd; import numpy as np; from sqlalchemy import create_engine, sql
import requests; import os.path;
import nltk as nltk
from nltk.corpus import stopwords; from nltk.cluster.util import cosine_distance; from nltk import pos_tag
import networkx as nx
from bs4 import BeautifulSoup
'''
This section of the monster analysis pack focused on using the NLTK (or similar tools) to analyse
The text found inside of the monsters know, a website dedicated to monster tactics http://themonstersknow.com/
This can be done by using beautiful soup to scrape information from each article, forming a dataframe containing said information
And pushing that through a machine learning function
'''



#The below function references the following article, which is being used as a basis for the implementation for NLTK usage
#The below functions relate to the NLTK ML library
#Future development should focus on summarizing particular paragraphs as articles are usually split up into seperate monsters that are related to the over all type
#https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
def read_article(text):
    print("Reading : {}".format(text))
    article = text.split(". ")
    sentence_lst = []
    for sentence in article:
        print(sentence)
        sentence_lst.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentence_lst.pop()
    return sentence_lst

def gen_summary(article, top_n):
    #Future development should look into using sentiment to guide output, find here http://www.nltk.org/howto/sentiment.html
    stop_words = stopwords.words("english")
    summarize_text = []
    #Tokenize text
    sentences = read_article(article)
    find_names(article, sentences)

    sentence_sim_matrix = find_similarities(sentences, stop_words)
    #Rank sentences
    sentence_sim_graph = nx.from_numpy_array(sentence_sim_matrix)
    scores = nx.pagerank(sentence_sim_graph)
    #Sort rank, pick top
    rank_sentence = sorted(((scores[i],s) for i, s in
                            enumerate(sentences)), reverse=True)
    #print("Indexes of top ranked_sentence order are :",rank_sentence)
    for i in range(top_n):
        summarize_text.append(" ".join(rank_sentence[i][1]))
    print("Summarize Text: \n", ". ".join(summarize_text))


def find_names(article, sentences):
    #Find names using chunking lable, using information from http://www.nltk.org/howto/chunk.html
    sent_names = sentences
    sent_names = nltk.sent_tokenize(article)
    sent_names = [nltk.word_tokenize(sent) for sent in sent_names]
    sent_names = [nltk.pos_tag(sent) for sent in sent_names]
    print(sent_names)
    names = []
    for tagged_sents in sent_names:
        for chunk in nltk.ne_chunk(tagged_sents):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == "PERSON":
                    names.append(' '.join([n[0] for n in chunk]))
    print(names)


def find_similarities(sents, stop_words):
    similarity_matrix = np.zeros((len(sents), len(sents)))
    for sent_id_1 in range(len(sents)):
        for sent_id_2 in range(len(sents)):
            if sent_id_1 == sent_id_2:
                continue
            similarity_matrix[sent_id_1] [sent_id_2] = sentence_similarity(sents[sent_id_1], sents[sent_id_2], stop_words)

    return similarity_matrix


def sentence_similarity(sent_id_1, sent_id_2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent_id_1 = [c.lower for c in sent_id_1]
    sent_id_2 = [c.lower for c in sent_id_2]
    all_words = list(set(sent_id_1 + sent_id_2))
    vec1 = [0] * len(all_words)
    vec2 = [0] * len(all_words)
    #create vector for first sentance
    for w in sent_id_1:
        if w in stopwords:
            continue
        vec1[all_words.index(w)] += 1
    #create vector for second sentance
    for i in sent_id_2:
        if i in stopwords:
            continue
        vec2[all_words.index(i)] += 1

    return 1 - cosine_distance(vec1, vec2)


#The below functions relate to reading and assigning articles to different sections
def read_blogs():
    if os.path.exists("articles.xlsx"):
        print("Using preexisting excell sheet instead")
        df = pd.read_excel("articles.xlsx", index_col=0)
        print(df)
        for i in range(5):
            print("*")
        clean_data(df)
    else:
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
        clean_data(df)


def clean_data(df):
    print("Starting up the machine learning, this should either be done by scrapping the site using beautiful soup, or via an SQL or CSV file that has been printed to and read from")
    df_targ = df.loc[df["article_id"] == "Angel Tactics"] #Test case using one article, future case will use for loop and iteration, reminder https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    article = str(df_targ["text"].values)
    sections = article.split(".Next: ")
    text = str(sections[0])
    sent_list = read_article(text)
    num_sum = round(len(sent_list) * .20)

    #read_article(text)
    gen_summary(text, num_sum)

def form_df(entry_dict):
    df_mk = pd.DataFrame(columns=["article_id", "text"])
    for k, v in sorted (entry_dict.items()):
        print(k, "is the key for: ", v)
        df_mk = df_mk.append({"article_id": k, "text": v}, ignore_index=True)
    form_sql(df_mk)
    df_mk.to_excel("articles.xlsx", sheet_name="monstersknow")
    return df_mk


def form_sql(df_mk):
    print(df_mk)
    eng = create_engine('sqlite://', echo=False)
    df_mk.to_sql("articles", con=eng)
    eng.execute("SELECT * FROM articles").fetchall()


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
import pandas as pd; import numpy as np; import urllib.request; import sqlite3 as lite; import sqlalchemy as sql
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so


loc = "datasets/kfc_monsters.xlsx"
df_file = pd.read_excel(loc)
print(df_file.head())
checker = "\n *** \n Testing \n *** \n"

def data_tranformation():
    df_csv = pd.read_excel(loc)
    df_csv.to_csv("kfc_monstercopy.csv", index=False)
    #CSV files are easier to parse through, using resources available to me
    print(df_csv.head())


def csv_cleaning():
    #This function should clean the database and create a cleaned copy
    #The cleaned copy will focus on monsters from the core books, to limit the scope
    try:
        data_tranformation()
        csv_unclean = pd.read_csv("kfc_monstercopy.csv")
        df = csv_unclean.fillna("Missing data") #Replace any null values
        df.columns = df.columns.str.replace("?", "")
        df.columns = df.columns.str.replace(" ", "")
        #Replace any white spaces in column names and any non letters / numbers



        print(list(df), df)
        print(checker)
    except:
        print("an error occured")



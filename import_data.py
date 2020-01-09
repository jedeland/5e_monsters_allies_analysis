import pandas as pd; import numpy as np; import urllib.request
import sqlite3 as lite; import sqlalchemy as sql; import string
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

#Move these options to interface in future
pd.set_option('display.max_columns', None)


loc = "kfc_monsters.xlsx"
df_file = pd.read_excel(loc)
#print(df_file.head())
checker = "\n *** \n Testing \n *** \n"

def data_tranformation():
    df_csv = pd.read_excel(loc)
    df_csv.to_csv("kfc_monstercopy.csv", index=False)
    #CSV files are easier to parse through, using resources available to me



def csv_cleaner():
    #This function should clean the database and create a cleaned copy
    #The cleaned copy will focus on monsters from the core books, to limit the scope
    try:
        data_tranformation()
        csv_unclean = pd.read_csv("kfc_monstercopy.csv")
        df = pd.DataFrame(csv_unclean)
        df = df.fillna(0) #Replace any null values
        df.columns = df.columns.str.replace("?", "")
        df.columns = df.columns.str.replace(" ", "")
        #Replace any white spaces in column names and question marks
        newcolumn = refine_sources(df)
        #print(newcolumn)
        df["smallsrc"] = newcolumn["sources"]
        df = df.drop("sources", axis=1)
        df = df.dropna()

        print(df)
        return df

    except:
        print("an error occured")



def refine_sources(df):
    # Creating new column for page number
    splitcolumn = df["sources"].str.split(": ", n=1, expand=True)
    # print("Trying to output new column \n", splitcolumn, list(splitcolumn))
    clean_refined_sources(df, splitcolumn)
    #print(list(df), df)
    select_sources = df["sources"].values
    select_sources = df.loc[df["sources"].values == 'monstermanual']
    adder = df.loc[df["sources"].values == 'volosguidetomonsters']
    #Implement Mordakiens tomb of foes if data is accessable
    select_sources = select_sources.append(adder)
    #print(checker, selectsources["sources"])
    return select_sources


def clean_refined_sources(df, splitcolumn):
    #This function cleans the sources and name columns, and splits the source column into two
    #Seperate columns, namely the pagenumber and source columns (using a delimiter)
    df["pagenum"], df["sources"] = splitcolumn[1], splitcolumn[0]
    df["sources"] = df["sources"].str.replace(" ", "")
    df["sources"] = df["sources"].str.replace("[^\w\s]", "")
    df["name"] = df["name"].str.replace(" ", "-")
    df["name"] = df["name"].str.replace("[^\w-]", "")
    df["sources"], df["name"] = [x.lower() for x in df["sources"]], [y.lower() for y in df["name"]]
    #Fixes issue with CR being converted to dates, should add preconditions in future
    df.loc[df["cr"].values == "2017-01-02 00:00:00", "cr"] = "0.5" #Typed as 1/2 CR
    df.loc[df["cr"].values == "2017-01-04 00:00:00", "cr"] = "0.25" #Typed as 1/4 CR
    df.loc[df["cr"].values == "2017-01-08 00:00:00", "cr"] = "0.125" #Typed as 1/8 CR
    df["cr"] = df["cr"].apply(pd.to_numeric)
    #print(df["cr"].unique())
    #print(df.loc[df["cr"] == "1/2"])





csv_cleaner()


import pandas as pd; import numpy as np; import urllib.request; import sqlite3 as lite; import sqlalchemy as sql
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

#Move these options to interface in future
pd.set_option('display.max_columns', None)


loc = "datasets/kfc_monsters.xlsx"
df_file = pd.read_excel(loc)
print(df_file.head())
checker = "\n *** \n Testing \n *** \n"

def data_tranformation():
    df_csv = pd.read_excel(loc)
    df_csv.to_csv("kfc_monstercopy.csv", index=False)
    #CSV files are easier to parse through, using resources available to me



def csv_cleaning():
    #This function should clean the database and create a cleaned copy
    #The cleaned copy will focus on monsters from the core books, to limit the scope
    try:
        data_tranformation()
        csv_unclean = pd.read_csv("kfc_monstercopy.csv")
        df = pd.DataFrame(csv_unclean)
        df = df.fillna(0) #Replace any null values
        #print(df.head())
        df.columns = df.columns.str.replace("?", "")
        df.columns = df.columns.str.replace(" ", "")
        #Replace any white spaces in column names and question marks
        newcolumn = refine_sources(df)
    except:
        print("an error occured")


def refine_sources(df):
    # Creating new column for page number
    splitcolumn = df["sources"].str.split(": ", n=1, expand=True)
    # print("Trying to output new column \n", splitcolumn, list(splitcolumn))
    df["pagenum"], df["sources"] = splitcolumn[1], splitcolumn[0]
    df["sources"] = df["sources"].str.replace(" ", "")
    df["sources"] = df["sources"].str.replace("[^\w\s]", "")
    df["sources"] = [x.lower() for x in df["sources"]]
    print(list(df), df)
    selectsources = df["sources"].values
    sourcenames = df["sources"].unique()
    print(sourcenames)
    selectsources = df.loc[df["sources"].values == 'monstermanual']
    adder = df.loc[df["sources"].values == 'volosguidetomonsters']
    #Implement Mordakiens tomb of foes if data is accessable
    selectsources = selectsources.append(adder)
    print(checker, selectsources["sources"])
    return selectsources


csv_cleaning()


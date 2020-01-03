import pandas as pd; import numpy as np; import urllib.request; import sqlite3 as lite; import sqlalchemy as sql
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so


loc = "datasets/kfc_monsters.xlsx"
df_file = pd.read_excel(loc)
print(df_file.head())
checker = "\n *** \n Testing \n *** \n"

def data_tranformation():
    df_sql = pd.read_excel(loc)
    db_filename = r"mydb.db"
    con = lite.connect(db_filename)
    df_sql.to_sql("mytable", con, if_exists="replace", index=True)

    print(df_sql.head())

def sql_cleaning():
    #This function should clean the database and create a cleaned copy
    #The cleaned copy will focus on monsters from the core books, to limit the scope
    try:
        db_name = r"venv/mydb.db"
        con = lite.connect(db_name)
        print(checker)
        df_sqlread = pd.read_sql("mytable")
    except:
        print("an error occured")


sql_cleaning()




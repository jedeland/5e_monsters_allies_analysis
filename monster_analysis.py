import pandas as pd; import numpy as np;
import sqlalchemy as sql; import string; import import_data
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

'''
This section focuses on extrapolating data from the selected monster sources, using different functions,
those being the monster manual and volos guide to monsters, with an intention to add MTF later
'''

checker = "\n *** \n Testing \n *** \n"

def find_average():
    df_copy = import_data.csv_cleaning()
    print(checker, df_copy)

def iqr_monster_cr():
    df_copy = import_data.csv_cleaning()
    meancr = df_copy["cr"]
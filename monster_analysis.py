import pandas as pd; import numpy as np;
import sqlalchemy as sql; import string; import import_data
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

'''
This section focuses on extrapolating data from the selected monster sources, using different functions,
those being the monster manual and volos guide to monsters, with an intention to add MTF later
'''

checker = "\n *** \n Testing \n *** \n"
divider = "\n***\n***"
question = "Type 1 for yes, or 2 for no"

def find_average_cr():
    #Finds average CR, may need to convert CR column to int/double for this
    df_copy = import_data.csv_cleaner()
    print(checker, df_copy)
    print("The mean value of the challenge rating is {0:.1f}".format(df_copy["cr"].mean()), divider)
    print("The mode value of the challenge rating is {0:.1f}".format(int(df_copy["cr"].mode())))
def find_quantile_cr():
    #Finds the average CR of each quantile, and outputs a CR average that fits into the "normal" range
    #Aka, between .25 and .75
    df_copy = import_data.csv_cleaner()
    print(checker)
    print("The first quantile of the CR is {}".format(df_copy["cr"].quantile(.25)),
          "The second quantile of the CR is {}".format(df_copy["cr"].quantile(.50)),
          "The third quantile of the CR is {}".format(df_copy["cr"].quantile(.75)))

def iqr_monster_cr():
    df_copy = import_data.csv_cleaner()
    print(checker)
    #Set the quantile groups
    early_monsters = df_copy["cr"].quantile(.25)
    later_monsters = df_copy["cr"].quantile(.75)
    iqr_enemies = later_monsters-early_monsters #Changed name to enemies to avoid confusion with method
    top_range_monsters = later_monsters + iqr_enemies * 1.5 #9+8*1.5
    low_range_monsters = early_monsters - iqr_enemies * 1.5 #1-8*1.5
    df_iqr = df_copy
    df_iqr = df_iqr.drop(df_iqr[df_iqr["cr"] > top_range_monsters].index)
    df_iqr = df_iqr.drop(df_iqr[df_iqr["cr"] < low_range_monsters].index)
    print("Printing monsters withing the IQR \n", df_iqr) #The IQR is quite compact, only 12 rows are dropped using this
    #STDEV would be more useful with the values given 


find_quantile_cr()
iqr_monster_cr()
import pandas as pd; import numpy as np;
import sqlalchemy as sql; import string; import import_data
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

'''
This section focuses on extrapolating data from the selected monster sources, using different functions,
those being the monster manual and volos guide to monsters, with an intention to add MTF later
'''

checker = "\n *** \n Testing \n *** \n"
divider = "\n***\n***\n"
question = "Type 1 for yes, or 2 for no"
#Could create global variable to implement the DataFrame, but using local variables to return particular outputs
#For future use with the interface file

def find_average_cr():
    #Finds average CR, may need to convert CR column to int/double for this
    df_copy = import_data.csv_cleaner()
    #print(checker, df_copy)
    #print("The mean value of the challenge rating is {0:.1f}".format(df_copy["cr"].mean()), divider)
    #print("The mode value of the challenge rating is {0:.1f}".format(int(df_copy["cr"].mode())))
    return df_copy["cr"].mean()
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

def ranked_by_cr():
    df_copy = import_data.csv_cleaner()
    df_copy["rankedcr"] = df_copy["cr"].rank(ascending=1)
    print(divider, "The least challenging monsters are \n", df_copy[df_copy["rankedcr"] < 40].sort_values("rankedcr"))
    print(divider, "The most challenging monsters are \n", df_copy[df_copy["rankedcr"] > 330].sort_values("rankedcr"))

def standard_dev_cr():
    df_copy = import_data.csv_cleaner()
    average = find_average_cr()
    std_cr = df_copy["cr"].std()
    top_range_monsters = average + std_cr * 1.96
    low_range_monsters = average - std_cr * 1.96
    df_out = df_copy
    #Create dataframe for returning information
    #Holds the top monsters to fight - print(df_out[df_out["cr"] > top_range_monsters].values)
    #Hold the bottom mosnters to fight - print(df_out[df_out["cr"] < low_range_monsters].values)
    df_out = df_out.drop(df_out[df_out["cr"] > top_range_monsters].index)
    df_out = df_out.drop(df_out[df_out["cr"] < low_range_monsters].index)
    #print(df_out)
    return df_out


standard_dev_cr()
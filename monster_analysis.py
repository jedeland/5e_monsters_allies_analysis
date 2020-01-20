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
#Should redesign functions to be modular and callable using the cleaned DF or a global variable, see below example
#When implementing the interface file
#df_global = import_data.csv_cleaner()
#def find_average_cr(df_input):
    #Finds average CR, may need to convert CR column to int/double for this
    #df_copy = df_input
    #out = round(df_copy["cr"].mean())
    #print(out)
    #return out

def find_average_cr():
    #Finds average CR, may need to convert CR column to int/double for this
    df_copy = import_data.csv_cleaner()
    #print(checker, df_copy)
    #print("The mean value of the challenge rating is {0:.1f}".format(df_copy["cr"].mean()), divider)
    #print("The mode value of the challenge rating is {0:.1f}".format(int(df_copy["cr"].mode())))
    out = round(df_copy["cr"].mean())
    return out

def find_quantile_cr():
    #Finds the average CR of each quantile, and outputs a CR average that fits into the "normal" range
    #Aka, between .25 and .75
    df_copy = import_data.csv_cleaner()
    print(checker)
    print("The first quantile of the CR is {}".format(df_copy["cr"].quantile(.25)),
          "The second quantile of the CR is {}".format(df_copy["cr"].quantile(.50)),
          "The third quantile of the CR is {}".format(df_copy["cr"].quantile(.75)))

def find_types_of_monster():
    df_copy = import_data.csv_cleaner()
    #Creating seperate dataframes using user input
    types = df_copy["type"].unique()
    print("Type the number of the type of monster you would like to search through")
    for i in range(len(types)-1):
        print("{0}: {1}".format(i, types[i]))
    user_input = input("Number: ")
    if user_input.isdigit() and int(user_input) < 13:
        print("Ok: Printing a Dataframe of this type of monster, along with some information")
        #Dataframe should be able to call different functions to create a wider picture of the DF
        monster_type_df = df_copy[df_copy["type"].values == types[int(user_input)]]
        num_monsters = len(monster_type_df)
        cr_avrg = round(monster_type_df["cr"].mean())
        deadliest = monster_type_df.loc[monster_type_df["cr"].values == monster_type_df["cr"].max()]
        weakest = monster_type_df[monster_type_df["cr"].values == monster_type_df["cr"].min()]
        print("The DataFrame contains {0} monsters\nThe Average Cr is {1}\nThe Deadliest monster is the {2}\nThe Weakest monster is the {3}\n"
              .format(num_monsters, cr_avrg, deadliest["name"].values, weakest["name"].values), monster_type_df)



find_types_of_monster()

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
    #print("Testing \n", df_out)
    return df_out

find_average_cr()
standard_dev_cr()
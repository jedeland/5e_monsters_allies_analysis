import pandas as pd; import numpy as np; import monster_analysis
import sqlalchemy as sql; import string; import import_data
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

def witcherify_monster():
    vulnerabilities = []
    resistance = []
    invulnerability = []

    print("This function witcherifies a monster, using the rules proscribed in this video\n",
          "https://youtu.be/GhjkPv4qo5w\n"
           )
    group_in = input("Please type the size of the group: ")
    if group_in.isdigit() and group_in != "1":
        print("Please type in the levels of the group")
        level_inputs = []
        for i in range(int(group_in)):
            level_inputs.append(int(input("Level: ")))

        average_lvl = sum(level_inputs) / len(level_inputs)
        average_lvl = round(average_lvl)
        cr_out = average_lvl+3
        print("Your group is made up of players that are levels : ", level_inputs,
              "\nThat means the average level is {}".format(average_lvl),
              "\nThe witcherified monster should be CR: {}".format(cr_out))
        monster = choose_monster(cr_out)
    else:
        print("This is an invalid input, please ensure the input is numeric and above 1")
        pass

def choose_monster(cr_in):
    #This function aims to choose a random monster based on the CR set above
    df_copy = monster_analysis.standard_dev_cr() #Uses standard dev to create a more relevant df
    df_refined = df_copy[round(df_copy["cr"]) == cr_in]
    df_refined = df_refined.drop(df_refined[df_refined["legendary"].values == "legendary"].index)

    print(df_refined.head())




witcherify_monster()
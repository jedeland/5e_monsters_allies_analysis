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
        monster = refine_monster(cr_out) #Continue after function is completed
    else:
        print("This is an invalid input, please ensure the input is numeric and above 1")
        pass

def refine_monster(cr_in):
    #This function aims to choose a random monster based on the CR set above
    df_copy = monster_analysis.standard_dev_cr() #Uses standard dev to create a more relevant df
    df_refined = df_copy[round(df_copy["cr"]) == cr_in]
    df_refined = df_refined.drop(df_refined[df_refined["legendary"].values == "legendary"].index)
    df_refined = df_refined.drop(df_refined[df_refined["lair"].values == "lair"].index)
    print(df_refined.index.tolist())
    monster_list = df_refined.index.tolist()
    print(monster_list[np.random.randint(0, len(monster_list))])
    while len(monster_list) > 3:
        monster_list.pop(np.random.randint(len(monster_list)))
    print(monster_list)
    print("Your options for a witcherfied monster are: ")
    #print(df_refined.keys())
    monster_selections = []
    refine_selections(df_refined, monster_list, monster_selections)
    print("Your options of selection are:")
    print("1: {0} \n2: {1} \n3: {2}".format(monster_selections[0], monster_selections[1], monster_selections[2]))
    monster_choice = input("Please type the number of your preferred monster, from the list: ")
    monster_list = monster_list.drop(monster_list[monster_list["name"] != mon])







def refine_selections(df_refined, monster_list, monster_selections):
    for i in range(len(monster_list)):
        monster_row = df_refined[df_refined.index == monster_list[i]]
        print(monster_row[["name", "hp", "ac", "size", "src", "pagenum", "section", "environment", "alignment"]])
        print("A {0} is a CR {1} monster with {2} hp that lives in the: {3}".format
              (monster_row["name"].values, monster_row["cr"].values,
               monster_row["hp"].values, monster_row["environment"].values))
        monster_selections.append("A {0} is a CR {1} monster with {2} hp that lives in the: {3}".format
              (monster_row["name"].values, monster_row["cr"].values,
               monster_row["hp"].values, monster_row["environment"].values))
        print("\n***\n")


witcherify_monster()
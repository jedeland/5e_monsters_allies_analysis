import pandas as pd; import numpy as np; import monster_analysis
import sqlalchemy as sql; import string; import import_data
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so


# This list of damage types was taken from https://www.reddit.com/r/dndnext/comments/9w5ho5/im_compiling_a_list_of_all_sources_of_resistance/
# Kudos to u/LyschkoPlon for creating it
dnd_5e_damage = ["Poison", "Fire", "Psychic", "Necrotic", "Cold", "Acid", "Piercing", "Slashing", "Bludgeoning",
                 "Magical (Weapon)", "Magical (Spell)", "Thunder", "Lightning", "Radiant", "Force",
                 "Weapon (Ranged)", "Weapon (Melee)"]
# These damage types should not appear on the same monster
non_compat_damage = {"Fire": "Cold", "Bludgeoning": "Piercing", "Necrotic": "Radiant",
                     "Cold": "Fire", "Piercing": "Bludgeoning", "Radiant": "Necrotic"}


def witcherify_monster():

    df_copy = monster_analysis.standard_dev_cr()
    print("This function witcherifies a monster, using the rules proscribed in this video\n",
          "https://youtu.be/GhjkPv4qo5w\n"
           )
    group_in = input("Please type the size of the group: ")

    # Lures needs to be improved, or can be added by the user using line interface, also needs to be made global
    # Lures could use creature types instead of names, to generalise the output
    lures = ["The creature is attracted to the scent of {} meat".format(df_copy["type"].sample().values),
         "The creature is attracted to the scent of {} meat".format(df_copy["name"].sample().values)]

    if group_in.isdigit() and group_in != "1" and int(group_in) <= 15:
        print("Please type in the levels of the group")
        level_inputs = []
        for i in range(int(group_in)):
            number_in = input("Level: ")
            if int(number_in) <= 30:
                level_inputs.append(int(number_in))
            else:
                print("The character's level has to be less than 30")


        average_lvl = sum(level_inputs) / len(level_inputs)
        average_lvl = round(average_lvl)
        cr_out = average_lvl+3
        print("Your group is made up of players that are levels : ", level_inputs,
              "\nThat means the average level is {}".format(average_lvl),
              "\nThe witcherified monster should be CR: {}".format(cr_out))
        #Outputs a single monster that has been selected using the console (out of 3)
        monster = refine_monster(cr_out)
        witcher_monster = mutate_monster(monster)
        #Continue with more options later on using the user interface

    elif int(group_in) > 16:
        print("This function does not support party sizes of that size")

    else:
        print("This is an invalid input, please ensure the input is numeric and above 1")
        pass


def mutate_monster(monster):
    #Take the monster that you chose, and half their HP
    vulnerabilities = []
    resistance = []
    invulnerability = []
    monster["hp"] = int(monster["hp"]) / 2
    num_immunity = round(int(monster["cr"]) / 3)
    num_resistance = None
    num_vulnerabilites = None
    if int(monster["cr"]) < 9:
        num_resistance = round(int(monster["cr"]))
        num_vulnerabilites = np.random.randint(1, 2)
    else:
        num_resistance = round(int(monster["cr"]) - 2)
        num_vulnerabilites = np.random.randint(1, 3)
    print(
        "Because of the creatures strength, mutation or otherwise ungodly powers, it has gained {0} immunities and {1} resistances!".
        format(num_immunity, num_resistance))
    print("In addition, the monster has become vulnerable to {} types of damage".format(num_vulnerabilites))
    #for loops that add the resis, invun, and vulner
    dmg_reduced = dnd_5e_damage
    for i in range(num_resistance):
        x = np.random.randint(0, len(dmg_reduced) -1)
        resistance_type = dmg_reduced[x]
        dmg_reduced.pop(x)
        if resistance_type not in resistance:
            resistance.append(resistance_type)
    for i in range(num_vulnerabilites):
        x = np.random.randint(0, len(dmg_reduced) -1)
        vulnerability_type = dmg_reduced[x]
        dmg_reduced.pop(x)
        if vulnerability_type not in resistance or vulnerabilities:
            vulnerabilities.append(vulnerability_type)
    for i in range(num_immunity):
        x = np.random.randint(0, len(dmg_reduced) -1)
        invulnerability_type = dmg_reduced[x]
        dmg_reduced.pop(x)
        if invulnerability_type not in resistance or vulnerabilities or invulnerability:
            invulnerability.append(invulnerability_type)





    print("The mutated {0} - has become resistant to the following types of damage\n{1}\nAnd has become immune to the following types of damage {2}"
    "\nAnd has become vulnerable to the following types of damage {3}".format(monster["name"].values, resistance, invulnerability, vulnerabilities))
    monster["resistance"] = pd.Series([resistance])
    monster["invulnerability"] = pd.Series([invulnerability])
    monster["vulnerabilities"] = pd.Series([vulnerabilities])
    return monster


def refine_monster(cr_in):
    #This function aims to choose a random monster based on the CR set above
    df_copy = monster_analysis.standard_dev_cr() #Uses standard dev to create a more relevant df
    df_refined = df_copy[round(df_copy["cr"]) == cr_in]
    df_refined = df_refined.drop(df_refined[df_refined["legendary"].values == "legendary"].index)
    df_refined = df_refined.drop(df_refined[df_refined["lair"].values == "lair"].index)

    monster_list = df_refined.index.tolist()
    while len(monster_list) > 3:
        monster_list.pop(np.random.randint(len(monster_list)))

    print("Your options for a witcherfied monster are: ")
    #print(df_refined.keys())
    monster_selections = []
    refine_selections(df_refined, monster_list, monster_selections)
    monster_selections = choose_monster(df_refined, monster_list, monster_selections)
    #print(monster_selections) Test
    return monster_selections


def choose_monster(df_refined, monster_list, monster_selections):
    print("Your options to select are:")
    print("1: {0} \n2: {1} \n3: {2}".format(monster_selections[0], monster_selections[1], monster_selections[2]))
    monster_choice = input("Please type the number of your preferred monster, from the list: ")
    monster_list = df_refined[df_refined.index == monster_list[int(monster_choice) - 1]]
    print("You have selected the {}".format(monster_list["name"].values))
    return monster_list


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
#No imports are required for this file, as the file will be used to direct a textual interface
from monster_analysis import *

analysis_list = ["Find Average", "Find IQR", "Find Types of Monsters", "General Information", "Show Monsters in IQR",
                 "Rank Monsters By Cr", "Show Monsters in Standard Deviation"]
visualisation_list = ["Plot Box", "Plot Line"]
analysis_list.append("Quit")
visualisation_list.append("Quit")
actions_dict = {"Analysis": analysis_list, "Visualisation": visualisation_list}

def start():
    finished = False

    print("Please type the action you wish to take:")
    keys = list(actions_dict.keys())
    keys.append("Quit")
    for i in range(len(actions_dict.keys()) + 1):
        x = i + 1
        print("{0}: {1}".format(x, keys[i]))
    while not finished:
        user_in = input("")
        if user_in == "1" or 1:
            analysis_options()
        elif user_in == "2" or 2:
            visualisation_options()
        elif user_in == "3" or 3:
            finished = True
        else:
            print("That is not a valid input, Try again:\n")

def analysis_options():
    print("Showing Analysis Options")

    for i in range(len(analysis_list)):
        x = i + 1
        print("{0}: {1}".format(x, analysis_list[i]))
    analysis_dict = {"1":find_average_cr(), "2":find_quantile_cr(), "3":find_types_of_monster()
                     ,"4":general_info_monsters(),"5":iqr_monster_cr(),"6":ranked_by_cr()
                     ,"7":standard_dev_cr(),"8":True}


def visualisation_options():
    print("Showing Visualisation Options")
    visualisation_list.append("Quit")
    for i in range(len(visualisation_list)):
        x = i + 1
        print("{0}: {1}".format(x, visualisation_list[i]))



start()
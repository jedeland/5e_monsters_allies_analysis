#No imports are required for this file, as the file will be used to direct a textual interface
analysis_list = ["Find Average", "Find IQR", "Find Types of Monsters", "General Information", "Show Monsters in IQR",
                 "Rank Monsters By Cr", "Show Monsters in Standard Deviation"]
visualisation_list = ["Plot Box", "Plot Line"]
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

def analysis_options():


def visualisation_options():

start()
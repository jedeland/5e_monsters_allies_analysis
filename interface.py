#No imports are required for this file, as the file will be used to direct a textual interface
def start():
    finished = False

    analysis_list = ["Find Average", "Find IQR", "Find Types of Monsters", "General Information", "Show Monsters in IQR", "Rank Monsters By Cr", "Show Monsters in Standard Deviation"]
    visualisation_list = ["Plot Box", "Plot Line"]
    actions_dict = {"Analysis":analysis_list, "Visualisation":visualisation_list}
    print("Please type the action you wish to take:")
    keys = list(actions_dict.keys())
    keys.append("Quit")
    for i in range(len(actions_dict.keys()) + 1):
        x = i + 1
        print("{0}: {1}".format(x, keys[i]))
    while not finished:
        user_in = input("")


start()
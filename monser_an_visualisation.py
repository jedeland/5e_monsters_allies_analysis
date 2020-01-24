import pandas as pd; import numpy as np; import matplotlib.pyplot as plt
import sqlalchemy as sql; import string; import import_data; import monster_analysis
#Pandas and sqlalchemy have to be initialised with the terminal, use pip install x to do so

'''
This file aims to visualise data that has been processed in the monster_analysis.py file
'''
def plot_cr_box():
    df_copy = import_data.csv_cleaner()
    print(df_copy.columns)
    df_copy.boxplot(by="type", column="cr")
    #Shows the Cr based on type using a box plot
    plt.show()

def plot_cr_line():
    df_copy = monster_analysis.ranked_by_cr()
    print(df_copy.columns)
    names = df_copy["name"]
    crs = df_copy["cr"]
    plt.plot(names, crs)
    plt.show()

plot_cr_line()
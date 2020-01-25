import pandas as pd; import numpy as np; import monster_analysis
import sqlalchemy as sql; import string; import import_data

#This addon pack focuses on the application of current and historic data to create more organic naming conventions for NPC's
#The following dataset will act as an anchor for this https://www.ssb.no/en/navn#renderAjaxBanner
#https://www.europeandataportal.eu/data/datasets?locale=en&tags=vornamen&keywords=vornamen
#https://www.europeandataportal.eu/data/datasets?locale=en
#https://archaeologydataservice.ac.uk/archives/view/atlas_ahrb_2005/datasets.cfm?CFID=331341&CFTOKEN=70517262
#Information taken from https://www.europeandataportal.eu under the Creative Commons Share-Alike Attribution Licence (CC-BY-SA).
#Arcane name set seems like a useful idea, see text below
'''
Courtesy of u/Alazypanda -
If need random fantastical sounding names I quite literally take the "generic" or chemical names of medication
Like the leader of the mafia my players are working with, Levo Thyroxine.
Might be worth adding some to the data base, but then its up to you to find where to split the word for first/lastname to make it sound right.
'''

npc_df = None

def npc_scandi_male():
    df = pd.read_excel("boys_NW_NPC.xlsx")
    df = df.rename(columns={"Historical top boys' names. 1880-2019" : "year"})
    for i in range(10):
        df = df.rename(columns={"Historical top boys' names. 1880-2019.{}".format(str(i + 1)) : str(i + 1)})
    df = df.dropna(axis="index")
    for x in range(len(df.columns) - 1):
        x += 1
        df["{}".format(str(x))] = [y.replace("\*","") for y in df["{}".format(str(x))]]

    print(df.columns)
    print(df)

npc_scandi_male()
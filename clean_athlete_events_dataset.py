##This script is for cleaning the data from the athlete_events dataset to allow match ups to my other dataset eg. through sport names

#Imports
import pandas as pd
import re
import csv

#import from other cleaning script other data & also select columns method
from clean_winter_olympic_medals_data import events_list as events_with_start_dates #Used for matching up the datasets
from clean_winter_olympic_medals_data import select_columns #Select Cols method which creates a new dataframe
pd.options.mode.chained_assignment = None  # default='warn'


##To get the events in the CSV so can match up with team from other one.
df = pd.read_csv("athlete_events.csv")
df_winter = df[(df.Season == 'Winter')]
sports = df_winter.Sport.unique().tolist()
events = df_winter.Event.unique().tolist()

#Function for removing the sport name in the column for events, the sport name is currently present in the CSV.
def remove_sport(item, list):
    sport = re.findall(r"(?=("+'|'.join(list)+r"))", item)
    sport = sport[0] + " "
    val = (re.split(sport, item))[1]
    return val

##Cleaning the data to match up with Winter_Olympic_Medals dataset
df_winter["Event"] = df_winter['Event'].apply(lambda x: remove_sport(x, sports))
events = df_winter.Event.unique().tolist()

##Creating a cleaned column that strips down the team column from eg. Britain - 3 to Britain
def adjustTeam(item):
    if (bool(re.search(r'\d', str(item)))):
        new_item = re.split(r'-', str(item))
        new_item = new_item[0].strip()
        return new_item
    else:
        new_item = item.strip()
        return new_item


#Create the cleaned_nation column which provides a value for each row for nation which can then be used
df_winter['cleaned_nation'] = df_winter['Team'].apply(lambda x: adjustTeam(x))

##Cleaning of dataset values for purpose of matching up sports etc. This also ensures that all the data is correct.
df_winter["Event"] = df_winter["Event"].str.capitalize()
df_winter["Sport"] = df_winter['Sport'].apply(lambda x: x.replace("Military Ski Patrol", "Biathlon"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" metres", "m"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" kilometres", "km"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" m", "m"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" km", "km"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("-kilometres", "km"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" kilometres", "km"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" / ", " "))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("/", " "))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(" x ", " "))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("mass", " mass"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("hill ", "hill, "))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("military", " military"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("Mixed (men)'s doubles", "Men's doubles"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("dancing", "dancing"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace(", individual", ""))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("Women's team pursuit (6 laps)", "Women's team pursuit"))
df_winter["Event"] = df_winter['Event'].apply(lambda x: x.replace("Men's team pursuit (8 laps)", "Men's team pursuit"))
df_winter["Event"] = df_winter["Event"].str.capitalize()
df_winter.loc[df_winter.Sport == "Alpine Skiing", 'Event'] =  df_winter['Event'].apply(lambda x: x.replace("super g", "super G"))

#Create new data frame and create a distinct list for sports & events - for the purposes of matching below.
events = select_columns(df_winter, ['Sport', 'Event'])
events.drop_duplicates(subset =["Sport", "Event"], keep = "first", inplace = True)
events_list = events.values.tolist()
events_list.sort(key=lambda x: (x[0], x[1]), reverse=False) #sorted by year

##Function below is for matching the data and checking all is correct. Non-Matches on events and sports will reveal inaccuracies between the data regarding sports and events.
def match_datasets(dataset_one, dataset_two):
    for event in dataset_one:
        matched = False
        for item in dataset_two:
            if (event[0] == item[0]) and (event[1] == item[1]):
                matches.append(event)
                matched = True
        if (not matched):
            non_matches.append(event)

    for item in dataset_two:
        matched = False
        for event in dataset_one:
            if (event[0] == item[0]) and (event[1] == item[1]):
                matched = True
        if (not matched):
            non_matches.append(item)

matches = []
non_matches = []
#Call function to test matches
match_datasets(events_with_start_dates, events_list)

#GRAPH to create data ready to produce the Height or Weight data in Main.py.

#--PLEASE RUN main.py FOR THIS GRAPH--#

#Imports
import pandas as pd
import plotly as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random

# Import the dataframes
from clean_athlete_events_dataset import df_winter as df_filtered #import the cleaned_nation dataframe from athlete events
from clean_winter_olympic_medals_data import df as medals_df

#Create some general variables and lists to be iterated through
medals_df_formatted = medals_df[(medals_df.sport_style == 'individual')]
sports = medals_df_formatted.Sport.unique().tolist()
years = medals_df_formatted.Year.unique().tolist()
years.sort()
events = medals_df_formatted.Event.unique().tolist()

#A method that pulls the first year of sport introduction and all intervening years before re-introduction even if the sport was absent at Olympics after it was introduced
def find_years(sport_years, overall_years):
    years = []
    year_introduced = sport_years[0]
    final_year = sport_years[len(sport_years) - 1]
    for item in overall_years:
        if item == year_introduced:
            years.append(year_introduced)
            i = overall_years.index(year_introduced)
            i += 1
            for year in range(len(overall_years) - i):
                years.append(overall_years[i])
                i += 1
    return years

#A method that takes in a list and calculates an average for a list, deals with values NaN
def average_calc(list):
    i = 0
    sum = 0
    for item in list:
        if item != "NaN":
            sum += item
            i += 1
    avg = (sum / i)
    return avg

#A method that returns the filtered frame according to what medal, sport and event is chosen. The years is just a list of all years for Winter Olympics
def return_filtered_frame(medal, sport, event, years):
    team_individual = ""
    #filtered frame to find the years of when the sport was active(to only show the years it was active or inbetweening years )
    filtered_frame_for_years = df_filtered[(df_filtered.Sport == sport) & (df_filtered.Event == event)]
    years_for_sport = filtered_frame_for_years.Year.unique().tolist()
    years_for_sport.sort()
    #manipulate years to only show data for when the event was present at the olympics BUT if sport was pulled it keeps the intervening years
    years_for_sport = find_years(years_for_sport, years)
    filtered_frame = df_filtered[(df_filtered.Medal == medal) & (df_filtered.Sport == sport) & (df_filtered.Event == event)]
    #find length of filtered frame & then find average per year
    dict = []

    for year in years_for_sport:
        filtered_frame_year = filtered_frame[(filtered_frame.Year == year)]
        if (len(filtered_frame_year) == 0):
            dict.append({ "Name" : None,
                        "Sex": None,
                        "Height": None,
                        "Weight": None,
                        "Team": None,
                        "Year": year,
                        })
        if (len(filtered_frame_year) == 1):
            dict.append({ "Name" : filtered_frame_year.iloc[0]['Name'],
                        "Sex": filtered_frame_year.iloc[0]['Sex'],
                        "Height": filtered_frame_year.iloc[0]['Height'],
                        "Weight": filtered_frame_year.iloc[0]['Weight'],
                        "Team": filtered_frame_year.iloc[0]['cleaned_nation'],
                        "Year": year,
                        })
        if (len(filtered_frame_year) > 1):
            heights = filtered_frame_year.Height.unique().tolist()
            weights = filtered_frame_year.Weight.unique().tolist()
            dict.append({ "Name" : filtered_frame_year.iloc[0]['Team'],
                        "Sex": "Team",
                        "Height": average_calc(heights),
                        "Weight": average_calc(weights),
                        "Team": filtered_frame_year.iloc[0]['cleaned_nation'],
                        "Year": year,
                        })
            team_individual = "Average "
    returned_df = pd.DataFrame(dict)
    return returned_df, team_individual

#Again some variables to be passed through to main.py. medal_settings is for size of the dots and colours and medals is for the possible medals to be iterated through
medal_settings = [['Gold', 20, 'Gold'], ['Silver', 16, 'Silver'], ['Bronze', 12, 'saddlebrown']]
medals = ['Gold', 'Silver', 'Bronze']

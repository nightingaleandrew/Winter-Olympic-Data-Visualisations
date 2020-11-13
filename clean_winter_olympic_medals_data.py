##This function is for cleaning the data from the Winter_Olympic_Medals dataset so it can be used for efficient comparison with my other dataset: athletes data
#In here I also have the messages for the Heights and Weights regarding sports and the colour schemes for each sport

#Imports
import plotly.graph_objects as go
import pandas as pd
import re
import csv

#Import the file
csvFile = "Winter_Olympic_Medals.xlsx - Data.csv"
df = pd.read_csv(csvFile)

#Lists for nations and events
nations = df.Country.unique().tolist()
events = df.Event.unique().tolist()

#Function for creating a column that states whether the medal was a team or individual medal
def ifTeam(item):
    new_item = re.split(r'-', str(item))
    if new_item[0] in nations:
        return "team"
    else:
        return "individual"

#Function for creating a new df with certain columns in a list
def select_columns(data_frame, column_names):
    new_frame = data_frame.loc[:, column_names]
    return new_frame

#Function for adding an event to every line
def yearIntro(item):
    for event in events_list:
        if event[1] == item:
            return event[3]
    return "none"

#For cleaning the dataset so it can match the other.
df["Medal"] = df['Medal'].apply(lambda x: x.replace("gold", "Gold"))
df["Medal"] = df['Medal'].apply(lambda x: x.replace("silver", "Silver"))
df["Medal"] = df['Medal'].apply(lambda x: x.replace("bronze", "Bronze"))

#Create the column for team or individual sport
df["sport_style"] = df['Name of Athlete or Team'].apply(lambda x: ifTeam(x))
df["yearIntro"] = df['Year'].apply(lambda x: x)

##Amending Sports to match other file
df["Sport"] = df['Sport'].apply(lambda x: x.replace("Bobsled", "Bobsleigh"))
df["Sport"] = df['Sport'].apply(lambda x: x.replace("Speedskating", "Speed Skating"))
df["Sport"] = df['Sport'].apply(lambda x: x.replace("Cross-Country Skiing", "Cross Country Skiing"))
df["Sport"] = df['Sport'].apply(lambda x: x.replace("Short-Track Speed Skating", "Short Track Speed Skating"))

##Ammending Events to match other file
df["Event"] = df["Event"].str.capitalize()
df["Event"] = df['Event'].apply(lambda x: x.replace("ã— ", ""))
df["Event"] = df['Event'].apply(lambda x: x.replace(" meters", "m"))
df["Event"] = df['Event'].apply(lambda x: x.replace(" kilometers", "km"))
df["Event"] = df['Event'].apply(lambda x: x.replace(" m", "m"))
df["Event"] = df['Event'].apply(lambda x: x.replace("-meter", "m"))
df["Event"] = df['Event'].apply(lambda x: x.replace(" km", "km"))
df["Event"] = df['Event'].apply(lambda x: x.replace("-kilometer", "km"))
df["Event"] = df['Event'].apply(lambda x: x.replace(" kilometer", "km"))
df["Event"] = df['Event'].apply(lambda x: x.replace(" x ", " "))
df["Event"] = df['Event'].apply(lambda x: x.replace("4x10km", "4 10km"))
df["Event"] = df['Event'].apply(lambda x: x.replace("hill ", "hill, "))
df["Event"] = df['Event'].apply(lambda x: x.replace("military", " military"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Men ", "Men's "))
df["Event"] = df['Event'].apply(lambda x: x.replace("Women ", "Women's "))
df["Event"] = df['Event'].apply(lambda x: x.replace("dance", "dancing"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Ice", "Mixed ice"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Menâ€™s ", "Men's "))
df["Event"] = df['Event'].apply(lambda x: x.replace(" / ", " "))
df["Event"] = df['Event'].apply(lambda x: x.replace("/", " "))
df["Event"] = df['Event'].apply(lambda x: x.replace("+", "and"))
df["Event"] = df['Event'].apply(lambda x: x.replace("mass", " mass"))
df["Event"] = df['Event'].apply(lambda x: x.replace("6 ", "6km "))
df["Event"] = df['Event'].apply(lambda x: x.replace("6km laps", "6 laps"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Team relay", "Mixed team relay"))
df["Event"] = df['Event'].apply(lambda x: x.replace(", individual", ""))
df["Event"] = df['Event'].apply(lambda x: x.replace(" classic", ""))
df["Event"] = df['Event'].apply(lambda x: x.replace(" free", ""))
df["Event"] = df['Event'].apply(lambda x: x.replace("Team", "Mixed team"))
df["Event"] = df['Event'].apply(lambda x: x.replace("super combined", "combined"))
df["Event"] = df['Event'].apply(lambda x: x.replace("ski halfpipe", "halfpipe"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Men's skiathlon 15km and 15km", "Men's 30km skiathlon"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Women's skiathlon 7.5km and 7.5km", "Women's 15km"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Women's team pursuit (6 laps)", "Women's team pursuit"))
df["Event"] = df['Event'].apply(lambda x: x.replace("Men's team pursuit (8 laps)", "Men's team pursuit"))
df["Event"] = df['Event'].apply(lambda x: x.replace("ski slopestyle", "slopestyle"))
df.loc[df.Sport == "Ski Jumping", 'Event'] =  df['Event'].apply(lambda x: x.replace("Men's team", "Men's large hill, team")) #Does work lol
df.loc[df.Sport == "Alpine Skiing", 'Event'] =  df['Event'].apply(lambda x: x.replace("super g", "super G"))

##Create new dataframe
events = select_columns(df, ['Sport', 'Event', 'sport_style', "yearIntro"])
events.drop_duplicates(subset =["Sport", "Event"], keep = "first", inplace = True) #Combines duplicates of sport & event
events_list = events.values.tolist()
events_list.sort(key=lambda x: (x[0], x[1], x[2], x[3]), reverse=False) #sorted by year
df["yearIntro"] = df['Event'].apply(lambda x: yearIntro(x))

sports = df.Sport.unique().tolist()
sports_and_events = {}
for sport in sports:
    df_sport = df[(df.Sport == sport)]
    events = df_sport.Event.unique().tolist()
    sports_and_events[sport] = events


#This is for matching sports to colours to create the colour scheme for efficient analysis
snow_sports = ["Snowboarding", "Freestyle Skiing", "Ski Jumping", "Alpine Skiing",  "Cross Country Skiing"] #red (raspberry, rose, red, red orange, tiger)
ice_speed_sports = ["Luge", "Skeleton", "Bobsleigh"] #green (shamrock, seafoam, olive)
skating_sports = ["Short Track Speed Skating", "Speed Skating", "Figure Skating"] #blue (turquoise, cyan, purple)
combined_events = ["Nordic Combined", "Biathlon", "Alpinism"] #(banana, fire)
team_events = ["Ice Hockey", "Curling"] #(black, grey)

#Below are the messages for the sports that come up in the Flask interface when a sport and event are selected
sports_with_colours = [{"sport": "Snowboarding", "colour": "rgb(227,11,93)"}, {"sport": "Freestyle Skiing", "colour": "rgb(255,0,127)"}, {"sport": "Ski Jumping", "colour": "rgb(255,0,0)"}, {"sport": "Alpine Skiing", "colour": "rgb(255,83,73)"}, {"sport": "Cross Country Skiing", "colour": "rgb(255,98,0)"},
                        {"sport": "Luge", "colour": "rgb(69,206,162)"}, {"sport": "Skeleton", "colour": "rgb(69,206,128)"}, {"sport": "Bobsleigh", "colour": "rgb(128,128,0)"},
                        {"sport": "Short Track Speed Skating", "colour": "rgb(48,213,200)"}, {"sport": "Speed Skating", "colour": "rgb(0,255,255)"}, {"sport": "Figure Skating", "colour": "rgb(238,130,238)"},
                        {"sport": "Nordic Combined", "colour": "rgb(255,225,53)"}, {"sport": "Biathlon", "colour": "rgb(255,175,53)"}, {"sport": "Alpinism", "colour": "rgb(255,244,79)"},
                        {"sport": "Ice Hockey", "colour": "rgb(0, 0, 0)"}, {"sport": "Curling", "colour": "rgb(128,128,128)"}]

#the function for associating the sport to a colour upon trace for a graph. See the graph for old sports new nations
def choose_colour(sport):
    for item in sports_with_colours:
        if sport == item["sport"]:
            return item["colour"]


messages = [{"sport": "Alpine Skiing", "message": "Alpine Skiing debuted at the 1936 Winter Olympics and has been present every year."},
            {"sport": "Biathlon", "message": "Biathlon debuted as Military Patrol in 1924 however was not present again until 1960."},
            {"sport": "Bobsleigh", "message": "Bobsleigh has been present every year since 1960!"},
            {"sport": "Cross Country Skiing", "message": "Cross Country Skiing has been an event in every games!"},
            {"sport": "Curling", "message": "Curling was included in 1924 but not seen since until 1998!"},
            {"sport": "Figure Skating", "message": "Figure Skating was an original event since 1924."},
            {"sport": "Freestyle Skiing", "message": "Freestyle Skiing entered the schedule in 1992!"},
            {"sport": "Ice Hockey", "message": "Ice Hockey was an original event from 1924!"},
            {"sport": "Luge", "message": "Luge entered the schedule in 1964."},
            {"sport": "Nordic Combined", "message": "Nordic Combined consists of Cross Country Skiing and Ski Jumping and entered in 1924."},
            {"sport": "Speed Skating", "message": "Speed Skating entered the Winter Olympics in 1924."},
            {"sport": "Ski Jumping", "message": "Ski Jumping has been a mainstay sport for every Winter Olympics."},
            {"sport": "Snowboarding", "message": "Snowboarding first entered the Winter Olympics in 1998."},
            {"sport": "Short Track Speed Skating", "message": "Short Track Speed Skating entered the schedule in 1992."},
            {"sport": "Skeleton", "message": "Skeleton appeared at 1924, 1948 and then since 2002."}
            ]

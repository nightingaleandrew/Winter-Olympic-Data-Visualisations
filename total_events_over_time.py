# GRAPH
# -This graph shows through a stacked area chart, the volume of each sport per number of it's events over time. I have done this as it also shows both traditional older events and times when sports were introduced clearly

import plotly.graph_objects as go
import pandas as pd
import csv
import random
import time
import plotly as py

from clean_winter_olympic_medals_data import df, sports_with_colours, choose_colour #Uses the data from the Winter_Olympic_Medals Dataset. This is cleaned.


#Select this to True if you would like to run just this file.
view_individual_graph = False


# Create the list for years and sports to iterate through
years = df.Year.unique().tolist()
sports = df.Sport.unique().tolist()

# Get Y values for graph, i.e numbers for each sport (number of events within each sport) at each olympics
def get_y(years, cat, type):
    y = []
    if ((cat != "all") and (type == "gender")):
        for year in years:
            events_cat_for_yr = df[(df.Gender == cat) & (df.Medal == "Gold") & (df.Year == year)]
            y.append(len(events_cat_for_yr))
    elif ((cat != "all") and (type == "sportCat")):
        for year in years:
            events_cat_for_yr = df[(df.Sport == cat) & (df.Medal == "Gold") & (df.Year == year)]
            y.append(len(events_cat_for_yr))
    elif ((cat != "all") and (type == "teamInd")):
        for year in years:
            events_cat_for_yr = df[(df.sport_style == cat) & (df.Medal == "Gold") & (df.Year == year)]
            y.append(len(events_cat_for_yr))
    else:
        for year in years:
            events_cat_for_yr = df[(df.Medal == "Gold") & (df.Year == year)]
            y.append(len(events_cat_for_yr))
    return y

#List for the series for the graph
data = []

#Iterate over the sports to create the series for the graph.
for sport in sports:
    scatter = go.Scatter(name=sport, x = years, y = get_y(years, sport, "sportCat"), stackgroup='one', line=dict(width=0.5, color=choose_colour(sport)))
    data.append(scatter)

#Create the graph with further axis labels and data etc
fig = go.Figure(data = data) #data from above
fig.update_layout(title="Total Events Over Time", xaxis_title="Olympics", yaxis_title="Total Events",font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
fig.update_layout(xaxis=dict(showticklabels=True, type='category'), hovermode="x") #This allows all x labels to be viewed at once
fig.update_layout(height=750,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4)) #further margin details and height of graph itself.


#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

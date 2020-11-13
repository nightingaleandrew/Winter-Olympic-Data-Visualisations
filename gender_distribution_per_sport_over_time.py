#Show percentage difference between men and woman competitors for each sport over time.
#This is because there are many graphs showing how overall female numbers have increased to almost 50:50 but I wanted to see if there were still any
  #male or female dominant sports.
#Use % diff as some sports like cross country are more dominant than others - not really interested in total numbers
#--- If an athlete is entered twice in one sport I have counted that as two particpants --- #

#Imports
import pandas as pd
import re
import csv
import plotly.graph_objects as go
pd.options.mode.chained_assignment = None

#Import file and filter down and then count number of male or female competitors per sport
from clean_athlete_events_dataset import df_winter as df #import the cleaned dataframe from athlete events
from clean_winter_olympic_medals_data import sports_with_colours, choose_colour #Brings in the colour uses. This is cleaned.


#Select this to True if you would like to run just this file.
view_individual_graph = False



#Create the lists to iterate through for the data series for the graph eg. sports and years
sports = df.Sport.unique().tolist()
sports.sort(key=lambda x: (x[0]), reverse=False) #sorted by sport
years = df.Year.unique().tolist()
years = sorted(years) #Sort by year

#List for dicts for each sport each year for their % of males
gender_dist = []

#Percentage difference calculator
def percentage_diff(m, f):
    value = ((m - f) / ((m + f) / 2)) * 100
    return value

#Create the list dict for each sport in each year and male percentage %
for year in years:
    for sport in sports:
        males = df[(df.Sport == sport) & (df.Sex == "M") & (df.Year == year)]
        females = df[(df.Sport == sport) & (df.Sex == "F") & (df.Year == year)]
        if (len(females) == 0) and (len(males) == 0):
            percentage = 0
        else:
            percentage = (percentage_diff(len(males), len(females)) / 2)
            gender_dist.append({
                    "year": year, #The year
                    "sport": sport, #The sport
                    "male_athletes": len(males), #Number of the males in the sport for the year
                    "female_athletes": len(females), #Number of females in the sport for the year
                    "percentage_diff": round(percentage, 2), ##Round to 2%
                    })

#for the series on the graph
data = []
#Remember the years might be different for each sport eg. curling
def get_year(sport):
    list = []
    for item in gender_dist:
        if item['sport'] == sport:
            list.append(item['year'])
    return list

#Get Y values for the each series
def get_sport_distri(sport):
    list = []
    for item in gender_dist:
        if item['sport'] == sport:
            list.append(item['percentage_diff'])
    return list

#Create data series for this graph
for sport in sports:
    scatter = go.Scatter(name=sport, x = get_year(sport), y = get_sport_distri(sport), showlegend = True, mode="markers+lines", line=dict(color=choose_colour(sport)))
    data.append(scatter)

#Trying to fix animation version with connectgaps

#create graph
fig = go.Figure(data = data)
fig.update_layout(title="Male Dominance in Sports Over Time by %", xaxis_title="Time", yaxis_title="% of Male Dominance in Sport",font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
fig.update_layout(xaxis=dict(showticklabels=True), hovermode="x", yaxis=(dict(range=[-100, 100])))
fig.update_layout(height=750,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4))
fig.update_xaxes(showline=True, zerolinecolor="Black") #linewidth=1, zeroline=True, zerolinecolor='Black', zerolinewidth=4 #I have not found out why this does not seem to work


#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

#Thinking behind this graph
##I initially wanted to label the men and women with different coloured points if men dominant or women or dominant. It would look to crowded though in recent olympics and I wanted to see correlations over time.
##Therefore went for -0 and +0 for this. This would just require clearly explained title and y axis descriptions

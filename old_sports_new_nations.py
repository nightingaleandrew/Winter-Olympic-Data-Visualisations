#GRAPH

#With this graph I am looking to answer the question of whether newer nations to the Olympics take up younger sports or not. An original standpoint on the Winter Olympics data usage.

#However, due to Plotly presenting only the color values for the first frame, I have had to change the orientation of the graph slightly. The graph currently shows the data from
# the traditional sports and what percentage of newer nations take up these traditional sports. However, this does make the data sparse on the graph.

#Imports
import plotly.express as px
import pandas as pd

from clean_athlete_events_dataset import df_winter as df #import the cleaned_nation dataframe from athlete events
from clean_winter_olympic_medals_data import sports_with_colours, choose_colour #Uses the data from the Winter_Olympic_Medals Dataset. This is cleaned.


#Select this to True if you would like to run just this file.
view_individual_graph = False


#Create years to iterate through & sort in order
years = df.Year.unique().tolist()
years.sort()

#Iterate through each year to find the percentage of newer countries taking up each sport for that Olympics.
#It also looks for the age of each sport at each Olympics and updates the graph data accordingly.
values = []
countries = []
sports = []
sports_with_years = []
for year in years:
    df_by_year = df[(df.Year == year)]
    sports_per_year = df_by_year.Sport.unique().tolist()
    countries_participating = df_by_year.cleaned_nation.unique().tolist()
    new_countries = []
    for country in countries_participating:
        if country not in countries:
            new_countries.append(country)
            countries.append(country)
    for sport in sports_per_year:
        #find age of sport - a sport's age is calculated from it's original appearence.
        if sport not in sports:
            sports_with_years.append([year, sport]) #append to sports_with_years
            age_of_sport = 0
            sports.append(sport)
        else:
            for item in sports_with_years:
                if item[1] == sport:
                    age_of_sport = year - item[0]

        #work out percentage of new countries to take up the sport
        df_by_year_by_sport = df_by_year[(df_by_year.Sport == sport)]
        number = 0
        total = len(new_countries)
        for nation in new_countries:
            df_by_year_by_sport_by_nation = df_by_year_by_sport[(df_by_year_by_sport.cleaned_nation == nation)]
            if (len(df_by_year_by_sport_by_nation) > 0):
                number += 1

        if (number != 0):
            percentage = round((number / total) * 100, 1)
        else:
            percentage = 0

        total_participants = len(df_by_year_by_sport.cleaned_nation.unique().tolist())
        values.append({"Year": year,
                        "Sport ": sport,
                        "Age of Sport": age_of_sport,
                        "Number of Participating Nations": total_participants,
                        "% of New Nations That Take Up The Sport": percentage})

#Convert dict into dataframe
new_df = pd.DataFrame(values)

#Create the colour discrete map for the graph
color_discrete_map = {}
for item in sports_with_colours:
    sport = item["sport"]
    colour = item["colour"]
    color_discrete_map[sport] = colour

#Create Scatter Graph
fig = px.scatter(new_df,
                x="% of New Nations That Take Up The Sport",
                y="Age of Sport",
                animation_frame="Year",
                animation_group="Sport ",
                size="Number of Participating Nations",
                color="Sport ", #only shows data from first frame values of Sport column
                hover_name="Sport ",
                title="How popular are the 'traditional' sports with new nations?",
                range_x=[0,100],
                range_y=[0,100],
                color_discrete_map = color_discrete_map)

for trace in fig.data:
    trace.name = trace.name.split('=')[1]

fig.update_layout(
        hoverlabel=dict(
        bgcolor="black",
        bordercolor="black",
        font = dict(color='lightgray'),
        font_size=18,
        font_family="Rockwell"))

fig.update_xaxes(title = dict(text=""))
fig.update_layout(
    annotations=[
        dict(
            x=0.5,
            y=-0.2,
            showarrow=False,
            text="% of New Nations That Take Up The Sport",
            xref="paper",
            yref="paper",
            font = dict(size=26)
        )])
#this would add in a new label for x axis

fig.update_layout(
    font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))


#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

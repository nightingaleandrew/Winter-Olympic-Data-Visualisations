# GRAPH
# -This graph presents the reader with a simple stack graph that shows the total medals per country over the course of the Olympics.
# -I have added the specialist sport/most successful sport within the hover label.

#Imports
import plotly.graph_objects as go
import pandas as pd

#Using the athletes data will count up all the team medals as individual medals
from clean_athlete_events_dataset import df_winter as df_filtered
#Using the medals dataset will count up correct medal count.
from clean_winter_olympic_medals_data import df as df_medals

#Select this to True if you would like to run just this file.
view_individual_graph = False


#various variables that are used to be iterated through below
medals = ['Gold', 'Silver', 'Bronze']
years = df_medals.Year.unique().tolist()
countries = df_medals.Country.unique().tolist()
nations_cleaned_for_facts = df_filtered.cleaned_nation.unique().tolist()

##For hover text, I am including most dominant sport where they have won the medals - as I am using further data from the dataset to make it a little interactive
def most_successful_sport(countries_with_medals):
    list = []
    for country in countries_with_medals: #picks up name of country
        df = df_medals[(df_medals.Country == country[0])]
        sport = df.Sport.mode().tolist()
        num_of_medals = len(df)
        df = df[(df.Sport == sport[0])]
        num_df = len(df)
        percentage = (num_df / num_of_medals) * 100
        if (len(sport) > 1):
            for i in range(len(sport)):
                if i == 0:
                    string = sport[0]
                else:
                    string += " & " + sport[i]
            list.append(["Specialist sports: " + string + " at " + str(round(percentage, 1)) + "% of total medals each."])
        else:
            list.append(["Specialist sport: " + sport[0] + " at " + str(round(percentage, 1)) + "% of total medals."])
    return list

#Create list with country name and number of gold, silver, bronze medals
country_medal_counts = []
for country in countries:
    m = []
    m.append(country)
    for medal in medals:
        athletes = df_medals[(df_medals.Country == country) & (df_medals.Medal == medal)]
        m.append(len(athletes))
    country_medal_counts.append(m)

#Sort list by gold, then silver, then bronze medals order
country_medal_counts.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)


#Return list of items for each trace from other lists
def returnItems(list, index):
    countries = []
    for item in list:
        countries.append(item[index])
    return countries

countries_with_medals = []
for item in country_medal_counts:
    if ((item[1] + item[2] + item[3]) > 0):
        countries_with_medals.append(item)

#Medal settings for each trace colours and name
medal_settings = [['Gold', "rgb(212,175,55)"], ['Silver', "rgb(128,128,128)"], ['Bronze', "rgb(205, 127, 50)"]]

data = []
i = 0
#Create traces for the graph
for medal in medals:
    trace = go.Bar(name=medal, x = returnItems(countries_with_medals, 0), y = returnItems(countries_with_medals, i + 1),  hovertext=returnItems(most_successful_sport(countries_with_medals), 0), marker = dict(color = medal_settings[i][1], line = dict(color = medal_settings[i][1], width = 1)))
    data.append(trace)
    i += 1

#Creates the graph
fig = go.Figure(data = data)
fig.update_layout(barmode='stack') #Bar mode to stack
fig.update_layout(title="Official Medals by Country up to 2014", yaxis_title="Medals", font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
fig.update_layout(height=750, #size of chart
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4))

#Below is formatting of hover labels
fig.update_layout(
    hoverlabel=dict(
        bgcolor="black",
        bordercolor="black",
        font = dict(color='lightgray'),
        font_size=18,
        font_family="Rockwell"))

#This angles the x axis ticks
fig.update_xaxes(tickangle=45)

#The below allows the x label to be replaced by a paper annotation (x label was getting caught up in the x axis tick labels)
fig.update_layout(
    annotations=[
        dict(
            x=0.5,
            y=-0.29,
            showarrow=False,
            text="Country",
            xref="paper",
            yref="paper",
            font = dict(size=19)
        )])

#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

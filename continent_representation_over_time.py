# GRAPH
# -This graph reveals the change in geographic representation per continent over time for the Winter Olympics. It has animation so the bars (continent) rise over
#time revealing the active change.
# -The countries can also be hovered over too with their number of participants.

#Imports
import plotly.express as px
import pandas as pd
from clean_athlete_events_dataset import df_winter as df #import the cleaned_nation dataframe from athlete events
import pycountry_convert as pc

#Select this to True if you would like to run just this file.
view_individual_graph = False

#if the continent cannot be found in the pycountry library then this function uses the countries below.
unmatched = []
def get_key_val(dict_list, name, cont):
    bool = False
    for d in dict_list:
        if name in d.values():
            bool = True
            return d[cont]
    if bool == False:
        return 'Other'

#Manual dict of countries that are not in the module I imported pycountry
countries = [{"name": "Chinese Taipei", "continent": "Asia"},
            {"name": "Czechoslovakia", "continent": "Europe"},
            {"name": "East Germany", "continent": "Europe"},
            {"name": "Netherlands Antilles", "continent": "North America"},
            {"name": "Serbia and Montenegro", "continent": "Europe"},
            {"name": "Soviet Union", "continent": "Europe"},
            {"name": "Timor Leste", "continent": "Asia"},
            {"name": "Unified Team", "continent": "Europe"}, #This was a team made up of former soviet republic nations in 1992
            {"name": "West Germany", "continent": "Europe"},
            {"name": "Individual Olympic Athletes", "continent": "Asia"}, #This was a team made up of Indian Athletes in 2014
            {"name": "Yugoslavia", "continent": "Europe"},]

#Method for getting the continent from the country name using the pycountry library.
def get_continent_name(item):
    try:
      country_code = pc.country_name_to_country_alpha2(item, cn_name_format="default")
      continent_code = pc.country_alpha2_to_continent_code(country_code)
      continent_name = pc.convert_continent_code_to_continent_name(continent_code)
      return continent_name
    except KeyError:
        cont = get_key_val(countries, item, "continent") #Otherwise uses the method above if cannot find continent name in the library
        if cont != "Other":
            return cont
        else:
            return 'International'

#Adding a continent column into the dataset using the cleaned_nation column created in the clean_athlete_events_dataset file
df["continent"] = df['cleaned_nation'].apply(lambda x: get_continent_name(x)) #checks on every value in the dataset

#This method below creates the list of dicts for the values for the graph. It is then transformed into a df.
#It finds the number of countries per continent for each year/olympics. It also finds the num of particpants
details = []
years = df.Year.unique().tolist()
years.sort()
max_aths = []
errors = [[1924, ["Africa", "South America"]], [1928, ["Africa", "Oceania"]], [1932, ["Africa", "South America", "Oceania"]],
            [1936, ["South America", "Africa"]], [1948, ["Africa", "Oceania"]], [1952, ["Africa"]],
            [1956, ["Africa"]], [1964, ["Africa"]], [1972, ["Africa"]], [1976, ["Africa"]], [1980, ["Africa"]]]
for year in years:
    for error in errors:
        if error[0] == year:
            for continent in error[1]:
                details.append({"Olympics": year,
                                "Continent": continent,
                                "Country": "test",
                                "Athletes": 0,
                                "Number of Countries": 0},
                                )
    df_by_year = df[(df.Year == year)]
    countries_of_year = df_by_year.cleaned_nation.unique().tolist()
    countries_of_year.sort()
    for country in countries_of_year:
        df_by_year_by_country = df_by_year[(df_by_year.cleaned_nation == country)]
        continent = df_by_year_by_country['continent'].iloc[0]
        num_athletes = len(df_by_year_by_country)
        max_aths.append(num_athletes)
        details.append({"Olympics": year,
                        "Continent": continent,
                        "Country": country,
                        "Athletes": num_athletes,
                        "Number of Countries": 1},
                        )

#Create the dataframe for the Plotly express graph below.
final_df = pd.DataFrame(details)

#Mapping the colours to the continent values. I have used the Olympic ring colours.
color_discrete_map = {'Asia': 'rgb(244, 195, 0)',
                        'Europe': 'rgb(0, 133, 199)',
                        'North America': 'rgb(178, 0, 29)',
                        'Oceania':'rgb(0, 159, 61)',
                        'Africa':'rgb(0, 0, 0)',
                        'South America': 'rgb(238, 125, 143)'}

fig = px.bar(final_df,
                        x="Continent", #col for x values
                        y="Number of Countries", #col for y values
                        color="Continent", #divides up on the continent column within the dataframe
                        animation_frame="Olympics", #range slider is on the Olympics values
                        animation_group="Country", #adds countries into bar
                        range_y=[0, 45], #Set the y scale
                        hover_name="Country", #upon hover, what is at the top of the box
                        hover_data = ["Olympics", "Continent", "Athletes"],
                        title="Change in countries over time by continent", #title of the graph
                        color_discrete_map=color_discrete_map)

#Updating the layout for the hover label. I have kept this the same across all graphs
fig.update_layout(
        hoverlabel=dict(
        bgcolor="black",
        bordercolor="black",
        font = dict(color='lightgray'),
        font_size=18,
        font_family="Rockwell"
    )
)
years = df.Year.unique().tolist()
years.sort()
#Updating the layout for the range slider. However, I cannot get some of it to work :(
fig.update_layout(
        sliders=dict(
        marks = years,
        y=3,
        yanchor="bottom",
        transition=dict(duration=50),
        bgcolor="grey"
    )
)

#The below changes the legend to change the name_of_the_column=value to just value
for trace in fig.data:
    trace.name = trace.name.split('=')[1]


#This below removes the x axis label (or changes to an empty string) from the graph (as it cannot be moved) and allows a new paper annotation to be put in that can be adjusted by x and y position.
fig.update_xaxes(title = dict(text=""))
fig.update_layout(
    annotations=[
        dict(
            x=0.5,
            y=-0.2,
            showarrow=False,
            text="Continent",
            xref="paper",
            yref="paper",
            font = dict(size=26)
        )])
#this would add in a new label for x axis


#Fonts for the graph itself eg. titles. I have kept this consistent across all graphs.
fig.update_layout(
    font=dict(family="Courier New, monospace", size=24, color="#7f7f7f"))

#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

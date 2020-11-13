## GRAPH
# Chloropleth map to reveal the % of male competitors over time since Lillehammer in 1992.
# I have used a colour scheme that allows the reader to differentiate between particpanting countries too.

#Imports
import plotly.express as px
import plotly as py
import pandas as pd
import pycountry
from clean_athlete_events_dataset import df_winter as df #import the cleaned_nation dataframe from athlete events

#Select this to True if you would like to run just this file.
view_individual_graph = False




#This method below creates the list of dicts for the values for the graph. It is then transformed into a df.
#It finds the countries, country_codes, male % of competitors for that country, num of male competitors & num of female competitors for hover labels
years = [1994, 1998, 2002, 2006, 2010, 2014]
male_percentages = []
for year in years:
    df_by_year = df[(df.Year == year)]
    countries_of_year = df_by_year.cleaned_nation.unique().tolist()
    for country in countries_of_year:
        df_by_year_by_country = df_by_year[(df_by_year.cleaned_nation == country)]
        country_code = df_by_year_by_country['NOC'].iloc[0]
        total_competitors = len(df_by_year_by_country)
        male_competitors = len(df_by_year_by_country[(df_by_year_by_country.Sex == "M")])
        male_percentage = (male_competitors / total_competitors)* 100
        details = {"Country": country,
                    "Year": year,
                    "country_code": country_code,
                    "Male Percentage %": round(male_percentage, 1),
                    "Male Competitors": male_competitors,
                    "Female Competitors": total_competitors - male_competitors
                    }
        male_percentages.append(details)

#Convert to dataframe
gender_percentage_df = pd.DataFrame(male_percentages)

#Create chlorpleth map
fig = px.choropleth(gender_percentage_df,
                    locations="country_code",
                    color="Male Percentage %",
                    hover_name="Country",
                    hover_data=["Year", "Female Competitors", "Male Competitors", "Male Percentage %"],
                    animation_frame="Year",
                    color_continuous_scale=[[0, 'red'], [0.5, 'yellow'], [1.0, 'green']],
                    title="Male % Distribution by Country since 1994 Olympics in Lillehammer, Norway",
                    width=2000,
                    height=1000
                    )

#Further details for the map itself
fig.update_layout(geo=dict(
    showframe=True,
    showcoastlines=False,
    projection_type='natural earth')) #I like this look, it presents it as more of a globe and therefore I beleive avoids the mis-representation that flat maps give for country size
fig.update_geos(resolution=50) #shows a greater resolution, looks more realistic

#Label hovering settings
fig.update_layout(
        hoverlabel=dict(
        bgcolor="black",
        bordercolor="black",
        font = dict(color='lightgray'),
        font_size=18,
        font_family="Rockwell"))

#General map text font label settings
fig.update_layout(
    font=dict(family="Courier New, monospace", size=24, color="#7f7f7f"))

#function for seeing the graph on it's own
if (view_individual_graph):
    fig.show()

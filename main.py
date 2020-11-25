## Imports
from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import os
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import pandas as pd
import json

#importing graphs and cleaning dataset scripts if needed
from height_or_weight_per_event_over_time import sports, events, medals, df_filtered, return_filtered_frame, medal_settings, years
from gender_distribution_per_sport_over_time import fig as fig_gender_distribution
from stacked_bar_chart_medals import fig as fig_stacked_bar_chart_medals
from total_events_over_time import fig as fig_events_over_time
from clean_winter_olympic_medals_data import sports_and_events, messages #for the dropdown boxes sports and events
from gender_distribution_map import fig as fig_map_gender_distribution
# from old_sports_new_nations import fig as fig_new_sports_new_nations
# from continent_representation_over_time import fig as fig_continent_graph
# from working_example_1_animation_gender_graph import fig as fig_working_graph_example_one

#Flask settings.
debug_mode = False #remember in debug mode, it initalises twice
secret_key = 'verysecretkey123lol' #secret key for Flash
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Just in case the strip function is needed
for sport in sports:
    sport = sport.strip()

#Creating the plot for the Height and Weight graphs.
def create_plot(sport, event, measure):
    #setting the axis
    if measure == "height":
        y_axis_title = "Height (cm)"
    else:
        y_axis_title = "Weight (kg)"

    #Creating the traces for the heights and weights graph by iterating through the medals imported in.
    data = []
    i = 0
    for medal in medals:
        frame = return_filtered_frame(medal, sport, event, years)[0]
        if_average = return_filtered_frame(medal, sport, event, years)[1]
        trace = go.Scatter(x = frame['Year'], y = frame[measure.capitalize()], name = medal, mode="markers+lines", showlegend = True, hovertext=frame['Name'] + " of " + frame['Team'], marker=dict(color=medal_settings[i][2], size=medal_settings[i][1], line=dict(color=medal_settings[i][2],width=2)) )
        data.append(trace)
        i += 1

    #Creating the figure itself
    fig = go.Figure(data = data)
    fig.update_layout(title= "Medal by " + if_average + measure.capitalize() + " for " + sport + ": " + event, xaxis_title="Olympics", yaxis_title = y_axis_title,font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
    fig.update_layout(hovermode="closest")
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell")) #Graph label settings as used throughout the project

    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    fig.update_layout(xaxis=dict(showticklabels=True, type='category'), width=1900)
    fig.update_layout( #Hover label settings as used throughout the project
        hoverlabel=dict(
            bgcolor="black",
            bordercolor="black",
            font = dict(color='lightgray'),
            font_size=18,
            font_family="Rockwell"))

    #General figure setting updates to make the graph look a little more clearer
    fig.update_layout(
        yaxis = dict(rangemode = "tozero"))
    fig.update_layout(
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4))

    #Get graph ready so can be added to Flask interface
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

#Function for associating apropiate message with sport for Heights and Weights graph. This is referred to in the report.
def find_message(messages, sport):
    message = []
    for item in messages:
        if item['sport'] == sport:
            msg = item['message']
            message.append(msg)
    return message

#When the Flask app runs, this runs with the Get Request and Post Request if the reader wants to take a little look at the Heights and Weights
@app.route("/", methods=['GET', 'POST'])
#For when the reader wants to see a height or weight
def create():
    if request.method == 'POST':
        sport = request.form['sport']
        event = request.form['sport_event']
        height_graph = create_plot(sport, event, "height")
        weight_graph = create_plot(sport, event, "weight")
        message = find_message(messages, sport)
        #Otherwise I have posted the details for Luge. I would love to try it someday!
    else:
        sport = 'Luge'
        event = '''Men's singles'''
        height_graph = create_plot(sport, event, "height")
        weight_graph = create_plot(sport, event, "weight")
        message = find_message(messages, sport)

        #Ensure the graphs are ready for the Flask interface
    # continent_graph = json.dumps(fig_continent_graph, cls=plotly.utils.PlotlyJSONEncoder)
    gender_distribution_graph = json.dumps(fig_gender_distribution, cls=plotly.utils.PlotlyJSONEncoder)
    stacked_bar_chart_medals = json.dumps(fig_stacked_bar_chart_medals, cls=plotly.utils.PlotlyJSONEncoder)
    events_over_time_graph = json.dumps(fig_events_over_time, cls=plotly.utils.PlotlyJSONEncoder)
    map_gender_distribution = json.dumps(fig_map_gender_distribution, cls=plotly.utils.PlotlyJSONEncoder)
    # new_sports_new_nations_chart = json.dumps(fig_new_sports_new_nations, cls=plotly.utils.PlotlyJSONEncoder)
    # working_graph_example_one = json.dumps(fig_working_graph_example_one, cls=plotly.utils.PlotlyJSONEncoder)

    #Render the template for Flask using index.html
    return render_template('index.html',
                        sports_events = sports_and_events,
                        height_graph=height_graph,
                        weight_graph=weight_graph,
                        message = message,
                        sports = sports,
                        # continent_graph = continent_graph,
                        gender_distribution_graph=gender_distribution_graph,
                        medals_per_country_graph=stacked_bar_chart_medals,
                        events_over_time_graph=events_over_time_graph,
                        map_gender_distribution = map_gender_distribution,
                        # new_sports_new_nations_chart = new_sports_new_nations_chart,
                        # working_graph_example_one = working_graph_example_one,
                        )

#Run
if __name__ == "__main__":
    app.secret_key = secret_key
    app.run(debug = debug_mode)

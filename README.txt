##This is the README for Winter Olympics Analysis Data Visualisation ##

#I have had a look into representing Winter Olympic data through Data Visualisation using the following datasets: 

Source: Korda, J. Summer & Winter Olympics [Online]. [Accessed 06 March 2020]. Available at:https://data.world/johayes13/summer-winter-olympic-games
Source: @vizwiz 2018/W7: The Winter Olympics [Online]. [Accessed 28 March 2020]. Available at:https://data.world/makeovermonday/2018w7-the-winter-olympics
I have included these in the repo

STRUCTURE OF & VIEWING THE VISUALISATIONS
- Run the presentation through main.py
- This will present you with an interface that has taken advantage of the Flask framework. 
- I use the plotly graphing library for something different - I have often used Matplotlib before now.


IMPORTS USED
- Below are the imports I have used and would be best to have installed to be able to run the main.py file, all graph and cleaning data files

import plotly.graph_objects
import plotly.express
import plotly
import pandas
import csv
import random
import time
import pycountry_convert
import pycountry
import re
from flask import Flask, render_template, request
import os
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

OPENING INDIVIDUAL GRAPH FILES
- If you would like to open individual graphs as seperate files, outside the Flask interface, then this is possible. Please note though, this is not recommended
as will not follow the story and themes as discussed in the report.

1. Enter the individual file
2. Select view_individual_graph to true
3. Run graph


CSV FILES USED
- The two links below are too the CSV files within Data World however, their CSV files should already be in the .zip dir
# File referenced as athletes_events, reffered to as athletes and cleaned in clean_athlete_events_dataset.py : https://data.world/johayes13/summer-winter-olympic-games
# File referenced as Winter_Olympic_Medals.xlsx - Data, referred to as Olympic Medals and cleaned in clean_winter_olympic_medals_data.py : https://data.world/makeovermonday/2018w7-the-winter-olympics


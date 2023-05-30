import streamlit as st
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from sam_new_func import sam_fun as sf
import pycountry
from backend import *
from Dashboardfunctions.api_fun import *
from Dashboardfunctions.lina_viz2 import *
# from Dashboardfunctions.sam_fun2 import *


# Load the variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('YOUTUBE_API_KEY_Anvesha')
youtube = build("youtube", "v3", developerKey=api_key)

# Create an input box on the sidebar for YouTube channel name
channel_name = st.sidebar.text_input("Enter YouTube Channel Name")


st.title("AVIEW X DataRes - Channel Specific Statistics")

try:
    channel = pg2_api(youtube, channel_name)
except:
    st.write("Error: ", channel_name, " is not currently supported.")
    st.stop()

columns = ['Like Count', 'View Count', 'Comment Count']
for column in columns:
    title = 'Number of ' + column + ' on 10 Most Recent Videos'
    st.subheader(title)
    st.plotly_chart(plot_most_recent(channel, column))

st.subheader('Overall Top 5 Most Used Tags')

st.plotly_chart(plot_top_tags(channel))

st.write(channel)

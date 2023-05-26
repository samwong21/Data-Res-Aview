import streamlit as st
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from sam_new_func import sam_fun as sf



# Load the variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build("youtube","v3",developerKey=api_key)



# Fetch channel statistics
popular_channel_ids = sf.trending_creators_by_country(youtube, "US")
channel_stats = sf.channels_stats(youtube, popular_channel_ids)
st.write(channel_stats)


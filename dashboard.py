import streamlit as st
import pastfiles.trending_creator_functions as tcf
import sam_new_func.sam_fun as sf
from googleapiclient.discovery import build
# import import_ipynb
import os
from dotenv import load_dotenv
# import sam_new_func.viz_fun as viz
# from sam_new_func import *



st.title("YouTube Trending Channel Analysis")
with st.sidebar.form(key='Form1'):
    select_mode = st.radio('Viewing Mode', ('Channel', 'Video', 'Summary Statistics'))
    num_of_subs = st.number_input('Enter subscriber count', 100)
    tags = st.text_input("Enter tag filters", " ")
    filter = st.form_submit_button(label='Filter')
    # TODO: figure out how to plot top channel by subscriber decending 
    st.slider('Select the season range you want to include', 2013, 2020, (2013, 2020))
    # TODO: get countries from backend
    options = st.selectbox('Filter by countries',["United States of America", "India", "France"])
    st.write('You selected:', options)


@st.cache_data
def set_up():
    # Load the variables from the .env file
    load_dotenv()
    # Get the API key from the environment variables
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build("youtube","v3",developerKey=api_key)
    # st.write(viz.get_country_code("United States of America"))
    popular_channel_ids = sf.trending_creators_by_country(youtube, "US")
    channel_stats = sf.channels_stats(youtube, popular_channel_ids)
    channel_stats_sorted = channel_stats.sort_values(by="subscriberCount", ascending=False)
    # return channel_stats_sorted
    st.write(channel_stats_sorted.head(10))
    st.bar_chart(channel_stats_sorted.head(10), x="title", y="subscriberCount")
    # plot top 10 channels by subscriber count

    # plot View counts of the most recent 10 channels
    channel_stats_sorted = channel_stats.sort_values(by="viewCount", ascending=False)
    st.bar_chart(channel_stats_sorted.head(10), x="title", y="viewCount")

    # plot Length of videos of most recent 10 videos
    # channel_stats_sorted = channel_stats.sort_values(by="", ascending=False)
    # st.bar_chart(channel_stats_sorted.head(10), x="title", y="viewCount")


# def plot():
#     st.bar_chart(channel_stats, x="title", y="subscriberCount")
    
    

set_up()

# row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
# with row0_1:
#     st.title('BuLiAn - Bundesliga Analyzer')
# with row0_2:
#     st.text("")
#     st.subheader('Streamlit App by [Tim Denzler](https://www.linkedin.com/in/tim-denzler/)')
# row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
# with row3_1:
#     st.markdown("Hello there! Have you ever spent your weekend watching the German Bundesliga and had your friends complain about how 'players definitely used to run more' ? However, you did not want to start an argument because you did not have any stats at hand? Well, this interactive application containing Bundesliga data from season 2013/2014 to season 2019/2020 allows you to discover just that! If you're on a mobile device, I would recommend switching over to landscape for viewing ease.")
#     st.markdown("You can find the source code in the [BuLiAn GitHub Repository](https://github.com/tdenzl/BuLiAn)")
#     st.markdown("If you are interested in how this app was developed check out my [Medium article](https://tim-denzler.medium.com/is-bayern-m%C3%BCnchen-the-laziest-team-in-the-german-bundesliga-770cfbd989c7)")

# st.sidebar.markdown("**First select the data range you want to analyze:** 👇")
# start_season, end_season = st.sidebar.select_slider('Select the season range you want to include', )
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv
from sam_new_func import sam_fun as sf
from backend import *
from Dashboardfunctions.api_fun import *
from Dashboardfunctions.lina_viz2 import *
# from Dashboardfunctions.sam_fun2 import *

youtube = setup_and_getKey()

# Create an input box on the sidebar for YouTube channel name
with st.sidebar:
    if 'channel_name' in st.session_state:
        default_channel_name = st.session_state.channel_name
    else:
        default_channel_name = 'MrBeast'
    channel_name = st.text_input(
        "Enter YouTube Channel Name", value=default_channel_name)
    st.session_state.channel_name = channel_name


st.title("AVIEW X DataRes - Channel Specific Statistics")

channel = get_channel_specfic_stats(channel_name)


@st.cache_data
def visualize_channel_lina1(channel):
    columns = ['Like Count', 'View Count', 'Comment Count']
    for column in columns:
        title = 'Number of ' + column + ' on 10 Most Recent Videos'
        st.subheader(title)
        st.plotly_chart(plot_most_recent(channel, column))


visualize_channel_lina1(channel)


@st.cache_data
def visualize_channel_lina2(channel):
    st.subheader('Overall Top 5 Most Used Tags')
    st.plotly_chart(plot_top_tags(channel))


visualize_channel_lina2(channel)


st.write(channel)

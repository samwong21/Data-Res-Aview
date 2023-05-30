import streamlit as st
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from sam_new_func import sam_fun as sf
import pycountry
from backend import *
from Dashboardfunctions.api_fun import *
# from Dashboardfunctions.sam_fun2 import *


@st.cache_data
def setup():
    # Load the variables from the .env file
    load_dotenv()
    # Get the API key from the environment variables
    api_key = os.getenv('YOUTUBE_API_KEY_Anvesha')
    youtube = build("youtube", "v3", developerKey=api_key)
    return youtube


# get a list of country name to select from
country_names = []
for country in pycountry.countries:
    country_names.append(country.name)

default_index = country_names.index('United States')

with st.sidebar:
    country_name = st.sidebar.selectbox(
        'Filter channels by countries', sorted(
            country_names))
    country = get_country_code(country_name)
    st.write('You selected:', country_name, " country code: ", country)

# Title of page # TODO: Center Aligh
st.title("AVIEW X DataRes - YouTube Trending Channel Analysis")
st.subheader(
    "By: Anvesha Dutta, Proud Jiao, Eric Huang, Lina Molla, Olivia Wang, Samantha Wong, Tanya Beri")
# st.markdown(
# "By Anvesha Dutta, Proud Jiao, Eric Huang, Lina Molla, Olivia Wang, Samantha Wong, Tanya Beri")


# Fetch channel statistics # The only API call
@st.cache_data
def get_channel_stats(country):
    youtube = setup()
    try:
        homepage_df = pg1_api(youtube, country)
        return homepage_df
    except:
        st.write("Error: ", country_name, " is not currently supported.")
        st.stop()


homepage_df = get_channel_stats(country)


st.write(homepage_df)


min_subs = homepage_df['subscriberCount'].min()
max_subs = homepage_df['subscriberCount'].max()
st.write("Min subs: ", min_subs, " Max subs: ", max_subs)


# Add Filter option by subscriber count # TODO: make it dynamic later
subscriber_count = st.sidebar.slider(
    label="Filter by Subscriber Count",
    min_value=0,
    max_value=10000000,
    value=(0, 10000),
    step=1000,
)

st.write("You selected: ", subscriber_count)

st.write(between_subs(homepage_df, subscriber_count[0], subscriber_count[1]))

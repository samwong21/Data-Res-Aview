import streamlit as st
from sam_new_func import sam_fun as sf
from backend import *
from Dashboardfunctions.api_fun import *
import numpy as np


with st.sidebar:
    # region country selection dropdown
    country_names = get_country_names()
    default_index = country_names.index('United States')
    if 'country_name' in st.session_state:
        index = country_names.index(st.session_state.country_name)
    else:
        index = default_index
    selected_country_name = st.sidebar.selectbox(
        'Filter channels by countries',
        country_names, index=index, help="Some countries are not supported in YouTube API")
    st.session_state.country_name = selected_country_name
    # endregion


st.title("AVIEW X DataRes - YouTube Trending Channel Analysis")
st.subheader(
    "By: Anvesha Dutta, Proud Jiao, Eric Huang, Lina Molla, Olivia Wang, Samantha Wong, Tanya Beri")

homepage_df = get_channel_stats(selected_country_name)
st.write(homepage_df)

with st.sidebar:
    # region subscriber slider filter
    min_subs = int(homepage_df['subscriberCount'].min())
    max_subs = int(homepage_df['subscriberCount'].max())
    st.write("Min subs: ", min_subs, " Max subs: ", max_subs)
    step = int((max_subs-min_subs)/1000)
    subscriber_count = st.slider(
        label="Filter by Subscriber Count",
        min_value=min_subs,
        max_value=max_subs,
        value=(min_subs, max_subs),
        step=step,
        help="This will filter the dataframe by selected range of subscriber count"
    )
    st.write("You selected: ", subscriber_count)
    # endregion

homepage_df_filtered = between_subs(
    homepage_df, subscriber_count[0], subscriber_count[1])
st.write(homepage_df_filtered)

import numpy as np
import pandas as pd
import plotly.express as px

def avg_views(df):
    '''
    Returns average views. Works for both pages of dashboard
    '''
    return round(df["viewCount"].astype(int).mean())


def avg_subs1(homepage_df):
    """
    Returns aveerage subscriber count. Only works for page 1
    """
    return round(homepage_df["subscriberCount"].mean())


def top_topics(homepage_df):
    '''
    Returns top 5 most popular topics. Only works for page 1
    '''
    return topics_counts(homepage_df)[0:5]





##Topic visualization
#----------------------
def topic_viz_sam(homepage_df):
    topic_df = topics_counts(homepage_df)
    fig = px.bar(topic_df, y= "Topic", x = "Number of Channels", title = "Popularity of Topics",color = "Number of Channels",orientation = "h", color_continuous_scale = "Agsunset" )
    fig.show()



##Helper Functions
#----------------------

def topics_counts(homepage_df):
    '''
    returns a dataframe with "Topic" and "Number of Channels" column. Shows the number of times each topic appears
    
    '''
    index = []
    for i in homepage_df["topic"]:
        x = i is not None
        index.append(x) 
    topic_counts = homepage_df["topic"][index].explode().value_counts()
    topic_df = pd.DataFrame({"Topic" : topic_counts.index, "Number of Channels" :topic_counts.values })
    return topic_df
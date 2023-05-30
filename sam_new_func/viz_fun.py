import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import re
from sam_new_func.sam_fun import *
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import math
from datetime import datetime, timedelta

api_key = "AIzaSyBqgqP0nQ-qP4LJc4_kytQTERSq-pXOff0" # you can change it to your own api 

########## scraping from https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#AA############
def get_country_code(country_name):
    
    """
    input a country name, output a country code
    """
    url = "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#AA"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    tables = soup.find_all("table", class_="wikitable")
    dfs = []

    for table in tables:
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cells = row.find_all("td")
            if cells:
                # add the contents of each cell to the data list
                row_data = []
                for cell in cells:
                    row_data.append(cell.get_text().strip())
                data.append(row_data)
        # create a pandas dataframe from the data list and add it to the dfs list
        df = pd.DataFrame(data)
        dfs.append(df)


    countries = dfs[2].iloc[:, 0:2]
    countries = countries.rename(columns={0: 'code', 1: 'country'})
    country_index = countries[countries.country == country_name].index[0]
    country_code = countries.code[country_index]
    
    return country_code
    
def plot_top_channels(country, column, top_percentile):
    """
    returns a df with top percentile Youtube channels in a specific country:
    
    @country: a string for the name of the country
    @column: a string for the column to define "top"; 
            3 options: 'Subscriber Count', 'View Count', 'Video Count'
    @top_percentile: a double or integer indicating what percentile of creators, 
                    e.g. 5 is top 5% of creators
    """
    country_code = get_country_code(country) # switch the country name into country code
    if column == 'Subscriber Count':
        df_column = 'subscriberCount'
    elif column == 'View Count':
        df_column = 'viewCount'
    elif column == 'Video Count':
        df_column = 'videoCount'
        
    youtube = build("youtube","v3", developerKey=api_key)
    creator_ids= trending_creators_by_country(youtube, country_code)
    stats_df = channels_stats(youtube, creator_ids)
    stats_df = add_emails(stats_df)
    #top5 = in_stats_df.sort_values(df_column, ascending = False).head(5)
    top_channels_df = top_channels(stats_df, df_column, (100 - top_percentile))
     
    #text_labels = [f'{value}' for value in top5[df_column]] 
    legend_labels = [f'{email}' for email in top_channels_df.emails]
    fig = px.bar(top_channels_df, x = 'title', y = df_column,
            title = 'Top ' + str(top_percentile) + ' Percentile Youtube Channels in\n' + ' ' + 
                 country + ' ' + 'Based on' + ' ' + column,
            hover_data = ['title', 'country', 'viewCount', 'subscriberCount', 'videoCount'],
            color = legend_labels) # text_labels?
    
    fig.update_layout(xaxis_title = 'Channels', yaxis_title= column)
    fig.update_layout(legend_title_text='Legend Title', 
                      legend=dict(title='Emails', x=0, y=-1.2, orientation='h'))
    return fig
    
###############################################################################    
    
def get_channel_id(channel_title):
    """
    input channel title, output its channel id
    
    @channel_title: a string for the title of a Youtube channel
    """
    youtube = build('youtube', 'v3', developerKey = api_key)
    search_response = youtube.search().list(
        q=channel_title,
        part='id',
        type='channel',
        maxResults=1
    ).execute()

    channel_id = search_response['items'][0]['id']['channelId']
    
    return channel_id
   
    
def plot_top_tags_wordcloud(channel_title):
    """
    input a channel title, plot the wordcloud of the tags of the videos in this channel
    
    @channel_title: a string for the title of a Youtube channel
    """
    
    youtube = build('youtube', 'v3', developerKey = api_key)
    channel_id = get_channel_id(channel_title)
    video_id = get_videoID_list(youtube, channel_id)
    df = get_video_details(youtube,video_id)

    tag_lists = df['tags']
    combined_tag_lists = [item for sublist in tag_lists for item in sublist]

    text = ' '.join(combined_tag_lists)

    wordcloud = WordCloud(background_color="white").generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
############################################################################### 

def convert_duration(durations):
    """
    converts the durations column into minutes
    
    @durations: the duration column
    """
    minutes_list = []
    
    for duration in durations:
        # check if duration string is empty
        if not duration:
            minutes_list.append(0)
            continue
        
        # check if duration string contains 'D', the ones with 'D' considered as an outlier
        if 'D' in duration:
            minutes_list.append(math.nan)
            continue
        
        duration = duration.strip('PT')  # Remove 'PT'
        
        # check if the duration string contains valid duration information
        if 'M' not in duration and 'S' not in duration:
            minutes_list.append(0)
            continue
        
        total_minutes = 0
        hours_index = 0  
        minutes_index = 0
        
        if 'H' in duration:
            hours_index = duration.index('H')
            hours = int(duration[:hours_index])
            total_minutes += hours * 60
        
        if 'M' in duration:
            minutes_index = duration.index('M')
            if minutes_index > hours_index:  # check if minutes exist
                try:
                    minutes = int(duration[hours_index+1:minutes_index])
                    total_minutes += minutes
                except ValueError:
                    pass
        
        if 'S' in duration:
            seconds_index = duration.index('S')
            if 'M' in duration and minutes_index > hours_index:
                try:
                    seconds = int(duration[minutes_index+1:seconds_index])
                    total_minutes += seconds / 60
                except ValueError:
                    pass
            elif 'H' in duration:
                try:
                    seconds = int(duration[hours_index+1:seconds_index])
                    total_minutes += seconds / 60
                except ValueError:
                    pass
            else:
                try:
                    seconds = int(duration[:seconds_index])
                    total_minutes += seconds / 60
                except ValueError:
                    pass
        
        minutes_list.append(round(total_minutes, 2))
    
    return minutes_list


def plot_tag_duration(channel_title):
    """
    input a channel title, plot the bubble plot of the video duratioin for x axis, view count for y axis, and the number of tags for the size of bubbles
    
    @channel_title: a string for the title of a Youtube channel
    """
    youtube = build('youtube', 'v3', developerKey = api_key)
    channel_id = get_channel_id(channel_title)
    video_id = get_videoID_list(youtube, channel_id)
    df = get_video_details(youtube,video_id)

    tag_lists = df['tags']
    tag_len = []
    for tag in tag_lists:
        length = len(tag)
        tag_len.append(length)

    df['tag_len'] = tag_len
    df['du_min'] = convert_duration(df['duration'])

    df = df[df['du_min'] < 200] # exclude outliers
    tag_view_du = df.groupby('tag_len')[['viewCount', 'du_min']].aggregate([np.mean, np.median]).reset_index()
    #bubble map
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(data = tag_view_du, 
                    x = tag_view_du['du_min']['median'],
                    y = tag_view_du['viewCount']['median'], 
                    size = tag_view_du['tag_len'],
                    legend=False, sizes=(20, 500), alpha = 0.5)

    ax.set_xlabel('Median Duration (min)')
    ax.set_ylabel('Median View Count')
    ax.set_title('The number of tags V.S. Duration')
    plt.show()



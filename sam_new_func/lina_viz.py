import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import re
from collections import Counter
from sam_fun import *
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

###############################################################################
def plot_top_channels(country, column, percentile):
    """
    returns a df with top percentile Youtube channels in a specific country:
    
    @country: a string for the name of the country
    @column: a string for the column to define top 5; 
            3 options: 'Subscriber Count', 'View Count', 'Video Count'
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
    top_channels_df = top_channels(stats_df, df_column, percentile)
     
    #text_labels = [f'{value}' for value in top5[df_column]] 
    legend_labels = [f'{email}' for email in top_channels_df.emails]
    fig = px.bar(top_channels_df, x = 'title', y = df_column,
            title = 'Top ' + str(100 - percentile) + ' Percentile Youtube Channels in' + ' ' + 
                 country + ' ' + 'Based on' + ' ' + column,
            hover_data = ['title', 'country', 'viewCount', 'subscriberCount', 'videoCount'],
            color = legend_labels) # text_labels?
    
    fig.update_layout(xaxis_title = 'Channels', yaxis_title= column)
    fig.update_layout(legend_title_text='Legend Title', 
                      legend=dict(title='Emails', x=0, y=-1.2, orientation='h'))
    fig.show()
    
###############################################################################    
def plot_most_recent(user, column):
    """
    returns a df with the specified statistics of most recent 10 Youtube channel's videos:
    
    @user: a string for the user id of the channel
    @column: a string for the column to define top 10; 
            3 options: 'Like Count', 'View Count', 'Video Length'
    """
    if column == 'Like Count':
        df_column = 'likeCount'
    elif column == 'View Count':
        df_column = 'viewCount'
    elif column == 'Video Length':
        df_column = 'videoLength'
        
    youtube = build("youtube","v3", developerKey=api_key)
    in_stats_df = channels_stats(youtube,[user])
    video_ids = get_videoID_list(youtube,user)
    video_stats = get_video_details(youtube,video_ids)
    most_recent10 = video_stats.head(10)
     
    fig = px.bar(most_recent10, x = 'title', y = df_column,
            title = column + '\'s of ' + in_stats_df.title[0] + '\'s 10 Most Recent Videos',
            hover_data = ['title', df_column])
    
    fig.update_layout(xaxis_title = 'Video', yaxis_title= column)
    # fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.show()
###############################################################################    
def plot_top_tags(user):
    """
    returns a df of the top 5 tags used by a specified channel:
    
    @user: a string for the user id of the channel
    """
        
    youtube = build("youtube","v3", developerKey=api_key)
    in_stats_df = channels_stats(youtube,[user])
    video_ids = get_videoID_list(youtube,user)
    video_stats = get_video_details(youtube,video_ids)
    top_tags = top_tags_modified(list(video_stats.tags))
    
    tags = [tag for tag, _ in top_tags]
    counts = [count for _, count in top_tags]
    
    fig = px.bar(x = tags, y = counts,
                 title = 'Top Tags used by ' + in_stats_df.title[0],
                 hover_data = [tags, counts])
    
    fig.update_layout(xaxis_title = 'Tags', yaxis_title= 'Counts')
    fig.show()
###############################################################################    
def top_tags_modified(tags_list):
    """
    MODIFIED helper function for plot_top_tags and returns the top 5 tags and their number of occurrences for a specific channel
    
    @tags_list: a list of lists of tags for all the tags used by a specific channel
    """
    all_strings = [string for sublist in tags_list for string in sublist]
    string_counts = Counter(all_strings)
    if len(string_counts) >= 5:
        top_tags = string_counts.most_common(5)
    else:
        top_tags = string_counts.most_common(len(string_counts))
    return top_tags
############################################################################### 
def top_tags(tags_list):
    """
    helper function for plot_top_tags and returns the top 5 tags and their number of occurrences for a specific channel
    
    splits each list nested within the lists items into individual words
    
    @tags_list: a list of lists of words for all the tags used by a specific channel
    """
    word_pattern = re.compile(r'\b\w+\b')  # Matches individual words
    
    all_words = []
    for sublist in tags_list:
        all_words.extend(word_pattern.findall(' '.join(sublist)))

    word_counts = Counter(all_words)
    if len(all_words) >= 5:
        top_tags = word_counts.most_common(5)
    else:
        top_tags = word_counts.most_common(len(all_words))
    
    return top_tags
###############################################################################    
   


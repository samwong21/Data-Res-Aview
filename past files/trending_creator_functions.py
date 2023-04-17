import pandas as pd
import requests
import numpy as np
from googleapiclient.discovery import build

def get_channel_data(youtube, channel_ids):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,topicDetails,status",
        id=','.join(channel_ids)
    )
    response = request.execute()
    
    all_data = []
    
    for i in range(len(np.unique(channel_ids))):
    
        channel = response['items'][i]

        channel_data = {}
        
        try:
            channel_data['channel_id'] = channel['id']
            channel_data['channel_name'] = channel['snippet']['title']
            channel_data['channel_desc'] = channel['snippet']['description']
            channel_data['channel_start_date'] = channel['snippet']['publishedAt']
            channel_data['total_views'] = channel['statistics']['viewCount']
            channel_data['total_subscribers'] = channel['statistics']['subscriberCount']
            channel_data['total_videos_posted'] = channel['statistics']['videoCount']
            channel_data['channel_country'] = channel['snippet']['country']
            channel_data['channel_topic'] = channel['topicDetails']['topicCategories']
        except:
            channel_data['channel_id'] = None
            channel_data['channel_name'] = None
            channel_data['channel_desc'] = None
            channel_data['channel_start_date'] = None
            channel_data['total_views'] = None
            channel_data['total_subscribers'] = None
            channel_data['total_videos_posted'] = None
            channel_data['channel_country'] = None
            channel_data['channel_topic'] = None
        
        all_data.append(channel_data)
        
    return pd.DataFrame(all_data)

def get_trending_american_creators_in_country(youtube, country):
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=country,
        maxResults = 50
    )
    response = request.execute()

    channel_ids = [response['items'][i]['snippet']['channelId'] for i in range(50)]

    all_data = []
    for i in range(50):
        video = response['items'][i]
        
        video_data = {}
        try:
            video_data['video_id'] = video['id']
            video_data['channel_id'] = video['snippet']['channelId']
            video_data['video_posting_date'] = video['snippet']['publishedAt']
            video_data['video_title'] = video['snippet']['title']
        except:
            video_data['video_id'] = None
            video_data['channel_id'] = None
            video_data['video_posting_date'] = None
            video_data['video_title'] = None
        all_data.append(video_data)
    
    df_video = pd.DataFrame(all_data)
    df_channels = get_channel_data(youtube, channel_ids)
    df_channels = df_channels[df_channels.channel_country.isin(['US', 'CA', 'MX'])]
    return df_video.merge(df_channels, on='channel_id')

def get_trending_american_creators(youtube, country_list):
    '''
    country_list: a list containing the ISO 3166-1 alpha-2 code for relevent countries.
        // find country code at: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    '''
    df_countries = pd.DataFrame()
    for country in country_list:
        df_country = get_trending_american_creators_in_country(youtube, country)
        df_country['trending_country'] = country
        df_countries = pd.concat([df_countries, df_country])
    return df_countries
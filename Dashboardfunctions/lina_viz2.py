import requests
# from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import re
from collections import Counter
# import plotly.graph_objects as go
api_key = 'AIzaSyDSz4TNw2LDHmdotHZoZb90Oe06z8FOC2Y'
# "AIzaSyBqgqP0nQ-qP4LJc4_kytQTERSq-pXOff0" # can change it to your own api
###############################################################################


def plot_most_recent(df, column):
    """
    plots the specified statistics of the most recent 10 Youtube channel's videos:

    @df: a channel specific data frame
    @column: a string specifying the column to define top 10; 
            3 options: 'Like Count', 'View Count', 'Comment Count'
    """
    if column == 'Like Count':
        df_column = 'likeCount'
        col = 'Likes'
    elif column == 'View Count':
        df_column = 'viewCount'
        col = 'Views'
    elif column == 'Comment Count':
        df_column = 'commentCount'
        col = 'Comments'

    # youtube = build("youtube","v3", developerKey=api_key)
    # in_stats_df = channels_stats(youtube,[user])
    # video_ids = get_videoID_list(youtube,user)
    # video_stats = get_video_details(youtube,video_ids)
    # most_recent10 = video_stats.sort_values("published", ascending = False).head(10)
    # most_recent10[df_column] = most_recent10.loc[:,df_column].astype(int)
    most_recent10 = df.sort_values('published', ascending=False).head(10)
    most_recent10[df_column] = most_recent10.loc[:, df_column].astype(int)

    fig = px.bar(most_recent10, x='title', y=df_column, hover_name='title',
                 hover_data={'title': False, df_column: True}, color_discrete_sequence=['#d62728'])

    fig.update_layout(xaxis_title='Video', yaxis_title=col)

    # fig.update_layout(
    #     xaxis = dict(
    #         tickmode = 'array',
    #         tickvals = list(range(0,10)),
    #         ticktext = [most_recent10.title[0][:len(most_recent10.title[0])//2] + '...',
    #                     most_recent10.title[1][:len(most_recent10.title[1])//2] + '...',
    #                     most_recent10.title[2][:len(most_recent10.title[2])//2] + '...',
    #                     most_recent10.title[3][:len(most_recent10.title[3])//2] + '...',
    #                     most_recent10.title[4][:len(most_recent10.title[4])//2] + '...',
    #                     most_recent10.title[5][:len(most_recent10.title[5])//2] + '...',
    #                     most_recent10.title[6][:len(most_recent10.title[6])//2] + '...',
    #                     most_recent10.title[7][:len(most_recent10.title[7])//2] + '...',
    #                     most_recent10.title[8][:len(most_recent10.title[8])//2] + '...',
    #                     most_recent10.title[9][:len(most_recent10.title[9])//2] + '...',]
    #     )
    # )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(0, 10)),
            ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        )
    )

    fig.update_layout(hovermode="x")
    fig.update_layout(autosize=False,
                      width=1000,
                      height=500,
                      margin=dict(l=100, r=100, t=100, b=100))
    return fig
###############################################################################


def plot_top_tags(df):
    """
    plots the top 5 tags used of a specified channel:

    @df: a channel specific data frame
    """

    # youtube = build("youtube","v3", developerKey=api_key)
    # in_stats_df = channels_stats(youtube,[user])
    # video_ids = get_videoID_list(youtube,user)
    # video_stats = get_video_details(youtube,video_ids)
    # top_tags = top_tags_modified(list(video_stats.tags))
    top_tags = top_tags_modified(list(df.tags))

    tags = [tag for tag, _ in top_tags]
    counts = [count for _, count in top_tags]
    df = pd.DataFrame({'tag': tags, 'count': counts})

    # fig = go.Figure()
    # fig.add_trace(go.Bar(x = df['tag'], y = df['count']))
    # fig.add_trace(go.Scatter(x = df['tag'], y = df['count']))

    fig = px.bar(df, x='tag', y='count', hover_name='tag',
                 hover_data={'tag': False, 'count': True}, color_discrete_sequence=['#d62728'])

    fig.update_layout(hovermode="x")
    fig.update_layout(
        xaxis_title='Tags', yaxis_title='Counts', showlegend=False)

    fig.update_layout(autosize=False,
                      width=1000,
                      height=500,
                      margin=dict(l=100, r=100, t=100, b=100))
    return fig
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

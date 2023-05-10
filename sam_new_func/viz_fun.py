import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import re
from sam_fun import *
api_key = "AIzaSyA-wrB_ng2gBm3Oac1RJXnLimDSE2mUsQY" # you can change it to your own api 

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
def plot_top_five_channels(country, column):
    """
    returns a df with top 5 Youtube channels in a specific country:
    
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
    in_creator_ids= trending_creators_by_country(youtube, country_code)
    in_stats_df = channels_stats(youtube,in_creator_ids)
    in_stats_df = add_emails(in_stats_df)
    top5 = in_stats_df.sort_values(df_column, ascending = False).head(5)
     
    #text_labels = [f'{value}' for value in top5[df_column]] 
    legend_labels = [f'Emails: {email}' for email in top5.emails]
    fig = px.bar(top5, x = 'title', y = df_column,
            title = 'Top 5 Youtube Channels in' + ' ' + country + ' ' + 'Based on' + ' ' + column,
            hover_data = ['title', 'country', 'viewCount', 'subscriberCount', 'videoCount'],
            color = legend_labels) # text_labels?
    
    fig.update_layout(xaxis_title = 'Channels', yaxis_title= column)
    fig.update_layout(legend_title_text='Legend Title', legend=dict(title='Groups'))
    fig.show()
    
###############################################################################    
    
    
    
    

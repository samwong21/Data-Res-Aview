import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import plotly.express as px
import re
from collections import Counter
from sam_fun import *
import plotly.graph_objects as go
api_key = "AIzaSyB8eESdFrPrh6NRNN6Cbs_8lc6ksv4oNAo" # you can change it to your own api 


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

## Functions to obtain trending category

def get_trending_videos(country):
    country_code = get_country_code(country)
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode=country_code
    )
    response = request.execute()
    videos = response['items']

    return videos

def get_category_name(category_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videoCategories().list(
        part='snippet',
        id=category_id
    )
    response = request.execute()
    category = response['items'][0]
    category_name = category['snippet']['title']

    return category_name

def count_trending_categories(videos):
    categories = {}
    for video in videos:
        categoryId = video['snippet']['categoryId']
        if categoryId in categories:
            categories[categoryId] += 1
        else:
            categories[categoryId] = 1

    return categories

def get_top_trending_categories(country):
    videos = get_trending_videos(country)
    categories = count_trending_categories(videos)
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    top_categories = []
    for category_id, channel_count in sorted_categories:
        category_name = get_category_name(category_id)
        top_categories.append((category_name, channel_count))
    return top_categories

def visualize_top_categories(country):
    top_categories = get_top_trending_categories(country)
    category_names = [category[0] for category in top_categories]
    channel_counts = [category[1] for category in top_categories]

    fig = go.Figure(data=[
        go.Bar(x=category_names, y=channel_counts, marker_color = 'rgb(180, 0, 0)')
    ])

    fig.update_layout(
        title='Top Trending YouTube Channel Categories',
        xaxis_title='Category',
        yaxis_title='Number of Channels'
    )

    fig.show()







    




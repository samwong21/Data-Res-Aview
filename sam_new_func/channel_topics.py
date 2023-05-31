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

def popular_categories_by_country(country):
    youtube = build('youtube', 'v3', developerKey=api_key)
    country_code = get_country_code(country)
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode=country_code,
        hl='en-US'
    )
    response = request.execute()
    categories = response['items']

    category_names = []
    video_counts = []
    for category in categories:
        category_names.append(category['snippet']['title'])
        video_counts.append(category['snippet']['channelStatistics']['videoCount'])

    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(x=category_names, y=video_counts)
    ])

    fig.update_layout(
        title='Popular YouTube Channel Categories in {}'.format(country),
        xaxis_title='Category',
        yaxis_title='Number of Channels'
    )

    fig.show()







    




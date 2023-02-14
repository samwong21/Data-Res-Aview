
def get_channel_stats(youtube,channel_id):
    '''
    Gets list of items from youtube api
    '''
    request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id = channel_id
    )
    response= request.execute()
    
    # get only stats from"items" key
    return response['items']
    

def stats_loc_name(channel_stats):
    '''
    Uses return from get_channel_stats to pull out view count, subscriber count, video count, user name of channel, and location of creator
    
    channel_stats: return object from get_channel_stats
    '''
    stats = channel_stats[0]["statistics"]
    country = channel_stats[0]["snippet"]["country"]
    title = channel_stats[0]["snippet"]["title"]
    return stats,country,title 
    
    
    
def get_video_list(youtube, upload_id):
    '''
    Grabs unique ID for every video on a channel
    
    youtube: youtube API build()
    upload_id: unique ID for playlist of every video on channel
    
    Returns:list of unique ID of
    '''
    video_list = []
    request = youtube.playlistItems().list(
        part = "snippet,contentDetails",
        playlistId = upload_id,
        maxResults = 50 # most results you can get on one page from API is 50
    )
    next_page = True #when False means no more pages
    
    while next_page: #as long as next_page is true, it will keep searching for results
        response = request.execute()
        data = response['items']
        
        for video in data:
            video_id = video["contentDetails"]["videoId"] #for each video result, look into content details then in that get video ID
            if video_id not in video_list:
                video_list.append(video_id)
        if "nextPageToken" in response.keys(): #if in JSON theres a nextPageToken, it means there are more responses
            next_page = True
            request = youtube.playlistItems().list(
                part = "snippet,contentDetails",
                playlistId = upload_id,
                maxResults = 50,
                pageToken = response['nextPageToken']#gets next page of results           
            )
        else:
            next_page = False #exits the while loop
    return video_list



def get_video_details(youtube,video_list):
    '''
    Grabs data for all videos in a channel
    
    youtube: youtube API build()
    video_list: list containing all unique video IDs of data you want to grab
    
    returns: a list of dictionaries, each dictionary contains stats for a unique video
    
    '''
    stats_list = []
    all_stats = []
    #because YT only lets you grab 50 videos at a time
    #need to jump 0-49, 50-99 etc (count by 50)

    for i in range(0,len(video_list),50):
        request = youtube.videos().list(
            part = "snippet,contentDetails,statistics",
            id = video_list[i:i+50] #non inclusive, will grab 0-49
        )
        
        data = request.execute()
        
        for video in data["items"]:
            
            title = video["snippet"]['title']
            published = video['snippet']['publishedAt']
            description = video['snippet']['description']
            tags = video["snippet"].get('tags',[]) #how many tags video has bc 'tags' is a list
            
            # .get ensures that if the info is unavailable (private etc), it won't throw an error, but put 0
            view_count = video["statistics"].get("viewCount",0)
            like_count = video["statistics"].get("likeCount",0)
            dislike_count = video["statistics"].get("dislikeCount",0)
            comment_count = video["statistics"].get("commentCount",0)
             
            #makes dictionary for each video with stas
            stats_dictionary = dict(title=title, 
                                    published=published,
                                    description = description,
                                    tags = tags,
                                    view_count = view_count,
                                    dislike_count = dislike_count,
                                    comment_count = comment_count
            )
            stats_list.append(stats_dictionary)
            
    return stats_list
    
    


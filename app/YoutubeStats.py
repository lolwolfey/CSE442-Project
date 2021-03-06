"""The google developers website offers guides for most of their methods here:
https://developers.google.com/youtube/v3/quickstart/python

additionally the GitHub can be found here:
https://github.com/googleapis/google-api-python-client

A YouTube video that explains how to obtain videos from a youtube page and separate the data on them using .channels() .playlistItems and .videos() from the YouTube api
https://www.youtube.com/watch?v=2mSwcRb3KjQ

A webpage that explains the basic use of matplot.pyplot for python which we are using to present our data from the YouTube page
https://matplotlib.org/stable/tutorials/introductory/pyplot.html

Overview for using .videos()
https://developers.google.com/youtube/v3/docs/videos

Overview for using .playlistitems
https://developers.google.com/youtube/v3/docs/playlistItems

Overview for using .channels()
https://developers.google.com/youtube/v3/docs/channels
"""
api_key2 = 'AIzaSyDZOWswxfehV6Abt8a0qVZkvW3OJnU41n8'


import os
import matplotlib.pyplot as plt

from googleapiclient.discovery import build

def WeeklyViewerCount(Chann_Id):

    # Should hide this key for real world use.
    api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'

    youtube = build('youtube', 'v3', developerKey=api_key)

    #The id is the YouTube id for CNN https://www.youtube.com/channel/UCupvZG-5ko_eiXAupbDfxWw
    request = youtube.channels().list(
        part='snippet, contentDetails,statistics',
        id = Chann_Id,
    )
    #data from the youtube channel
    response = request.execute()


    channel_stats = response['items']  # items key here gets channel resources/stats dictionary:  https://developers.google.com/youtube/v3/docs/channels#resource

    #gets the upload id of the youtube account so that we can access their videos: https://developers.google.com/youtube/v3/docs/playlistItems/list
    upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']

    video_list = []

    #requests the 50 most recent videos uploaded by the youtube page using their upload_id. This is limited to 50 ids for request.
    request = youtube.playlistItems().list( #https://developers.google.com/youtube/v3/docs/playlistItems/list
        part="snippet,contentDetails",
        playlistId=upload_id,
        maxResults = 7     #50 is max amount per request, suggest changing it to 7
    )
    response = request.execute()

    #Gets the videoId of each video so that we can access the data on each video
    data = response['items'] #https://developers.google.com/youtube/v3/docs/playlistItems#resource 
    for video in data:
        video_id = video['contentDetails']['videoId']
        if video_id not in video_list:
            video_list.append(video_id)
    print(video_list)
    print(len(video_list))

    stats_list = []

    #Requests the statistics on each video from our Video_list
    request = youtube.videos().list( #https://developers.google.com/youtube/v3/docs/videos/list
        part = "snippet,contentDetails,statistics",
        id = video_list[0:50]
    )
    data = request.execute()

    for video in data['items']: # array of video resources
        published = video['snippet']['publishedAt'] #get publish date of a video
        views = video['statistics'].get('viewCount',0) #get total views of a video, if not exist then 0
        likes = video['statistics'].get('likeCount', 0) #get total likes of a video, if not exist then 0
        dislikes = video['statistics'].get('dislikeCount', 0) #get total dislikes of a video, if not exist then 0
        stats_dictionary = dict(
            published = published,
            views = views,
            likes = likes,
            dislikes = dislikes
        )
        stats_list.append(stats_dictionary)
    print(stats_list)

    view_list = []
    published = []
    likelist = []
    dislikelist =[]
    for vid in stats_list:
        view_list.insert(0,(int(vid['views'])/1000000)) #VIEWS, inserted at head
        pub = vid['published']
        pub = pub.split('-')
        month = pub[1]
        day = pub[2].split('T')
        day = day[0]
        published.insert(0,vid['published']) #date inserted at head
        likelist.insert(0,(int(vid['likes'])/1000)) #dislikes amounts
        dislikelist.insert(0,(int(vid['dislikes'])/1000)) 

    print(view_list)

    graphlists = [published, view_list, likelist, dislikelist]
    return graphlists


    # plt.plot(published, view_list)  #x is published and y is view_list
    # plt.ylabel('Viewers (in millions)')
    # plt.xlabel('Videos')
    # plt.savefig('Viewer_count.png')

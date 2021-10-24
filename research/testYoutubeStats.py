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

# Should hide this key for real world use.
api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'

youtube = build('youtube', 'v3', developerKey=api_key)

#The id is the YouTube id for CNN https://www.youtube.com/channel/UCupvZG-5ko_eiXAupbDfxWw
request = youtube.channels().list(
    part='snippet, contentDetails,statistics',
    id = 'UCupvZG-5ko_eiXAupbDfxWw',
)

response = request.execute()
channel_stats = response['items']
upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']
print(upload_id)

video_list = []
request = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId=upload_id,
    maxResults = 50
)

response = request.execute()
data = response['items']
for video in data:
    video_id = video['contentDetails']['videoId']
    if video_id not in video_list:
        video_list.append(video_id)
print(video_list)
print(len(video_list))

stats_list = []

request = youtube.videos().list(
    part = "snippet,contentDetails,statistics",
    id = video_list[0:50]
)
data = request.execute()

for video in data['items']:
    published = video['snippet']['publishedAt']
    views = video['statistics'].get('viewCount',0)
    stats_dictionary = dict(
        published = published,
        views = views
    )
    stats_list.append(stats_dictionary)
print(stats_list)

view_list = []
published = []
for vid in stats_list:
    view_list.insert(0,(int(vid['views'])/1000000))
    pub = vid['published']
    pub = pub.split('-')
    month = pub[1]
    day = pub[2].split('T')
    day = day[0]
    published.insert(0,vid['published'])
print(view_list)
plt.plot(published, view_list)
plt.ylabel('Viewers (in millions')
plt.xlabel('Videos')
plt.show()

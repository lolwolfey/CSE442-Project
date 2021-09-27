"""
Note in order to run this you will need to pip intall the following:

1. pip install --upgrade google-api-python-client
2. pip install --upgrade google-auth-oauthlib google-auth-httplib2

*this pip install will need to be included in the Dockerfile as well.

The google developers website offers guides for most of their methods here:
https://developers.google.com/youtube/v3/quickstart/python

additionally the GitHub can be found here:
https://github.com/googleapis/google-api-python-client

Youtube video which provides the same information provided in the links above plus a guide for the code below:
https://www.youtube.com/watch?v=th5_9woFJmk
"""

from googleapiclient.discovery import build

# Should hide this key for real world use.
api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part='statistics',
    forUsername = 'schafer5'
)

response = request.execute()

print(response)
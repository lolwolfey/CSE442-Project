from flask import *
import requests
#from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from .database_handler import get_channel_id, name_to_id

main = Blueprint('main',__name__)

channels = [()]
@main.route('/home')
@login_required
def home():
    return render_template('Home.html')

@main.route('/search',methods = ["GET","POST"])
@login_required
def search():
    api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'
    if request.method == "POST":
        print(f"Request Form: {request.form}")
        ytchannel = request.form.get("userName")
        print(ytchannel)
        #rint(f"REQ:{request.form['col']}")
        if (request.form.get("col")):
            ytchannel = request.form.get("col")
        #print(request.form.get("username"))
        #ytchannel = request.form.get("userName") #get the username field of form in search page
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&forUsername={ytchannel}&key={api_key}"
        json_url = requests.get(url) #get the json data from url
        data = json.loads(json_url.text)
        #print(data)
        channelID = data['items'][0]["id"] #channelID to use in linking to the YT channel
        #print(channelID)
        subCount = data['items'][0]["statistics"]["subscriberCount"]
        viewCount = data['items'][0]["statistics"]["viewCount"]
        videoCount = data['items'][0]["statistics"]["videoCount"]
        channelPic = data['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
        name_to_id(channelID,ytchannel) #writing channelID and channel username to database
        dbCheck = get_channel_id(ytchannel) #used to check if database stores
        infoTuple = (ytchannel,subCount,viewCount,videoCount,channelPic,channelID,dbCheck)
        channels[0] = infoTuple
        print(channels)
        return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],channelID=channels[0][5],DBcheck=channels[0][6])
    #newurl = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&relevanceLanguage=en&maxResults=5&key={api_key}"
    #json_url2 = requests.get(newurl)
    #data2 = json.loads(json_url2.text)
    #print(data2)
    
    return render_template("Search.html")

@main.route('/stats')
@login_required
def stats():
    global channels
    return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],channelID=channels[0][5])

@main.route('/settings')
@login_required
def settings():
    return render_template('Settings.html')





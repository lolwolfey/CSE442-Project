from flask import *
import requests
#from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

main = Blueprint('main',__name__)

channels = [()]
@main.route('/home')
@login_required
def home():
    return render_template('testHome.html')

@main.route('/search',methods = ["GET","POST"])
@login_required
def search():
    api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'
    if request.method == "POST":
        #print(request.form)
        #print(request.form.get("username"))
        ytchannel = request.form.get("username")
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&forUsername={ytchannel}&key={api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        #print(data)
        subCount = data['items'][0]["statistics"]["subscriberCount"]
        viewCount = data['items'][0]["statistics"]["viewCount"]
        videoCount = data['items'][0]["statistics"]["videoCount"]
        channelPic = data['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
        infoTuple = (ytchannel,subCount,viewCount,videoCount,channelPic)
        channels[0] = infoTuple
        return redirect(url_for('stats'))
        #print(channels)

    #print(request.form.get()) 
    return render_template('Search.html')

@main.route('/stats')
@login_required
def stats():
    global channels
    return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4])

@main.route('/settings')
@login_required
def settings():
    return render_template('Settings.html')





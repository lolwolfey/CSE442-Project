from flask import *
import os
import sys
import requests
#from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json
from . import YoutubeStats
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

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
        #print(request.form)
        #print(request.form.get("username"))
        ytchannel = request.form.get("userName") #get the username field of form in search page
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&forUsername={ytchannel}&key={api_key}"
        json_url = requests.get(url) #get the json data from url
        data = json.loads(json_url.text)
        
        sys.stderr.write(str(data))
        channelID = data['items'][0]["id"] #channelID to use for plotting
        subCount = data['items'][0]["statistics"]["subscriberCount"]
        viewCount = data['items'][0]["statistics"]["viewCount"]
        videoCount = data['items'][0]["statistics"]["videoCount"]
        channelPic = data['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
        infoTuple = (ytchannel,subCount,viewCount,videoCount,channelPic,channelID) #adds all the info into tuple and adds tuple to array
        channels[0] = infoTuple
        return redirect(url_for('stats'))
        #print(channels)

    #print(request.form.get()) 
    return render_template('Search.html')

@main.route('/stats')
@login_required
def stats():
    global channels
    YoutubeStats.WeeklyViewerCount(channels[0][5])
    return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],Youtube_Id=channels[0][5])

@main.route('/settings')
@login_required
def settings():
    return render_template('Settings.html')

@main.route('/plot.png')
@login_required
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.set_title("Random Noise")
    axis.set_xlabel("1 - 100")
    axis.set_ylabel("Random #'s (1-50)")
    axis.plot(xs, ys, )
    return fig





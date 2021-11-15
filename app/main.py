from flask import Flask
from flask import *
import os
import sys
import requests
#from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .database_handler import bookmark_channel, init, signup_user, user_login, User, change_pass, get_password_by_username
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from .auth import password_requirements
import json
from . import YoutubeStats
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import numpy

main = Blueprint('main',__name__)

channels = [()]
@main.route('/home')
@login_required
def home():
    """
    TO DO:
    1. bookmarks = bookmarks table from current_user
    2. pass bookmarks into render template
    3. for loop in Home.html that adds all bookmarks to a value of a form.
    4. onclick='submit', action = /search_id --> looks up a channel by id and redirects to stats.

    *5. Add delete bookmark functionality possibly later (technically exist on stats page itself)
    """
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
        return redirect(url_for('main.stats'))
        #print(channels)

    #print(request.form.get())
    return render_template('Search.html')

@main.route('/stats', methods=['POST', 'GET'])
@login_required
def stats():
    
    if request.method == 'POST':
        add_remove = request.form.get('add_remove')
        channel = request.form.get('channel_name')
        id = request.form.get('channel_id')
        if add_remove == 'remove':
            remove_bookmark(channel, id)
        else:
            add_bookmark(channel, id)
    # global channels
    # YoutubeStats.WeeklyViewerCount(channels[0][5])
    # return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],Youtube_Id=channels[0][5])
    return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],Youtube_Id=channels[0][5])

@main.route('/settings', methods = ['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        # username = request.form['usrname']
        OldPass = request.form['oldpw']
        NewPass = request.form['newpw']
        # user = User(None, current_user.username, None)
        pwhash = get_password_by_username(current_user.username)
        flash('VALID password, everything up to now works!'+ str(OldPass) + str(NewPass) + str(current_user.username))
        if check_password_hash(pwhash, OldPass): #check if old password is correct
             valid, error = password_requirements(NewPass)  #check if new password meets requirements
             if valid:
                change_pass(current_user.username,NewPass)      #if it means requirements update password
             else:
                flash('Invalid NEW Password!', 'error')         #if not, generate error saying it did not
        else:
            flash('Old password is not correct', 'error')
    return render_template('Settings.html')

# @main.route("/SettingPassChange", methods = ['POST'])


@main.route('/plot.png')        #both functions required for making graph
@login_required
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    global channels
    # YoutubeStats.WeeklyViewerCount(channels[0][5])
    datalist = YoutubeStats.WeeklyViewerCount(channels[0][5])

    #References: https://www.tutorialspoint.com/matplotlib/matplotlib_bar_plot.htm, https://matplotlib.org/stable/api/figure_api.html
    fig = Figure()
    #line graph
    axis = fig.add_subplot(2, 1, 1)
    xs = datalist[0]                        #returns array of 7 most recent publish dates
    ys = datalist[1]                        #returns an of 7 most recent video's total viewerships
    axis.set_title("Total Views of the 7 Most Recent Videos")
    axis.set_xticks([])
    axis.set_ylabel("Total Viewership (in millions)")
    axis.plot(xs, ys)

    #bar graph 
    bars = fig.add_subplot(2, 1, 2)
    xs1 = datalist[0]                           #returns an array
    ys1 = datalist[2]                           #returns an array
    ys2 = datalist[3]
    distance = numpy.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    bars.set_title("Likes and Dislikes of the 7 Most Recent Videos")
    bars.set_xlabel("Last 7 Videos")
    bars.set_ylabel("Likes and Dislikes (in thousands)")
    bars.bar(distance - 0.1, ys1, 0.2, label= 'Likes')
    bars.bar(distance + 0.1, ys2, 0.2, label= 'Dislikes')
    bars.legend()
    fig.tight_layout()
    return fig

"""
@main.route('/bookmark', methods=['POST'])
@login_required
def bookmark():
    add_remove= request.form['add_remove']
    channel = request.form['channel_name']
    id = request.form['channel_id']
    if add_remove == 'remove':
        remove_bookmark(channel, id)
    else:
        add_bookmark(channel, id)
"""

@main.route('/add_bookmark')
@login_required
def add_bookmark(channel, id):
    sys.stderr.write('added: channel = ' + channel + ', id =' + id)
    return # Call bookmark_channel(id,channel) function.

@main.route('/remove_bookmark')
@login_required
def remove_bookmark(channel, id):
    sys.stderr.write('removed: channel = ' + channel + ', id =' + id)
    return # Create remove_bookmark(id, channel) function, and call it here.

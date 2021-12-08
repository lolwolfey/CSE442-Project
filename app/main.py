from flask import Flask
from flask import *
import os
import sys
import requests
#from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .database_handler import bookmark_channel, channel_exists, get_privacy, init, signup_user, user_login, User, private_update, public_update, change_pass, get_password_by_username, name_to_id, get_channel_id, get_users_list, channel_exists
from .database_handler import bookmark_channel, init, signup_user, user_login, User, change_pass, get_password_by_username, has_bookmark, delete_bookmark, get_bookmarks
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from .auth import password_requirements
import json
from . import YoutubeStats
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from tkinter import *
import random
import numpy

# """
# Reference Links
# --------------------------------------------------------------------------------------------------------------
# Werkzeug.security: https://werkzeug.palletsprojects.com/en/2.0.x/utils/
# flask: flask: https://flask.palletsprojects.com/en/2.0.x/ 
# flask-login: https://flask-login.readthedocs.io/en/latest/
# psycopg2: https://www.psycopg.org/docs/
# sys: https://docs.python.org/3/library/sys.html
# os: https://docs.python.org/3/library/os.html
# random: https://docs.python.org/3/library/random.html
# string: https://docs.python.org/3/library/string.html
# numpy: https://www.w3schools.com/python/numpy
# tkinter: https://docs.python.org/3/library/tkinter.html
# io: https://docs.python.org/3/library/io.html
# json: https://docs.python.org/3/library/json.html
# matplotlib.backends.backend_agg: https://matplotlib.org/3.5.0/api/backend_agg_api.html
# matplotlib.figure: https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure
# requests: https://docs.python-requests.org/en/latest/
# """

main = Blueprint('main',__name__)

channels = [()]
@main.route('/home')
@login_required
def home():
    bookmarks = get_bookmarks(current_user.user_id)
    return render_template('Home.html', bookmarks=bookmarks)

@main.route('/remove_bookmark_home', methods = ['POST'])
@login_required
def remove_bookmark_home():
    id = request.form.get('bookmark_delete')
    delete_bookmark(current_user.user_id,id)
    return redirect('/home')


"""
TO DO:
Make this load the proper stats page based on button you cicked.
"""
@main.route('/search_id', methods = ['POST'])
@login_required
def search_id():
    api_key = 'AIzaSyCrIwhrMNtHT0TX7HOJKhuMhWpKHvNjkXM'
    channelID = request.form.get('bookmark_button')
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2Cstatistics&id={channelID}&key={api_key}"
    json_url = requests.get(url) #get the json data from url
    data = json.loads(json_url.text)

    sys.stderr.write(str(data))
    ytchannel = data['items'][0]["snippet"]["localized"]["title"] 
    subCount = data['items'][0]["statistics"]["subscriberCount"]
    viewCount = data['items'][0]["statistics"]["viewCount"]
    videoCount = data['items'][0]["statistics"]["videoCount"]
    channelPic = data['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
    infoTuple = (ytchannel,subCount,viewCount,videoCount,channelPic,channelID) #adds all the info into tuple and adds tuple to array
    channels[0] = infoTuple
    return redirect(url_for('main.stats'))

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
        print(f"data['pageInfo'] = {data['pageInfo']} and data['PageInfo']['totalResults]= {data['pageInfo']['totalResults']}")
        sys.stdout.flush()
        if(data['pageInfo']['totalResults']!=0):
            sys.stderr.write(str(data))
            ytchannel = ytchannel = data['items'][0]["snippet"]["localized"]["title"]
            channelID = data['items'][0]["id"] #channelID to use in linking to the YT channel
            #print(channelID)
            subCount = data['items'][0]["statistics"]["subscriberCount"]
            viewCount = data['items'][0]["statistics"]["viewCount"]
            videoCount = data['items'][0]["statistics"]["videoCount"]
            channelPic = data['items'][0]["snippet"]["thumbnails"]["medium"]["url"]
            if(channel_exists(channelID)!= None):
                name_to_id(str(channelID),ytchannel) #writing channelID and channel username to database
            dbCheck = get_channel_id(ytchannel) #used to check if database stores
            infoTuple = (ytchannel,subCount,viewCount,videoCount,channelPic,channelID,dbCheck)
            channels[0] = infoTuple
            print(channels)
            return redirect(url_for('main.stats'))
        #print(channels)
        else:
            return render_template('Search.html',noYTuser="No such YouTuber found, check username and try again")
    return render_template('Search.html',noYTuser="")

@main.route('/searchuser',methods = ["GET","POST"])
@login_required
def searchuser():
    if(request.method == "POST"):
        searchName = request.form.get("userName")
        #print(searchName)
        userRetval = get_users_list()
        print(f"USER RETURN VALUE: {userRetval}")
        sys.stdout.flush()
        listUser = []
        for elem in userRetval:
            listUser.append(elem[0])
        print(f"LISTUSER: {listUser}")
        sys.stdout.flush()
    # create result list
        output = []
        for elem in listUser:
            if searchName in elem and elem != current_user.username:
                output.append(elem)
        print(f"search suggestions: {output}")
        sys.stdout.flush()
        return render_template("SearchUser.html",searchedUsers=output,len=len(output))
    return render_template("SearchUser.html")

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

    already_bookmarked = has_bookmark(current_user.user_id, channels[0][0], channels[0][5])
    if already_bookmarked:
        already_bookmarked = 1
    else:
        already_bookmarked = 0
    # global channels
    # YoutubeStats.WeeklyViewerCount(channels[0][5])
    # return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],Youtube_Id=channels[0][5])
    return render_template("Stats.html",Other_User=channels[0][0],subCounter=channels[0][1],viewCounter=channels[0][2],videoCounter=channels[0][3],thumbNail=channels[0][4],Youtube_Id=channels[0][5],already_bookmarked=already_bookmarked)

@main.route('/settings', methods = ['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        if(request.form.get("oldpw") and request.form.get("newpw")):
            OldPass = request.form.get("oldpw")
            NewPass = request.form.get("newpw")
            # user = User(None, current_user.username, None)
            pwhash = get_password_by_username(current_user.username)
            flash('VALID password, everything up to now works!')
            if check_password_hash(pwhash, OldPass): #check if old password is correct
                valid, error = password_requirements(NewPass)  #check if new password meets requirements
                if valid:
                    change_pass(current_user.username,NewPass)      #if it means requirements update password
                else:
                    flash('Invalid NEW Password!', 'error')         #if not, generate error saying it did not
            else:
                flash('Old password is not correct', 'error')
        if(request.form.get("col") == "PRIVATE"):
            print(f"CURRENT USERNAME: {current_user.username}")
            private_update(current_user.username) #make private
            print(f"AFTER MAKING USER of {current_user.username} private: {get_privacy(current_user.username)}")
            sys.stdout.flush()
        if(request.form.get("col") == "PUBLIC"):
            print(f"CURRENT USERNAME: {current_user.username}")
            public_update(current_user.username) #make public
            print(f"AFTER MAKING USER of {current_user.username} public: {get_privacy(current_user.username)}")
            sys.stdout.flush()
        
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

@main.route('/add_bookmark')
@login_required
def add_bookmark(channel, id):
    sys.stderr.write('added: channel = ' + channel + ', id =' + id)
    return bookmark_channel(current_user.user_id,channel,id)

@main.route('/remove_bookmark')
@login_required
def remove_bookmark(channel, id):
    sys.stderr.write('removed: channel = ' + channel + ', id =' + id)
    return delete_bookmark(current_user.user_id,id)

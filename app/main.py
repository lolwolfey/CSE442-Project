from flask import Flask
from flask import *
#from . import db
import os
import sys
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main',__name__)

@main.route('/home')
@login_required
def home():
    return render_template('Home.html')

@main.route('/search')
@login_required
def search():
    return render_template('Search.html')

@main.route('/stats')
@login_required
def stats():
    return render_template('Stats.html')

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

@main.route('/barplot.png')
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

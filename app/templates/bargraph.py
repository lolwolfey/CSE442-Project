import matplotlib.pyplot as plt
import numpy as np

#This creates the basic layout of the bargraph; the data will be computed
#and the information will be sent to here where it will be used to create
#the graph, and that will be saved as a png and displayed on the frontend.

xtick = ['7 days ago', '6 days ago', '5 days ago', '4 days ago', '3 days ago', '2 days ago', 'yesterday']
plt.title("Views on this channel each day for the past week")
plt.xticks(xtick)
plt.xlabel("Days")
plt.ylabel("Total Views")

plt.savefig('/app/templates/barplot.png')

#if this proves too demanding for the server or if its not allowed for the project, then we will shift to plotly.js
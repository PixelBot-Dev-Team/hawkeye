import matplotlib.pyplot as plt
import numpy as np
import datetime


#make up time data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(24)]

onlineUsersHistory = [19, 21, 33, 38, 48, 57, 63, 73, 81, 98, 104, 113, 125, 122, 112, 101, 87, 76, 54, 43, 32, 26, 28, 36] #test

def createChart(x, history):
    plt.title("PixelPlace Online Users (24h) (mockup)")
    plt.suptitle("HawkEye")
    
    plt.plot(x, history)
    plt.gcf().autofmt_xdate()

    plt.show()

createChart(x, onlineUsersHistory)
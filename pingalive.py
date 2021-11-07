import datetime
import pathlib
import sqlite3
import threading
import time
from PIL import Image
from io import DEFAULT_BUFFER_SIZE
import random

import matplotlib.pyplot as plt
import requests
CurrentDir = pathlib.Path(__file__).parent.absolute()
import pypxl

im = Image.open(f"{CurrentDir}\\7.png")
global c7img
c7img = im.load()

global start_time
start_time = datetime.datetime.utcnow()

bot8 = pypxl.Bot("pbt_ttt_1", "dMd>+8%}6DCDC'NH", 7)
def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f

@background
@bot8.socketconnection.on("ping.alive")
def pongalive():
    command = "window.pingalive=function(){function _(x){for(var b=[],a=_0x53b6(\"0x363\")+_0x53b6(\"0xac3\")+\"JKLEZCFXTA\",_=a.length,n=0;n<x;n++)b[_0x53b6(\"0x160\")](a[_0x53b6(\"0x9ac\")](Math[_0x53b6(\"0xe83\")](Math[_0x53b6(\"0x5ba\")]()*_)));return b[_0x53b6(\"0x7\")](\"\")}var x={0:\"g\",1:\"m\",2:\"b\",3:\"o\",4:\"z\",5:\"c\",6:\"f\",7:\"x\",8:\"t\",9:\"a\"},n=x;function t(x){for(var b=[],a=_0x53b6(\"0x270\")+_0x53b6(\"0x32a\")+_0x53b6(\"0xa1b\")+\"EFGHIJKLMN\"+_0x53b6(\"0x3f4\")+\"YZ\",_=a[_0x53b6(\"0x3a0\")],n=0;n<x;n++)b.push(a[_0x53b6(\"0x9ac\")](Math[_0x53b6(\"0xe83\")](Math.random()*_)));return b[_0x53b6(\"0x7\")](\"\")}return function(){var x,b=(parseInt((new Date)[_0x53b6(\"0x845\")]()/1e3)+\"\")[_0x53b6(\"0xeb1\")](\"\"),a=\"\";for(x in b)0==x&&(a+=t(5)),1==x&&(a+=t(7)),2==x&&(a+=_(3)),3==x&&(a+=t(8)),4==x&&(a+=_(6)),5==x&&(a+=t(3)),6==x&&(a+=t(6)),7==x&&(a+=_(4)),8==x&&(a+=t(7)),9==x&&(a+=t(6)),0===Math[_0x53b6(\"0xe83\")](2*Math[_0x53b6(\"0x5ba\")]())?_0x53b6(\"0x63c\")===_0x53b6(\"0x63c\")&&(a+=n[parseInt(b[x])][_0x53b6(\"0x721\")+\"e\"]()):a+=n[parseInt(b[x])];return a+=\"=\"}()};"
    bot8.driver.execute_script(command)
    pingalive = bot8.driver.execute_script("return pingalive()")

    bot8.socketconnection.emit("pong.alive", pingalive)
    print("pong'd ", pingalive)

def chat_Safety_Check(data):
    createdAt = data["createdAt"]
    messagetime = datetime.datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
    if messagetime > start_time and data["username"] != "TTTBot5" and data["username"] != "TTTBot6" and data["channel"] in ["whispers"]:
        return True
    else:
        return False

@bot8.socketconnection.on("chat.user.message")
@background
def logChat7(data):
    print(data)
    if chat_Safety_Check(data) == True: 
        pass 
    else: 
        return
    messageUsername = data["username"]
    messageGuild = data["guild"]
    message = data["message"]
    if message == "":
        message = "/here"
    messageIcons = data["icons"]
    target = messageUsername


    messageChannel = data["channel"]
    messageMention = data["mention"]
    MessageDic = str(message).split()
    prefix = MessageDic[0]
    print(prefix)

    if prefix == "!fill":
        if messageUsername == "SoManyNames" or messageUsername == "AlmosYT":
            if len(MessageDic) == 4:
                try:
                    x = int(MessageDic[1])
                    y = int(MessageDic[2])
                    color = int(MessageDic[3])
                except:
                    bot8.send_Chat(f"One of the Arguments is not a Number!",f"{messageUsername}","whispers",f"{target}",29)
                else:
                    bot8.send_Chat(f"Trying to start a Fill at X:{x},Y:{y}!:",f"{messageUsername}","whispers",f"{target}",29)
                    newThread = threading.Thread(target=playerAlikeFill,args=(x,y,color))
                    newThread.start()
            else:
                bot8.send_Chat("Missing or too many Arguments! Syntax is '$fill x y color'!",f"{messageUsername}","whispers",f"{target}",29)



def playerAlikeFill(x,y,color):
	stack = []
	trash = []
	pixel_list = []
	stack.append([x, y])
	while len(stack) != 0:
		x,y = stack.pop()
		pixel_list.append([x,y])
		if getPixel7(x, y) != (204, 204, 204, 255):
			trash.append([x,y])
			if [x,y + 1] not in stack and [x,y + 1] not in trash:
				stack.append([x,y + 1])
			if [x,y - 1] not in stack and [x,y - 1] not in trash:
				stack.append([x,y - 1])
			if [x + 1,y] not in stack and [x + 1,y] not in trash:
				stack.append([x + 1,y])
			if [x - 1,y] not in stack and [x - 1,y] not in trash:
				stack.append([x - 1,y])
		else:
			print(f"Skipping {x},{y}!")
	for x,y in pixel_list:
		bot8.place_Pixel(x,y,color)
		#sleeptime = random.uniform(0.016, 0.026)
		time.sleep(0.016)
	print(f"Done Filling")

def getPixel7(x,y):
	global c7img
	color = c7img[x,y]
	return color

if __name__ == "__main__":
    print('FUCK MY LIFE')
    input()



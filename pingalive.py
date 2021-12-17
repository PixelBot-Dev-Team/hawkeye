import datetime
import pathlib
import sqlite3
import threading
import time
from PIL import Image
from io import DEFAULT_BUFFER_SIZE
import random
from tqdm import tqdm
import json
import urllib.request
import ssl

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
#bot7 = pypxl.Bot("pbt_ttt_2", "BnASyqy577gPX2RD", 7)

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
    contents = json.loads(urllib.request.urlopen("https://api.almos.xyz/new?apikey=0amkTtaa0VvpDYyTBR8dMz").read())
    bot8.socketconnection.emit("pong.alive", contents["pongalive"])
    print("pong'd ", contents["pongalive"])

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

    if prefix == "!dot":
        if messageUsername == "SoManyNames" or messageUsername == "AlmosYT":
            if len(MessageDic) == 4:
                try:
                    x = int(MessageDic[1])
                    y = int(MessageDic[2])
                    color = int(MessageDic[3])
                except:
                    bot8.send_Chat(f"One of the Arguments is not a Number!",f"{messageUsername}","whispers",f"{target}",29)
                else:
                    bot8.send_Chat(f"Trying to start a Dotting at X:{x},Y:{y}!:",f"{messageUsername}","whispers",f"{target}",29)
                    newThread = threading.Thread(target=dotFill,args=(x,y,color))
                    newThread.start()
            else:
                bot8.send_Chat("Missing or too many Arguments! Syntax is '$dot x y color'!",f"{messageUsername}","whispers",f"{target}",29)
        else:
            bot8.send_Chat("This Command is currently only avaiable to Simon and Almos!",f"{messageUsername}",f"{messageChannel}",f"{target}",29)


    elif prefix == "!fill":
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
	for x,y in tqdm(pixel_list):
		bot8.place_Pixel(x,y,color)
		#sleeptime = random.uniform(0.016, 0.026)
		time.sleep(0.016)
	print(f"Done Filling")

def dotFill(x,y,color):
    stack = []
    trash = []
    pixel_list = []
    stack.append([x, y])
    while len(stack) != 0:
        x,y = stack.pop()
        pixel_list.append([x,y])
        if getPixel7(x, y) != (204, 204, 204, 255):
            #debugMessage(f"Adding to Stack: {x},{y}!")
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
    while len(pixel_list) > 0:
        x,y = random.choice(pixel_list)
        bot8.place_Pixel(x,y,color)
        time.sleep(0.016)
        #debugMessage(f"Placing {x},{y}!")
        pixel_list.remove([x,y])
    print(f"Done Dotting")

def getPixel7(x,y):
	global c7img
	color = c7img[x,y]
	return color

if __name__ == "__main__":
    print('FUCK MY LIFE')
    input()



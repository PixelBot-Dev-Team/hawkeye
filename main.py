# sourcery skip: aware-datetime-for-utc
import datetime
import pathlib
import threading
import time
import socketio
import requests

CurrentDir = pathlib.Path(__file__).parent.absolute()

webhook_onoff = "https://discord.com/api/webhooks/883775606540632075/hHrdNa-UHAaerqtoBWMdnenBsi0Tfd1-zsW78hPEIenvHNN1EA8IvEiNGvanko7zqiL_"
webhook_mvp = "https://discord.com/api/webhooks/835654940008382464/RsN3Jjg8B6Ukv-8C09MfjktvyGrQztO4At2RIf27w4ZwmLpq_olf7kjr_YXPyAE8Cv43"
webhook_global = "https://discord.com/api/webhooks/835654823784874015/yXIkpU5K7mjAcJc3bBorIkaApkH5cw5Sc-_rdoKrJo-Jfxfmuyabk7C1MYtU8Nmtegit"
webhook_stats = "https://discord.com/api/webhooks/883773760447066112/qzeDM4A882s1DmvM7OXyswue_fQCnZL-F2xDu-iIyk5mB7CAN7ZmjJj1Gspz-ThQ5ezS"
webhook_mods = "https://discord.com/api/webhooks/883807042656157828/053ufcOenaZo0dZHqBhz1Fd47SAt4qQ5_Wd3ZIMPo_RRcIGbBqguw1zjULrsS2QCMyJ0"
webhook_mutes = "https://discord.com/api/webhooks/888503958904119356/t-v4e44YADLH7x5mF68XSj0nYKcV07dDRGFQ7z6fmkPTQnqBZ6bIAlfoECU_1Z7sjkOc"
webhook_nonenglish = "https://discord.com/api/webhooks/1069645268808634463/nyWeuJnVh9wVealJiUg6mV0wqXVb0SsJoRmB5j2GXGu1wOCxABXbclQRXG8eFHR-LbCm"
webhook_anarchy = "https://discord.com/api/webhooks/1069654465180881016/QBgsP1x89uPsuPlfdxnKBWu6KMAdlsQ55MKXl_6FcUKPSmtgVrbcmEDyGh5jnAzSKTbl"
webhook_gifts = "https://discord.com/api/webhooks/1069671206678175774/6oC9cFqw-hyBbYkuolhW7eJ_u5qYDbATjHBhK1lCCxZx7vJ86vm91vXqreR4ujrnefru"
webhook_CoinIslandNotif = "https://discord.com/api/webhooks/1069671531539603477/NflDPBF_51vysbpJnyyFXqVP8oApcIAfFjQFvLa8zEKIUVcNLhBTqsviEssNYI1m2Iif"
webhook_ItemLogs = "https://discord.com/api/webhooks/1069693721014190131/5W6y8OUesWPe2IAEykdowVnpaRl9Wyc_UfWEC6mtECb9t_At1S-G7ET0yq9Z770HOQnq"
webhook_WarNotifs = "https://discord.com/api/webhooks/1070057490009567233/qKMUIhEhnTV3L06sYaUzdCMLAyUimJg1vbQl_i-rekC7wQozod_avxnY8fBCGo8o30ms"

CoinIsland_roles = {0:"<@&1069696793702584320>",1:"<@&1069696820730667120>",2:"<@&1069696859012083762>",3:"<@&1069696893585719367>",}

badgeDict = {"_1_month" : "<:1month:883780503583465532>","_1_year" : "<:1year:883780503369568277>","_3_months" : "<:3months:883780503440871465>","_admin" : "<:admin:883780503323430933>","_booster" : "<:booster:883780503596060712>","_ppbread" : "<:ppbread:883780503713488916>","_chat_moderator" : "<:chatmoderator:883780503386357781>","_gifter" : "<:gifter:883780503646392370>","_moderator" : "<:moderator:883780503566704710>","_nitro" : "<:nitro:883780503675764736>","_paintingmoderator" : "<:paintingmoderator:883780503151460373>","_paintingowner" : "<:paintingowner:883780503780601866>","_partner" : "<:partner:883780503558299658>","_vip" : "<:vip:883780503516377108>","_former_global_moderator":"<a:formerglobalmoderator:1067942869786169435>","_3_days":"<a:3days:1067947658372730990>"}
pp_items = {1:"Pixel Missile",2:"Pixel Bomb",3:"Atmic Bomb",4:"Premium (1 Month)",5:"Premium (1 Year)",6:"Rainbow Username",7:"Guild Bomb",8:"Avatar Bomb",9:"Name Change",10:"XMAS Username",11:"Premium (3 Days)",12:"HALLOWEEN Username",}
warAreas = {"0":"Australia","1":"Russia","2":"Africa","3":"Antarctica","4":"Canadad","5":"Brazil","6":"China","7":"Greenland","8":"US",}

# pp_id_to_hex = {0:"#FFFFFF",1:"#C4C4C4",2:"#888888",3:"#555555",4:"#222222",5:"#000000",6:"#006600",7:"#22B14C",8:"#02BE01",9:"#51E119",10:"#94E044",11:"#FBFF5B",12:"#E5D900",13:"#E6BE0C",14:"#E59500",15:"#A06A42",16:"#99530D",17:"#633C1F",18:"#6B0000",19:"#9F0000",20:"#E50000",21:"#FF3904",22:"#BB4F00",23:"#FF755F",24:"#FFC49F",25:"#FFDFCC",26:"#FFA7D1",27:"#CF6EE4",28:"#EC08EC",29:"#820080",30:"#5100FF",31:"#020763",32:"#0000EA",33:"#044BFF",34:"#6583CF",35:"#36BAFF",36:"#0083C7",37:"#00D3DD",38:"#45FFC8",39:"#003638",40:"#477050",41:"#98FB98",42:"#FF7000",43:"#CE2939",44:"#FF416A",45:"#7D26CD",46:"#330077",47:"#005BA1",48:"#B5E8EE",49:"#1B7400"}

global socketconnection7
socketconnection7 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection7.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection7.emit(event='init', data={"authId":"Hawkeye7","boardId":7})
global socketconnection8
socketconnection8 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection8.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection8.emit(event='init', data={"authId":"Hawkeye8","boardId":8})
global socketconnection13
socketconnection13 = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
socketconnection13.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
socketconnection13.emit(event='init', data={"authId":"Hawkeye13","boardId":13})

@socketconnection7.on("throw.error")
def error7(data):
	print(data)
	socketconnection7.disconnect()
	socketconnection7.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
	socketconnection7.emit(event='init', data={"authId":"Hawkeye7","boardId":7})

@socketconnection8.on("throw.error")
def error8(data):
	print(data)
	socketconnection8.disconnect()
	socketconnection8.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
	socketconnection8.emit(event='init', data={"authId":"Hawkeye8","boardId":8})

@socketconnection13.on("throw.error")
def error13(data):
	print(data)
	socketconnection13.disconnect()
	socketconnection13.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
	socketconnection13.emit(event='init', data={"authId":"Hawkeye13","boardId":13})

global start_time
start_time = datetime.datetime.utcnow()

def background(f):
	'''
	a threading decorator
	use @background above the function you want to run in the background
	'''
	def bg_f(*a, **kw):
		threading.Thread(target=f, args=a, kwargs=kw).start()
	return bg_f

def chat_Safety_Check(data):
	messagetime = datetime.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
	return messagetime > start_time and data["channel"] in [
		"global",
		"painting",
		"nonenglish",
	]

# Chat Logs

# 7/Global Chat and nonenglish
@socketconnection7.on("chat.user.message")
@background
def logChat7(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/7#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
{message}
{messageMentionInsert}
"""
	if messageChannel == "global":
		webhookURL = webhook_global
		botUsername = "/7 Chat Message"
		canvas = 7
	elif messageChannel == "nonenglish":
		webhookURL = webhook_nonenglish
		botUsername = "Non english Chat Message"
		canvas = 7
	else:
		print("yo wtf man")
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": f"{botUsername}",
		"embeds": [embed],
	}
	postWebhook(webhookURL, whdata)
	checkChatMessage(message, messageUsername,canvas)

@socketconnection8.on("chat.user.message")
@background
def logChat8(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# return if not 8 message
	if messageChannel != "painting":
		return
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/8#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
		{message}
		{messageMentionInsert}
	"""
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": "/8 Chat Message",
		"embeds": [embed],
	}
	postWebhook(webhook_mvp, whdata)
	checkChatMessage(message, messageUsername,8)

@socketconnection13.on("chat.user.message")
@background
def logChat13(data):
	# Check if message is new
	if chat_Safety_Check(data) != True:
		return
	# make data easier to use
	messageUsername = data["username"]
	messageChannel = data["channel"]
	messageMention = data["mention"]
	messageGuild = data["guild"]
	messageIcons = data["icons"]
	message = data["message"]
	# return if not 13 message
	if messageChannel != "painting":
		return
	# handle /here shits
	try:
		x = data["posX"]
		y = data["posY"]
		zoom = data["posS"]
		insert = f"(x:{x},y:{y},zoom:{zoom})"
		message = f"""{message} | /here Coords:{insert}
<https://pixelplace.io/13#x={x}&y={y}&s={zoom}>"""
	except KeyError:
		# There just arent coords / the message doesent include /here
		pass
	except Exception as e:
		print(f"Idk bruh some error somewhere lol ({e})")
		return
	# Convert some shit and get some shit
	discordIconString = getIcons(messageIcons)
	discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
	discordGuildNameDivider = "" if messageGuild == "" else " - "
	messageMentionInsert = (f"Mentioned people: {messageMention}" if messageMention != "" else "")
	discordMessage = f"""
{message}
{messageMentionInsert}
"""
	embed = {"description": f"{discordMessage}","title": f"{messageUsername} {discordIconString}{discordGuildNameDivider}{messageGuild}"}
	whdata = {
		"content": f"{discordRelativeTimestamp}",
		"username": "/13 (/0) Chat Message",   #
		"embeds": [embed],
	}
	postWebhook(webhook_anarchy, whdata)

# Misc Logs

@socketconnection7.on("chat.stats")
@background
def postChatStats(data):
	canvas7Stat = data[0]
	totalStat = data[1]
	content = f"""
Players on Canvas 7>{canvas7Stat}
Players in total   >{totalStat}
These Numbers might not be accurate."""
	embed = {"description": f"{content}","title": "Stats", "color": 16776958} #white
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Stats","embeds": [embed],}
	postWebhook(webhook_stats, whdata)

@socketconnection7.on("j")
@background
def postJoins(data):
	if data == "":
		return
	content = f"{data} joined!"
	embed = {"description": f"{content}","title": "Joins", "color": 2531122} #green
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Joins","embeds": [embed],}
	postWebhook(webhook_onoff, whdata)

@socketconnection7.on("l")
@background
def postLeaves(data):
	content = f"{data} left!"
	embed = {"description": f"{content}","title": "Leaves", "color": 13571349} #red
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Leaves","embeds": [embed],}
	postWebhook(webhook_onoff, whdata)

@socketconnection7.on("chat.system.delete")
@background
def postMutes(data):
	embed = {"description": f"","title": "Chat Mute detected!", "fields" : [{"name" : "Muted User", "value" : f"{data}"}, {"name" : "Info", "value" : "These logs are not official information. To appeal a mute, join the PixelPlace discord."}], "color": 13036340} #yellow
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069701352479010846> ||","username": "Chat Mutes","embeds": [embed],}
	postWebhook(webhook_mutes, whdata)

@socketconnection7.on("item.notification.gift")
@background
def postGifts(data):
	gifter = data["from"]
	gifted = data["to"]
	gift = pp_items[data["item"]]
	embed = {"description":"","title": "Gift detected!", "fields" : [{"name" : "Gifted User", "value" : f"{gifted}"}, {"name" : "Gifter", "value" : f"{gifter}"}, {"name" : "Item", "value" : f"{gift}"}], "color": 13036340} #yellow
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Gift Logs","embeds": [embed],}
	postWebhook(webhook_gifts, whdata)

@socketconnection7.on("coin_island_owner_change")
@background
def postCoinIslandNotif(data):
	newOwner = data["from"]
	coinsGained = data["amount"]
	islandId = data["island"]
	ping = CoinIsland_roles[islandId]
	embed = {"description": "","title": f"Coin Island {islandId} has a new Owner", "fields" : [{"name" : "New Owner", "value" : f"{newOwner}"}, {"name" : "Coins gained", "value" : f"{coinsGained}"}], "color": 13036340} #yellow
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || {ping} ||","username": "Coin Island Logs","embeds": [embed],}
	postWebhook(webhook_CoinIslandNotif, whdata)

@socketconnection7.on("item.notification.use")
@background
def postItemUse(data):
	user = data["from"]
	item = data["itemName"]
	canvas = data["painting"]
	x = data["x"]
	y = data["y"]
	zoom = data["zoom"]
	color = data["c"] # pp id
	embed = {"description": f"<https://pixelplace.io/{canvas}#x={x}&y={y}&s={zoom}>","title": f"{item} used!", "fields" : [{"name" : "Username", "value" : f"{user}"}, {"name" : "X", "value" : f"{x}"}, {"name" : "Y", "value" : f"{y}"}], "color": 13036340}
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "Item usage logs","embeds": [embed],}
	postWebhook(webhook_ItemLogs, whdata)

@socketconnection7.on("area_fight_start")
@background
def postWarStart(data):
	print("War Started")
	warType = "Player war" if data["fightType"] else "Guild war"
	area = warAreas[data["id"]]
	endTime = int(data["fightEndAt"])
	embed = {"description": "","title": "A new war has started!", "fields" : [{"name" : "Area", "value" : f"{area}"}, {"name" : "Type", "value" : f"{warType}"}, {"name" : "End", "value" : f"<t:{endTime}:R>"}], "color": 13036340}
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069696750060838942> ||","username": "War logs","embeds": [embed],}
	postWebhook(webhook_WarNotifs, whdata)

@socketconnection7.on("area_fight_end")
@background
def postWarEnd(data):
	print("War Ended")
	warType = "Player war" if data["fightType"] else "Guild war"
	area = warAreas[data["id"]]
	winner = data["ownedBy"]
	if winner  == "":
		winner = "No one"
	gainedPoints = ["points"]
	nextWarTimer = int(data["nextFight"]) + int(getTimeStamp())
	stats = data["stats"]
	embed = {"description": "","title": f"The {warType} in {area} has ended!", "fields" : [{"name" : "Winner", "value" : f"{winner}"}, {"name" : "Awarded Battle Points", "value" : f"{gainedPoints}"}, {"name" : "Next War", "value" : f"<t:{nextWarTimer}:R>"}], "color": 13036340}
	whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "War logs","embeds": [embed],}
	postWebhook(webhook_WarNotifs, whdata)

# Helper Methods

def checkChatMessage(message,username,canvas):
	with open(f"{CurrentDir}/filter.txt",'r') as file:
		slurlist = file.read().splitlines()
		for word in message.split():
			if word.lower() in slurlist:
				embed = {"description": "","title": "Bad word detected!", "fields" : [{"name" : "Username", "value" : f"{username}"}, {"name" : "Canvas", "value" : f"{canvas}"}, {"name" : "Message", "value" : f"{message}"}, {"name" : "Detected Word", "value" : f"{word}"}], "color": 14662147} #yellow
				whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "AutoMod","embeds": [embed],}
				postWebhook(webhook_mods, whdata)

def getTimeStamp():
	return str(time.time()).split(".")[0]

def getIcons(icons):
	iconsstr = ""
	for icon in icons:
		icon = icon.replace("-", "_")
		icon = f"_{icon}"
		if icon == "_bread":
			icon = "_ppbread"
		try:
			formatted_icon = badgeDict[f"{icon}"]
		except KeyError:
			print(f"'{icon}' not found")
			continue
		iconsstr = f"{iconsstr}{formatted_icon}"
	return iconsstr

def postWebhook(url, data):
	requests.post(url, json=data)
	time.sleep(1)

while True:
	input("Press Ctrl + c to end")

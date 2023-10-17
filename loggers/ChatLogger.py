import datetime
import threading

import requests
from homoglyphs import Homoglyphs
from socketio import Client

from lib.util import background, getBadgeDict, getTimeStamp, postWebhook

class ChatLogger:
	def __init__(self, canvas:int, WH_CHAT_URL:str, WH_OWMINCE_URL:str, WH_MUTE_URL:str, WH_ALERT_URL:str, WH_FILTER_URL:str, startTime, checkMessage:bool = True, owminceCheck:bool = True, non_eng_overwrite = False) -> None:
		# Setup Connection
		self.canvas = canvas
		socketConnection = Client(reconnection=True, logger=False, engineio_logger=False)
		socketConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
		socketConnection.emit(event='init', data={"authId":f"HawkEye Agent (Canvas {self.canvas})","boardId":self.canvas})

		@socketConnection.on("chat.user.message")
		@background
		def logChat(data):
			if self.messageIsOld(data,startTime):
				return
			self.CM_Channel:str = data["channel"]
			# Return global message is a specific canvas is being logged
			if self.canvas != 7 and self.CM_Channel != "painting":
				return
			# Return global message if non eng overwrite is active
			if non_eng_overwrite and self.CM_Channel != "nonenglish":
				return
			# Return noneng message if non eng overwrite is off
			elif not non_eng_overwrite and self.CM_Channel != "global":
				return
			self.CM_Username:str = data["username"]
			self.CM_Mentions:str = data["mention"]
			self.CM_Guild:str = data["guild"]
			self.CM_Badges:list = data["icons"]
			self.CM_Message:str = data["message"] # backup for further processing
			final_text:str = self.CM_Message
			# Gather Rich data
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={self.CM_Username}").json()
			try:
				self.RD_Guild_rank = int(rich_data["guild_rank"])
				self.RD_Guild_rank_title = {1:rich_data["guild_rank_1_title"],2:rich_data["guild_rank_2_title"],3:rich_data["guild_rank_3_title"] or ""}
				final_rank_guild = self.RD_Guild_rank_title[self.RD_Guild_rank]
			except:
				final_rank_guild = ""
			self.RD_Profile_canvas = rich_data["canvas"]
			# Represent stuff like rainbow names etc
			usernameInsert = ""
			if RD_golden_profile := bool(rich_data["golden"]):
				usernameInsert = usernameInsert+"🟨"
			if RD_Rainbow_name := getTimeStamp() < rich_data["rainbowTime"]:
				usernameInsert = usernameInsert+"🌈"
			if RD_Xmas_name := getTimeStamp() < rich_data["xmasTime"]:
				usernameInsert = usernameInsert+"🎄"
			if RD_Halloween_name := getTimeStamp() < rich_data["halloweenTime"]:
				usernameInsert = usernameInsert+"🎃"
			if usernameInsert != "":
				usernameInsert = " ("+usernameInsert+")"
			# Process /here 
			try:
				hereCommand_X = data["posX"]
				hereCommand_Y = data["posY"]
				hereCommand_Zoom = data["posS"]
				final_text = f"[[{hereCommand_X},{hereCommand_Y}]](https://pixelplace.io/{self.canvas}#x={hereCommand_X}&y={hereCommand_Y}&s={hereCommand_Zoom})" + final_text
			except KeyError:
				pass
			# Process Mentions
			if self.CM_Mentions != "":
				final_text = f"""{final_text}
						
Mentions: {self.CM_Mentions}"""
			# Process Badges
			final_badges = ''.join([getBadgeDict()[badge] for badge in self.CM_Badges])			
			# Process Guild divider
			final_guild_divider = " - " if self.CM_Guild != "" else ""
			# Embed stuff
			embed = {"title": f"{self.CM_Username} {final_badges}{usernameInsert}{final_guild_divider}{self.CM_Guild}{final_guild_divider}{final_rank_guild}",
				"description": final_text,
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{self.RD_Profile_canvas}.png","height": 0,"width": 0},
				"color":"65501",
			}
			whdata = {
				"content": f"Logged <t:{getTimeStamp()}:R>",
				"username": f"HawkEye (/{self.canvas} logs)",
				"embeds": [embed],
			}
			# Message is completely processed. Time for other checks
			if owminceCheck and self.CM_Username.lower() == "owmince":
				postWebhook(WH_OWMINCE_URL,whdata)
			if checkMessage:
				checkingThread = threading.Thread(target=self.checkMessage,args=[self.CM_Message,WH_FILTER_URL],daemon=True).start()
			# Webhook stuff
			postWebhook(WH_CHAT_URL,whdata)

		@socketConnection.on("chat.system.delete")
		@background
		def logMutes(data):
		# Would be cool to later on log messages in a db for a day or smth and lookup the last message of the user
			if self.canvas == 7:
				return
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={data}").json()
			userCanvasId = rich_data["canvas"]
			badges = str(rich_data["othersIcons"]).split(",").append(rich_data["premiumIcon"])
			if rich_data["vip"]:
				badges.append("vip")
			final_badges = ''.join([getBadgeDict()[badge] for badge in badges])	
			embed = {"description": "",
					 "title": "Chat Mute detected!", 
					 "thumbnail":{"url": f"https://pixelplace.io/canvas/{userCanvasId}.png","height": 0,"width": 0},
					 "fields" : [{"name" : "Muted User", "value" : f"{data}{final_badges}"}], "color": 2123412}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069701352479010846> ||","username": "HawkEye (Mute Logs)","embeds": [embed],}
			postWebhook(WH_MUTE_URL, whdata)

		@socketConnection.on("canvas.alert")
		@background
		def logAlerts(message):
			if self.canvas == 7:
				return
			embed = {"title": "New Canvas Alert!","description": f"{message}",} 
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Alert Logs)","embeds": [embed],}
			postWebhook(WH_ALERT_URL, whdata)
			
	# Helper #

	def checkMessage(self,adjusted_message,WH_FILTER_URL) -> None:
		with open("./lib/filter.txt",'r') as filter_file:
			original_message = adjusted_message
			slurlist = filter_file.read().splitlines()
			possible_messages = Homoglyphs().to_ascii(adjusted_message)
			for adjusted_message in possible_messages:
				for word in adjusted_message.split():
					if word in slurlist:
						adjusted_message = str(original_message).replace(word,f"**{word}**")
						embed = {"description": "","title": "Violation detected!", "fields" : [{"name" : "Username", "value" : self.CM_Username}, {"name" : "Canvas", "value" : self.canvas}, {"name" : "Message", "value" : f"{adjusted_message}"}, {"name" : "Detected Word", "value" : f"{word}"}], "color": 14662147} #yellow
						whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (AutoMod)","embeds": [embed],}
						postWebhook(WH_FILTER_URL, whdata)
						break
				
	def messageIsOld(self,data, startTime):
		messagetime = datetime.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
		return messagetime < startTime

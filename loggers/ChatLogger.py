import time
from datetime import datetime
from threading import Thread

from homoglyphs import Homoglyphs
from socketio import Client
from socketio.exceptions import ConnectionError

from lib.util import (background, getBadgeDict, getProfileData, getTimeStamp,
                      postWebhook)


class ChatMessage():
	def __init__(self,messageData) -> None:
		self.USERNAME:str = messageData["username"]
		self.MENTIONS:str = messageData["mention"]
		self.GUILD:str = messageData["guild"]
		self.BADGES:list = messageData["icons"]
		self.TEXT:str = messageData["message"]
		try:
			self.HAS_HERE:bool = True
			self.HERE_COMMAND_X:int = int(messageData["posX"])
			self.HERE_COMMAND_Y:int = int(messageData["posY"])
			self.HERE_COMMAND_ZOOM:float = float(messageData["posS"])
		except KeyError:
			self.HAS_HERE:bool = False
		_, self.PFP_CANVAS_ID, self.USERNAME_EXTRA, _, self.GUILD_TITLE, self.GUILD_DIVIDER = getProfileData(self.USERNAME)
		
	def getBadgesAsEmotes(self) -> str:
		return ''.join([getBadgeDict()[badge] for badge in self.BADGES])

class ChatLogger:
	"""Chat Logger for Pixelplace.io\n
	Set canvas to `-1` to log non english chat."""
	def __init__(self, startTime:int, canvas:int, WH_CHAT_URL:str, WH_OWMINCE_URL:str, WH_MUTE_URL:str, WH_ALERT_URL:str, WH_FILTER_URL:str, checkMessagesForSlurs:bool = True, filterOwminceMessages:bool = True) -> None:
		# Convert data to self.
		if canvas == -1:
			self.canvas = 7
			self.isNonEngLogger = True
		else:
			self.canvas = canvas
			self.isNonEngLogger = False
		self.checkMessagesForSlurs = checkMessagesForSlurs
		if self.checkMessagesForSlurs:
			self.FILTER_FILE:list = open("./lib/filter.txt",'r').read().splitlines()
		self.filterOwminceMessages = filterOwminceMessages
		self.startTime = startTime
		self.WEBHOOKS = {
			"MESSAGES": WH_CHAT_URL,
			"OWMINCE" : WH_OWMINCE_URL,
			"MUTES"   : WH_MUTE_URL,
			"ALERTS"  : WH_ALERT_URL,
			"FILTERED": WH_FILTER_URL,
		}
		# Setup Connection
		self.connected = False
		while not self.connected:
			try: 
				socketConnection = Client(reconnection=True, logger=False, engineio_logger=False)
				socketConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
				socketConnection.emit(event='init', data={"authId":f"HawkEye Agent (Canvas {self.canvas})","boardId":self.canvas})
				self.connected = True
			except ConnectionError:
				print("didnt connect retrying (chatlogger)")
				time.sleep(2)

				
		@socketConnection.on("chat.user.message")
		@background
		def logChat(messageData):
			# Check if message is valid for Logger Config
			if not self.messageIsValid(messageData, self.startTime):
				return
			chatMessageObject = ChatMessage(messageData)
			# Process /here (if no /here is found it gets set to "")
			embedText = f"[[{chatMessageObject.HERE_COMMAND_X},{chatMessageObject.HERE_COMMAND_Y}] ](https://pixelplace.io/{self.canvas}#x={chatMessageObject.HERE_COMMAND_X}&y={chatMessageObject.HERE_COMMAND_Y}&s={chatMessageObject.HERE_COMMAND_ZOOM})" if chatMessageObject.HAS_HERE else ""
			# Process Main text
			embedText = f"{embedText}{chatMessageObject.TEXT}"
			# Process Mentions
			if chatMessageObject.MENTIONS != "":
				embedText = f"{embedText}\n\nMentions:{chatMessageObject.MENTIONS}"			
			# Create Embed
			embed = {
				"title": f"{chatMessageObject.USERNAME}{chatMessageObject.getBadgesAsEmotes()}{chatMessageObject.USERNAME_EXTRA}{chatMessageObject.GUILD_DIVIDER}{chatMessageObject.GUILD}{chatMessageObject.GUILD_DIVIDER}{chatMessageObject.GUILD_TITLE}",
				"description": embedText,
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{chatMessageObject.PFP_CANVAS_ID}.png","height": 0,"width": 0},
			}
			webhookData = {
				"content": f"Logged <t:{getTimeStamp()}:R>",
				"username": f"HawkEye (/{self.canvas} logs)",
				"embeds": [embed],
			}
			# Send to normal logs
			postWebhook(WH_CHAT_URL,webhookData)
			# Message is completely processed. Time for other checks
			if self.filterOwminceMessages and chatMessageObject.USERNAME.lower() == "owmince":
				postWebhook(WH_OWMINCE_URL,webhookData)
			if self.checkMessagesForSlurs:
				_ = Thread(target=self.checkMessage,args=[chatMessageObject,WH_FILTER_URL],daemon=True).start()

		@socketConnection.on("chat.system.delete")
		@background
		def logMutes(USERNAME):
			if self.canvas == 7: # These are logged in MiscLogger.py
				return
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(USERNAME)
			embed = {
				"title": "Chat Mute detected!", 
				"description": "",
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{PFP_CANVAS_ID}.png","height": 0,"width": 0},
				"fields" : [
					{"name" : "Muted User", "value" : f"{USERNAME}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE}"}
					]}
			#                                                       {      Mute Role      }
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069701352479010846> ||","username": "HawkEye (Mute Logs)","embeds": [embed],}
			postWebhook(WH_MUTE_URL, whdata)

		@socketConnection.on("canvas.alert")
		@background
		def logAlerts(message):
			if self.canvas == 7: # These are logged in MiscLogger.py
				return
			embed = {"title": "New Canvas Alert!","description": f"{message}",} 
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Alert Logs)","embeds": [embed],}
			postWebhook(WH_ALERT_URL, whdata)
			
	# Helper #

	def checkMessage(self,chatMessageObject:ChatMessage,WH_FILTER_URL:str) -> None:
		original_message = chatMessageObject.TEXT
		for message in Homoglyphs()._to_ascii(chatMessageObject.TEXT):
			for word in message.split():
				if word in self.FILTER_FILE:
					newMessageText = str(original_message).replace(word,f"**~~{word}~~**")
					embed = {
						"title"      : "Violation detected!",
						"description": "",
						"thumbnail":{"url": f"https://pixelplace.io/canvas/{chatMessageObject.PFP_CANVAS_ID}.png","height": 0,"width": 0},
						"fields"     : [
							{"name" : "Username", "value" : f"{chatMessageObject.USERNAME}{chatMessageObject.USERNAME_EXTRA}{chatMessageObject.GUILD_DIVIDER}{chatMessageObject.GUILD}{chatMessageObject.GUILD_DIVIDER}{chatMessageObject.GUILD_TITLE}"},
							{"name" : "Message", "value" : f"{newMessageText}"}, 
							{"name" : "Detected Word", "value" : f"{word}"},
							{"name" : "Canvas", "value" : self.canvas}, 
							]}
					whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (AutoMod)","embeds": [embed],}
					postWebhook(WH_FILTER_URL, whdata)
					return		
				
	def messageIsValid(self,messageData, startTime):
		# Filter out all messages that got sent before the bot started
		# -> Avoid logging the same message twice
		messageTime = datetime.strptime(messageData["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
		if startTime > messageTime:
			return False
		# Filter out global messages if the canvas isnt /7
		if self.canvas != 7 and messageData["channel"] == "global":
			return False
		# Filter out global messages if its logging the nonEng chat 
		if self.isNonEngLogger and messageData["channel"] != "nonenglish":
			return False
		# Filter out nonEng messages if its logging global chat
		if self.canvas == 7 and not self.isNonEngLogger and messageData["channel"] != "global":
			return False
		return True

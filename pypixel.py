#Imports
from webdriver_manager.chrome import ChromeDriverManager

import time
import pathlib
import socketio
import requests
import atexit
import http.client
import redditlogin
from codecs import encode

from debugtool import debugMessage as dm

#Setting 🛣️
class Bot():
	def __init__(self, username, password, canvas, authToken = None,authKey = None,authId = None):
		"""Initializes the Bot class
		Args:
			username (string): A Reddit Username attached to a Pixelplace Account
			password (string): A Password matching the username
			canvas (int, optional): Id of the Pixelplace Canvas. Defaults to 7.
		"""
		#Assigning 💩
		self.username = username
		self.password = password
		self.canvas = canvas
		self.active = False

		self.authId, self.authKey, self.authToken = self.loginuser()
		self.socketconnection = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
		self.AttemptSocketAuth()

		self.active = True

		#Error 🖐ling

		@self.socketconnection.on("throw.error")
		def Place_error(data):
			"""Error Handling for Pixelplace
			Args:
				data (int): id of the Error
			"""
			if data == 0:
				dm(message=f"[{data}] You need to login on pixelplace.io first. Create an account, it's free !", source="Pypxl", prefix="General")
				dm("Attempting Socket Connection", "Pypxl", "General", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 1:
				dm(f"[{data}] Your session expired, please refresh the page", "Pypxl", "General")
				dm("Attempting Socket Connection", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 2:
				dm(f"[{data}] You need to create a username first", "Pypxl", "General")
			if data == 3:
				dm(f"[{data}] Color not found", "Pypxl", "General")
			if data == 4:
				dm(f"[{data}] This color is only available to premium subscribers", "Pypxl", "General")
			if data == 5:
				dm(f"[{data}] Wrong coordinates", "Pypxl", "General")
			if data == 6:
				dm(f"[{data}] This canvas has been temporarily disabled because its owner used premium settings on it and his membership has expired. Please wait for the owner to renew his premium membership or to revert canvas settings to non premium ones")
			if data == 7:
				dm(f"[{data}] Your premium membership has expired and this canvas is using premium settings. To continue, please renew your membership or revert canvas settings back to non premium ones")
			if data == 8:
				dm(f"[{data}] Please wait until the end of your cooldown", "Pypxl", "General")
			if data == 9:
				dm(f"[{data}] This canvas is private, you can't draw on it", "Pypxl", "General")
			if data == 10:
				dm(f"[{data}] To be able to place pixels on this canvas, you have to request approval from the owner", "Pypxl", "General")
				self.requestCanvasApproval()
				#Send feedback per chat and call request function via command
			if data == 11:
				dm(f"[{data}] You are placing pixels too fast, please slow down", "Pypxl", "General")
				#increase timeout slightly to be smart
				#self.timeout += 0.002
			if data == 12:
				dm(f"[{data}] This canvas is terminated", "Pypxl", "General")
			if data == 13:
				dm(f"[{data}] Error while getting canvas data", "Pypxl", "General")
			if data == 14:
				dm(f"[{data}] Error while getting canvas access data", "Pypxl", "General")
			if data == 15:
				dm(f"[{data}] You have too many instances of pixelplace.io opened, please close some windows", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 16:
				dm(f"[{data}] Too many users share your internet connection (are you  using a proxy ?)", "Pypxl", "General")
			if data == 17:
				dm(f"[{data}] Pixelplace.io has been disabled for your internet connection (are you  using a proxy ?)", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 18:
				dm(f"[{data}] Server is full, please try again later", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 19:
				dm(f"[{data}] Reloading...", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)
			if data == 20:
				dm(f"[{data}] Your account has been temporarily disabled for placing pixels and/or sending messages too fast, try again in 5 minutes", "Pypxl", "General")
				self.active = False
				self.switchUser(self.username,self.password)

		@self.socketconnection.event
		def debugConnectionStatus(self):
			dm(f"Connected {self.username} succesfully", f"PyPxl")

	def switchUser(self,username,password):
		self.disconnect()
		self.password = password
		self.username = username
		self.authToken, self.authKey, self.authId = self.loginuser()
		self.AttemptSocketAuth()

	#export auth 💾
	def get_auth(self,cookie):
		for x in cookie:
			if x["name"] == "authToken":
				authToken = str(x["value"])
			elif x["name"] == "authKey":
				authKey = str(x["value"])
			elif x["name"] == "authId":
				authId = str(x["value"])
		return authToken, authKey, authId

	#loggin in user with automation to get auth data
	def loginuser(self,):
		try:
			return redditlogin.login(self.username, self.password)
		except Exception as e:
			print(self.username, "Error:", e)

	def disconnect(self):
		self.socketconnection.disconnect()

	def cleanup(self):
		try:
			self.driver.close()
			self.driver.quit()
			dm("Closed Driver instance","Pypxl")
		except:
			dm("Failed to close Driver instance","Pypxl","Error")

	#Attempt to 🔗 via socketio
	def AttemptSocketAuth(self):
		self.socketconnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
		self.socketconnection.emit(event='init', data={"authKey":self.authKey,"authToken":self.authToken,"authId":self.authId,"boardId":self.canvas})

	#change 🖼
	def changecanvas(self, canvas):
		self.canvas = canvas
		self.disconnect()
		self.AttemptSocketAuth()

	#Place 🎨
	def place_Pixel(self, locx, locy, color, timeout = 0.050, bunch = 1):
		self.socketconnection.emit(event="p", data=[int(locx), int(locy), int(color), 1])
		dm(f"[Bot-Send] Pixel: {locx},{locy} with color {color}", "Pypxl")

		#TODO IMPLEMENT ACCOUNT CLASS BASED TIMEOUT

		time.sleep(timeout)

#can be moved to pypxl
	#send 📍
	def send_Pixel(self, locx, locy, color, announce=True):
		try:
			if (self.active == True):
				self.socketconnection.emit(event="p", data=[int(locx), int(locy), int(color), 1])

				if announce:
					dm(f"[Bot-Send] Pixel Sent from Queue: {locx},{locy} with color {color} for bot {self.ppusername}", "Pypxl", "General")

			else:
				raise Exception("Agent is not active. You have done a big oopsie.")
		except Exception as e:
			print("ERRRROOOOOR" + str(e) + str(e.__traceback__))



	#send 📝
	def send_Chat(self, text, mention, type, target, color, announce):
		"""Sends a Chat Message
		Args:
			text (string): Text of the Message
			mention (string): Name of the People that should be mentioned
			type (string): type of Message
			target (string): Used to indicate message receiver for Private Messages
			color (int): color id of the Message
		"""
		if (self.active == True):
			self.socketconnection.emit(event="chat.message", data={"text": str(text), "mention": str(mention), "type": str(type), "target": str(target), "color": int(color)})
		else:
			raise Exception("Agent is not active. You have done a big oopsie.")
		if announce:
			dm(f"[Bot-Send] Text:{text} Mentions:{mention} Whispered to:{target}", "Pypxl", "General")

	#send 📝🚨
	def send_Command(self, cmd, type):
		self.socketconnection.emit(event="chat.command", data={"cmd": str(cmd), "type": str(type)})

	def requestCanvasApproval(self):
		conn = http.client.HTTPSConnection("pixelplace.io")
		dataList = []
		boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
		dataList.append(encode('--' + boundary))
		dataList.append(encode('Content-Disposition: form-data; name=createRequest;'))

		dataList.append(encode('Content-Type: {}'.format('text/plain')))
		dataList.append(encode(''))

		dataList.append(encode("true"))
		dataList.append(encode('--' + boundary))
		dataList.append(encode('Content-Disposition: form-data; name=message;'))

		dataList.append(encode('Content-Type: {}'.format('text/plain')))
		dataList.append(encode(''))

		dataList.append(encode("This is an automatic request filed by an Agency User. We do not condone anything against TOS and will swiftly take action against Agency Users who break TOS. Please send abuse complaints to JCMS#0557 or Almos#7982 via Discord. Made with ❤️ by PBDT."))
		dataList.append(encode('--' + boundary))
		dataList.append(encode('Content-Disposition: form-data; name=painting;'))

		dataList.append(encode('Content-Type: {}'.format('text/plain')))
		dataList.append(encode(''))

		dataList.append(encode(f"{self.canvas}"))
		dataList.append(encode('--'+boundary+'--'))
		dataList.append(encode(''))

		body = b'\r\n'.join(dataList)
		payload = body
		headers = {
		'Origin': 'https://pixelplace.io',
		'Cookie': f'authId={self.authId}; authKey={self.authKey}; authToken={self.authToken};',
		'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
		}

		conn.request("POST", "/api/get-painting-access.php", payload, headers)
		res = conn.getresponse()
		data = res.read()
		self.approvalStatus = "Pending"
		print('Result of access request: ' + data.decode("utf-8"))

	def DisconnectFromSocket(self):
		self.socketconnection.disconnect()
		self.authToken, self.authKey, self.authId = self.loginuser()
		self.AttemptSocketAuth()


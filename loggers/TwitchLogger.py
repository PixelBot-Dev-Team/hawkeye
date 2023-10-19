import socket
import threading
import re as regex
from lib.util import getTimeStamp,postWebhook

class TwitchLogger:
	def __init__(self, channelName:str, WH_TWITCH_URL:str) -> None:
		self.WH_URL = WH_TWITCH_URL
		server = 'irc.chat.twitch.tv'
		port = 6667
		nickname = 'justinfan12345'
		self.irc_socket = socket.socket()
		self.irc_socket.connect((server, port))
		self.irc_socket.send(f'PASS {nickname}\r\n'.encode('utf-8'))
		self.irc_socket.send(f'NICK {nickname}\r\n'.encode('utf-8'))
		self.irc_socket.send(f'JOIN #{channelName}\r\n'.encode('utf-8'))
		twitch_thread = threading.Thread(target=self.listen,daemon=True)
		twitch_thread.start()

	def listen(self):
		while True:
			message = self.irc_socket.recv(2048).decode('utf-8')
			ping_data = regex.search(r"PING :tmi\.twitch\.tv", message)
			if ping_data:
				self.irc_socket.send(bytes(f"PONG {ping_data.group(0).split(':')[1]}\r\n", "UTF-8"))
				continue
			if message.startswith(":tmi.twitch.tv") or message.startswith(":justinfan12345") or message.startswith("PING"):
				continue
			if "#owmince" in message:
				username = message.split("!")[0][1:].strip()
				text = message.split("#owmince :")[1]
				discordRelativeTimestamp = f"Logged <t:{getTimeStamp()}:R>"
				embed = {"description": f"{text}","title": f"{username}"}
				whdata = {
					"content": f"{discordRelativeTimestamp}",
					"username": "HawkEye (Twitch Logs)",
					"embeds": [embed],
				}
				postWebhook(self.WH_URL,whdata)
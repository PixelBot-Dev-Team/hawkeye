import os.path
import requests
import hashlib

from lib.util import getTimeStamp, postWebhook

class UpdateLogger():
	def __init__(self,WH_UPDATE_URL) -> None:
		self.whurl = WH_UPDATE_URL
		self.checkForUpdate()
	
	def checkForUpdate(self):
		if not os.path.isfile("/data/pphash.txt"):
			md5hash = self.getCurrentHash()
			with open("/data/pphash.txt","w",encoding="utf8") as saved_hash:
				saved_hash.write(md5hash)
				return
		with open("data/pphash.txt","r+",encoding="utf8") as saved_hash:
			old_hash = saved_hash.read()
			new_hash = self.getCurrentHash()
			if new_hash == old_hash:
				return
			else:
				saved_hash.seek(0)
				saved_hash.write(new_hash)
				saved_hash.truncate()
				self.sendEmbed(new_hash)
				
	def getCurrentHash(self):
		# owmince i swear to god if you start changing the file name or the url im gon-
		response = requests.get("https://pixelplace.io/js/script.min.js")
		return hashlib.md5(response.text.encode("utf8")).hexdigest()
	
	def sendEmbed(self,new_hash):
		embed = {
			"title": "New update detected!",
			"description": f"Hash: `{new_hash}`",
		}
		whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Update Logs)","embeds": [embed],}
		postWebhook(self.whurl, whdata)
				
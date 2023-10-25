import requests

from lib.util import background, getItemDict, getProfileData, getTimeStamp, postWebhook

class ItemLogger:
	def __init__(self, master_connection, WH_GIFT_URL:str, WH_ITEMUSE_URL:str) -> None:
		socketConnection = master_connection

		@socketConnection.on("item.notification.gift")
		@background
		def logGifts(data):
			gifter = data["from"]
			gifted = data["to"]
			BADGES_GIFTER, _, USERNAME_EXTRA_GIFTER, GUILD_GIFTER, GUILD_TITLE_GIFTER, GUILD_DIVIDER_GIFTER = getProfileData(gifter)	
			BADGES_GIFTED, _, USERNAME_EXTRA_GIFTED, GUILD_GIFTED, GUILD_TITLE_GIFTED, GUILD_DIVIDER_GIFTED = getProfileData(gifted)	
			itemId = data["item"]
			giftName,urlExtension = getItemDict()[itemId]
			embed = {
				"title": "Gift detected!", 
				"description":"",
				"thumbnail":{"url": f"https://pixelplace.io/img/item-{itemId}{urlExtension}","height": 0,"width": 0},
				"fields" : [
					{"name" : "From", "value" : f"{gifter}{BADGES_GIFTER}{USERNAME_EXTRA_GIFTER}{GUILD_DIVIDER_GIFTER}{GUILD_GIFTER}{GUILD_DIVIDER_GIFTER}{GUILD_TITLE_GIFTER}"}, 
					{"name" : "To", "value" : f"{gifted}{BADGES_GIFTED}{USERNAME_EXTRA_GIFTED}{GUILD_DIVIDER_GIFTED}{GUILD_GIFTED}{GUILD_DIVIDER_GIFTED}{GUILD_TITLE_GIFTED}"}, 
					{"name" : "Item", "value" : f"{giftName}"}
					]} 
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Gift Logs)","embeds": [embed],}
			postWebhook(WH_GIFT_URL, whdata)
		
		@socketConnection.on("item.notification.use")
		@background
		def logItemUse(data):
			username = data["from"]
			item = data["itemName"]
			canvas = data["painting"]
			x = data["x"]
			y = data["y"]
			zoom = 11.55
			BADGES, _, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)	
			itemId = [key for key, value in getItemDict().items() if value == item][0]
			urlExtension = getItemDict()[itemId][1]
			embed = {
				"title": f"{item} used!",
				"description": f"[Take me there!](https://pixelplace.io/{canvas}#x={x}&y={y}&s={zoom})",
				"thumbnail":{"url": f"https://pixelplace.io/img/item-{itemId}{urlExtension}","height": 0,"width": 0},
				"fields" : [
					{"name" : "Username", "value" : f"{username}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE}"}, 
					{"name" : "X", "value" : f"{x}"}, 
					{"name" : "Y", "value" : f"{y}"}
					]}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Item usage Logs)","embeds": [embed],}
			postWebhook(WH_ITEMUSE_URL, whdata)

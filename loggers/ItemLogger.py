import requests

from lib.util import background, getItemDict, getBadgeDict, getTimeStamp, postWebhook

class ItemLogger:
	def __init__(self, master_connection, WH_GIFT_URL:str, WH_ITEMUSE_URL:str) -> None:
		socketConnection = master_connection

		@socketConnection.on("item.notification.gift")
		@background
		def logGifts(data):
			gifter = data["from"]
			gifted = data["to"]
			rich_data_from = requests.get(f"https://pixelplace.io/api/get-user.php?username={gifter}").json()
			try:
				badges = str(rich_data_from["othersIcons"]).split(",")
				badges.append(rich_data_from["premiumIcon"])
				if rich_data_from["vip"]:
					badges.append("vip")
				final_badges_from = ''.join([getBadgeDict()[badge] for badge in badges])
			except KeyError as er:
				print(er)
				final_badges_from = ""
			usernameInsert_from = ""
			if RD_golden_profile := bool(rich_data_from["golden"]):
				usernameInsert_from = usernameInsert_from+"🟨"
			if RD_Rainbow_name := getTimeStamp() < rich_data_from["rainbowTime"]:
				usernameInsert_from = usernameInsert_from+"🌈"
			if RD_Xmas_name := getTimeStamp() < rich_data_from["xmasTime"]:
				usernameInsert_from = usernameInsert_from+"🎄"
			if RD_Halloween_name := getTimeStamp() < rich_data_from["halloweenTime"]:
				usernameInsert_from = usernameInsert_from+"🎃"
			if usernameInsert_from != "":
				usernameInsert_from = " ("+usernameInsert_from+")"
			rich_data_to = requests.get(f"https://pixelplace.io/api/get-user.php?username={gifted}").json()
			try:
				badges = str(rich_data_to["othersIcons"]).split(",")
				badges.append(rich_data_to["premiumIcon"])
				if rich_data_to["vip"]:
					badges.append("vip")
				final_badges_to = ''.join([getBadgeDict()[badge] for badge in badges])
			except KeyError as er:
				final_badges_to = ""
			usernameInsert_to = ""
			if RD_golden_profile := bool(rich_data_to["golden"]):
				usernameInsert_to = usernameInsert_to+"🟨"
			if RD_Rainbow_name := getTimeStamp() < rich_data_to["rainbowTime"]:
				usernameInsert_to = usernameInsert_to+"🌈"
			if RD_Xmas_name := getTimeStamp() < rich_data_to["xmasTime"]:
				usernameInsert_to = usernameInsert_to+"🎄"
			if RD_Halloween_name := getTimeStamp() < rich_data_to["halloweenTime"]:
				usernameInsert_to = usernameInsert_to+"🎃"
			if usernameInsert_to != "":
				usernameInsert_to = " ("+usernameInsert_to+")"
			itemId = data["item"]
			giftName,urlExtension = getItemDict()[itemId]
			embed = {"description":"","title": "Gift detected!", "fields" : [{"name" : "From", "value" : f"{gifter}{final_badges_from}{usernameInsert_from}"}, {"name" : "To", "value" : f"{gifted}{final_badges_to}{usernameInsert_to}"}, {"name" : "Item", "value" : f"{giftName}"}], "color": 15844367, "thumbnail":{"url": f"https://pixelplace.io/img/item-{itemId}{urlExtension}","height": 0,"width": 0}}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Gift Logs)","embeds": [embed],}
			postWebhook(WH_GIFT_URL, whdata)
		
		@socketConnection.on("item.notification.use")
		@background
		def logItemUse(data):
			user = data["from"]
			item = data["itemName"]
			canvas = data["painting"]
			x = data["x"]
			y = data["y"]
			zoom = 11.55
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={user}").json()
			try:
				badges = str(rich_data["othersIcons"]).split(",")
				badges.append(rich_data["premiumIcon"])
				if rich_data["vip"]:
					badges.append("vip")
				final_badges = ''.join([getBadgeDict()[badge] for badge in badges])
			except KeyError as er:
				final_badges = ""
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
			itemId = [key for key, value in getItemDict().items() if value == item][0]
			urlExtension = getItemDict()[itemId][1]
			embed = {"description": f"[Take me there!](https://pixelplace.io/{canvas}#x={x}&y={y}&s={zoom})","title": f"{item} used!", "fields" : [{"name" : "Username", "value" : f"{user}{final_badges}{usernameInsert}"}, {"name" : "X", "value" : f"{x}"}, {"name" : "Y", "value" : f"{y}"}], "color": 1752220, "thumbnail":{"url": f"https://pixelplace.io/img/item-{itemId}{urlExtension}","height": 0,"width": 0}}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Item usage Logs)","embeds": [embed],}
			postWebhook(WH_ITEMUSE_URL, whdata)

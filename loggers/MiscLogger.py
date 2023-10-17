import requests

from lib.util import background, getBadgeDict ,getTimeStamp, postWebhook


class MiscLogger:
	def __init__(self, master_connection, WH_MUTE_URL:str, WH_ANNOUNCE_URL:str, WH_ALERT_URL:str, WH_ONOFF_URL:str, WH_STATS_URL:str) -> None:
		socketConnection = master_connection
		
		@socketConnection.on("chat.system.delete")
		@background
		def logMutes(data):
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={data}").json()
			userCanvasId = rich_data["canvas"]
			badges = str(rich_data["othersIcons"]).split(",").append(rich_data["premiumIcon"])
			if rich_data["vip"]:
				badges.append("vip")
			final_badges = ''.join([getBadgeDict()[badge] for badge in badges])
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
			embed = {"description": "",
					 "title": "Chat Mute detected!", 
					 "thumbnail":{"url": f"https://pixelplace.io/canvas/{userCanvasId}.png","height": 0,"width": 0},
					 "fields" : [{"name" : "Muted User", "value" : f"{data}{final_badges}{usernameInsert}"}], "color": 2123412}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069701352479010846> ||","username": "HawkEye (Mute Logs)","embeds": [embed],}
			postWebhook(WH_MUTE_URL, whdata)

		@socketConnection.on("chat.system.announce")
		@background
		def logAnnounce(message):
			embed = {"title": "New Global Announcement!","description": f"{message}",} 
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Announce Logs)","embeds": [embed],}
			postWebhook(WH_ANNOUNCE_URL, whdata)
			
		@socketConnection.on("canvas.alert")
		@background
		def logAlerts(message):
			embed = {"title": "New Canvas Alert!","description": f"{message}",} 
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Alert Logs)","embeds": [embed],}
			postWebhook(WH_ALERT_URL, whdata)
		
		@socketConnection.on("j")
		@background
		def logJoins(data):
			if data == "":
				return
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={data}").json()
			userCanvasId = rich_data["canvas"]
			try:
				badges = str(rich_data["othersIcons"]).split(",")
				badges.append(rich_data["premiumIcon"])
				if rich_data["vip"]:
					badges.append("vip")
				final_badges = ''.join([getBadgeDict()[badge] for badge in badges])	
			except:
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
			embed = {"description": f"{data}{final_badges}{usernameInsert} joined!","title": "Joins", "color": 2531122, "thumbnail":{"url": f"https://pixelplace.io/canvas/{userCanvasId}.png","height": 0,"width": 0}} #green
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Join Logs)","embeds": [embed],}
			postWebhook(WH_ONOFF_URL, whdata)

		@socketConnection.on("l")
		@background
		def logLeaves(data):
			if data == "":
				return
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={data}").json()
			userCanvasId = rich_data["canvas"]
			try:
				badges = str(rich_data["othersIcons"]).split(",")
				badges.append(rich_data["premiumIcon"])
				if rich_data["vip"]:
					badges.append("vip")
				final_badges = ''.join([getBadgeDict()[badge] for badge in badges])	
			except:
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
			embed = {"description": f"{data}{final_badges}{usernameInsert} left!","title": "Leaves", "color": 13571349, "thumbnail":{"url": f"https://pixelplace.io/canvas/{userCanvasId}.png","height": 0,"width": 0}} #red
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Leave Logs)","embeds": [embed],}
			postWebhook(WH_ONOFF_URL, whdata)
					
		@socketConnection.on("chat.stats")
		@background
		def logStats(data):
			UsersCount = data[0]
			ConnectionsCount = data[1]
			embed = {"description": "","title": "Stats", "fields" : [{"name" : "Users", "value" : f"{UsersCount}"}, {"name" : "Individual Connections", "value" : f"{ConnectionsCount}"}, {"name" : "Connections per user (Ø)", "value" : f"{round(ConnectionsCount / UsersCount,2)}"}], "color": 16776958}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Stat Logs)","embeds": [embed],}
			postWebhook(WH_STATS_URL, whdata)
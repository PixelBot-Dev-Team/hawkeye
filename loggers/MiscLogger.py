import requests

from lib.util import background, getProfileData ,getTimeStamp, postWebhook


class MiscLogger:
	def __init__(self, master_connection, WH_MUTE_URL:str, WH_ANNOUNCE_URL:str, WH_ALERT_URL:str, WH_ONOFF_URL:str, WH_STATS_URL:str) -> None:
		socketConnection = master_connection
		
		@socketConnection.on("chat.system.delete")
		@background
		def logMutes(username):
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)		
			embed = {"description": "",
					 "title": "Chat Mute detected!", 
					 "thumbnail":{"url": f"https://pixelplace.io/canvas/{PFP_CANVAS_ID}.png","height": 0,"width": 0},
					 "fields" : [
						 {"name" : "Muted User", "value" : f"{username}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE}"}
						 ]}
			#                                                       {      Mute Ping      }
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
		def logJoins(username):
			if username == "":
				return
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)	
			embed = {
				"title": "Joins",
				"description": f"{username}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE} joined!",
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{PFP_CANVAS_ID}.png","height": 0,"width": 0},
				}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Join Logs)","embeds": [embed],}
			postWebhook(WH_ONOFF_URL, whdata)

		@socketConnection.on("l")
		@background
		def logLeaves(username):
			if username == "":
				return
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)	
			embed = {
				"title": "Leaves",
				"description": f"{username}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE} left!",
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{PFP_CANVAS_ID}.png","height": 0,"width": 0},
				}
			# embed = {"description": f"{data}{final_badges}{usernameInsert} left!","title": "Leaves", "color": 13571349, "thumbnail":{"url": f"https://pixelplace.io/canvas/{userCanvasId}.png","height": 0,"width": 0}} #red
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
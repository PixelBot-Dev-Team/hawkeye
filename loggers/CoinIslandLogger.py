from lib.util import background ,getTimeStamp, postWebhook, getProfileData

class CoinIslandLogger:
	def __init__(self, master_connection, WH_CICHANGE_URL:str) -> None:
		socketConnection = master_connection

		CoinIsland_roles = {
			0:"<@&1069696793702584320>",
			1:"<@&1069696820730667120>",
			2:"<@&1069696859012083762>",
			3:"<@&1069696893585719367>",
		}

		@socketConnection.on("coin_island_owner_change")
		@background
		def logCoinIslandChanges(data):
			newOwner = data["from"]
			coinsGained = data["amount"]
			islandId = data["island"]
			coinIslandPing = CoinIsland_roles[islandId]
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(newOwner)	
			embed = {
				"title": f"Coin Island {islandId} has a new Owner",
				"description": "",
				"thumbnail":{"url": f"https://pixelplace.io/canvas/{PFP_CANVAS_ID}.png","height": 0,"width": 0}, 
				"fields" : [
					{"name" : "New Owner", "value" : f"{newOwner}{BADGES}{USERNAME_EXTRA}{GUILD_DIVIDER}{GUILD}{GUILD_DIVIDER}{GUILD_TITLE}"},
					{"name" : "Coins gained", "value" : f"{coinsGained}"},
				]}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || {coinIslandPing} ||","username": "HawkEye (Coin Island Logs)","embeds": [embed]}
			postWebhook(WH_CICHANGE_URL, whdata)
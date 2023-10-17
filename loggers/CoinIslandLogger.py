import requests

from lib.util import background, getBadgeDict ,getTimeStamp, postWebhook

class CoinIslandLogger:
	def __init__(self, master_connection, WH_CICHANGE_URL) -> None:
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
			ping = CoinIsland_roles[islandId]
			rich_data = requests.get(f"https://pixelplace.io/api/get-user.php?username={newOwner}").json()
			canvasId = rich_data["canvas"]
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
			embed = {"description": "","title": f"Coin Island {islandId} has a new Owner", "fields" : [{"name" : "New Owner", "value" : f"{newOwner}{final_badges}{usernameInsert}"}, {"name" : "Coins gained", "value" : f"{coinsGained}"}], "color": 12745742, "thumbnail":{"url": f"https://pixelplace.io/canvas/{canvasId}.png","height": 0,"width": 0}} #yellow
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || {ping} ||","username": "Coin Island Logs","embeds": [embed],}
			postWebhook(WH_CICHANGE_URL, whdata)
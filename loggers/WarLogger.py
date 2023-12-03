import requests

from lib.util import background, getTimeStamp, postWebhook

class WarLogger:
	def __init__(self, master_connection, WH_WAR_URL) -> None:
		socketConnection = master_connection
		
		warAreas = {
			"0":["Australia",[2144,1330,16]],
			"1":["Russia",[1919,472,176]],
			"2":["Africa",[1269,973,16]],
			"3":["Antarctica",[1327,1772,16]],
			"4":["Canada",[473,675,16]],
			"5":["Brazil",[826,1214,16]],
			"6":["China",["x","y",16]],
			"7":["Greenland",[890,211,16]],
			"8":["US",[477,833,16]],
		}

		@socketConnection.on("area_fight_start")
		@background
		def postWarStart(data):
			warType = "Player" if data["fightType"] else "Guild"
			warInfo = warAreas[data["id"]]
			area = warInfo[0]
			x = warInfo[1][0]
			y = warInfo[1][1]
			s = warInfo[1][2]
			endTime = int(data["fightEndAt"])
			embed = {"description": "","title": f"A new {warType} war has started!", "fields" : [{"name" : "Area", "value" : f"[{area}](https://pixelplace.io/7-pixels-world-war#x={x}&y={y}&s={s})"}, {"name" : "End", "value" : f"<t:{endTime}:R>"}], "color": 15158332}
			#                                                       {      Wars Ping      }
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> || <@&1069696750060838942> ||","username": "HawkEye (War Logs)","embeds": [embed],}
			postWebhook(WH_WAR_URL, whdata)


		@socketConnection.on("area_fight_end")
		@background
		def logWarEnd(data):
			warInfo = warAreas[data["id"]]			
			area = warInfo[0]
			x = warInfo[1][0]
			y = warInfo[1][1]
			s = warInfo[1][2]
			nextWar = getTimeStamp() + data["nextFight"] - 120 # 120 = time the fight itself takes
			newOwner = data["ownedBy"]
			warType = "player" if data["fightType"] == 1 else "guild"			
			if newOwner == "":
				embed = {"description":"No Winner :c","title": f"The {warType} War has ended!", "fields" : [{"name" : "Area", "value" : f"[{area}](https://pixelplace.io/7-pixels-world-war#x={x}&y={y}&s={s})"}, {"name" : "Next war in", "value" : f"<t:{nextWar}:R>"}], "color": 15158332}
				whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (War Logs)","embeds": [embed],}
				postWebhook(WH_WAR_URL, whdata)
				return
			warStats = data["stats"]
			if data["fightType"]:
				# player war
				usernames = [entry["username"] for entry in warStats]
				usernames.append("Username")
				usernameColumnLength = len(sorted(usernames,key=len)[-1])
			pixelsColumnLength = len(sorted([str(entry["pixels"]) for entry in warStats],key=len)[-1])
			if data["fightType"]:
				# player war
				tableText = f"""{str('Username').ljust(usernameColumnLength)} | {str('Guild').center(5)} | {str('px').rjust(pixelsColumnLength)}\n{str("-") * (usernameColumnLength + pixelsColumnLength + 5 + 6)}"""
			else:
				tableText = f"""{str('Guild').center(5)} | {str('Users').ljust(6)} | {str('px').rjust(pixelsColumnLength)}\n{str("-") * (6 + pixelsColumnLength + 5 + 6)}"""
			for entry in warStats:
				if entry["guild"] == "":
					entry["guild"] = "----"
				if data["fightType"]:
					tableText = f"""{tableText}\n{entry["username"].ljust(usernameColumnLength)} | {entry["guild"].ljust(5)} | {str(entry["pixels"]).rjust(pixelsColumnLength)}"""			
				else:
					tableText = f"""{tableText}\n{entry["guild"].ljust(5)} | {str(entry["users"]).ljust(6)} | {str(entry["pixels"]).rjust(pixelsColumnLength)}"""
			if data["fightType"]:
				# player war
				tableText = f"""{tableText}\n{str("-") * (usernameColumnLength + pixelsColumnLength + 5 + 6)}\n{"Total".ljust(usernameColumnLength)} | {"----".ljust(5)} | {str(data["total"]["pixels"]).rjust(pixelsColumnLength)}"""
			else:
				tableText = f"""{tableText}\n{str("-") * (6 + pixelsColumnLength + 5 + 6)}\n{"Total".ljust(5)} | {str(data["total"]["users"]).ljust(6)} | {str(data["total"]["pixels"]).rjust(pixelsColumnLength)}"""
			only_results_data = data.copy()
			resultsText = """"""
			for key in ["id","defended","ownedBy","ownedByGuild","previousOwner","fightType","stats","nextFight","canvas","total"]:
				del only_results_data[key]
			for key,value in only_results_data.items():
				resultsText = f"""{resultsText}{str(key).capitalize()}: {value}\n"""		
			finalText = f"""**Winner**\n{newOwner}\n\n**Rewards**\n{resultsText}\n**Stats**\n```{tableText}```"""			
			embed = {"description": finalText,"title": f"The {warType} War has ended!", "fields" : [{"name" : "Area", "value" : f"[{area}](https://pixelplace.io/7-pixels-world-war#x={x}&y={y}&s={s})"}, {"name" : "Next war in", "value" : f"<t:{nextWar}:R>"}], "color": 15158332, "thumbnail":{"url": f"https://pixelplace.io/canvas/{data['canvas']}.png","height": 0,"width": 0}}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (War Logs)","embeds": [embed],}
			postWebhook(WH_WAR_URL, whdata)

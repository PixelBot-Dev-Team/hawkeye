from lib.dbutil import create_database,add_mute_stats,add_user_stats,add_connection_stats,add_item_stats,add_coin_island_reward_stats,add_war_stats
from lib.util import background,getTimeStamp

class DataLogger:
	def __init__(self, master_connection) -> None:
		create_database()
		socketConnection = master_connection
		
		@socketConnection.on("chat.system.delete")
		@background
		def saveMutes(username):
			add_mute_stats(getTimeStamp(),username)

		@socketConnection.on("chat.stats")
		@background
		def saveStats(data):
			UsersCount = data[0]
			ConnectionsCount = data[1]
			average = round(ConnectionsCount / UsersCount,2)
			add_user_stats(getTimeStamp(),UsersCount,ConnectionsCount,average)
			
		@socketConnection.on("j")
		@background
		def saveJoins(username):
			if username == "":
				return
			add_connection_stats(getTimeStamp(),1,username)			
		
		@socketConnection.on("l")
		@background
		def saveLeaves(username):
			if username == "":
				return
			add_connection_stats(getTimeStamp(),0,username)				
			
		@socketConnection.on("item.notification.use")
		@background
		def saveItemUse(data):
			username = data["from"]
			itemId = data["item"]
			x = data["x"]
			y = data["y"]
			add_item_stats(getTimeStamp(),itemId,f"{x},{y}",username)
			
		@socketConnection.on("coin_island_owner_change")
		@background
		def logCoinIslandReward(data):
			coinsGained = data["amount"]
			islandId = data["island"]
			add_coin_island_reward_stats(getTimeStamp(),islandId,coinsGained)
			
		@socketConnection.on("area_fight_end")
		@background
		def saveWarStats(data):
			warStats = data["stats"]
			# warType = "player" if data["fightType"] == 1 else "guild"
			if data["fightType"]:
				participants = len([entry["username"] for entry in warStats])
			else:
				participants = data["total"]["users"]
			warType = data["fightType"]
			add_war_stats(getTimeStamp(),warType,participants,data["total"]["pixels"],data["points"])
		
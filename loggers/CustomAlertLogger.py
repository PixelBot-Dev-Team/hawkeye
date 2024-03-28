from lib.alertutil import add_customMessage_alert, add_join_alert, add_leave_alert, add_to_pending_redemptions, create_database, get_active_custom_word_alerts, get_active_join_alerts, get_active_leave_alerts, get_pending_redemptions
from lib.util import background, getProfileData, getTimeStamp, postWebhook
from loggers.ChatLogger import ChatMessage

timeByItemId  = {
	5 : 60 * 60 * 24 * 730,
	13 : 60 * 60 * 24 * 365,
	4 : 60 * 60 * 24 * 180,
	11 : 60 * 60 * 24 * 90,
	10 : 60 * 60 * 24 * 45,
	12 : 60 * 60 * 24 * 45,
	9 : 60 * 60 * 24 * 25,
	3 : 60 * 60 * 24 * 20,
	6 : 60 * 60 * 24 * 10,
	7 : 60 * 60 * 24 * 5,
	8 : 60 * 60 * 24 * 5,
	1 : 60 * 60 * 48,
	2 : 60 * 60 * 24,
}

class CustomAlertLogger:
	def __init__(self, master_connection, WH_CUSTOMALERT_URL:str, gifted_username = "GiftBank") -> None:
		create_database()
		socketConnection = master_connection
		self.giftedUsername = gifted_username.lower()
		
		# when GiftBank account gets a gift, add a pending redemption for gifter with the corresponding duration
		@socketConnection.on("item.notification.gift")
		@background
		def addToCanRedeemList(data):
			username = data["from"]
			if str(data["to"]).lower() == self.giftedUsername:
				alertDuration = timeByItemId[int(data["item"])]
				add_to_pending_redemptions(username,alertDuration)
		
		@socketConnection.on("chat.user.message")
		def readChat(messageData):
			chatMessageObject = ChatMessage(messageData)
			# Check if someone wants to register a new alert
			if chatMessageObject.MENTIONS.lower() == self.giftedUsername:
				duration = get_pending_redemptions(chatMessageObject.USERNAME)
				if duration == None:
					return
				self.parseAlert(chatMessageObject,duration)
			# no one wants to register a new alert, continue to check for customWords
			activeAlerts = get_active_custom_word_alerts()
			for text,discordId in activeAlerts:
				if text.lower() in chatMessageObject.TEXT.lower():
					embedText = f"{chatMessageObject.USERNAME}{chatMessageObject.getBadgesAsEmotes()}{chatMessageObject.USERNAME_EXTRA} triggered your alert for '{text}'! ({chatMessageObject.TEXT})"
					embed = {
						"title": "Triggered custom text alert!",
						"description": embedText,
					}
					webhookData = {
						"content": f"Logged <t:{getTimeStamp()}:R> ||<@{discordId}>||",
						"username": f"HawkEye (Custom alerts)",
						"embeds": [embed],
					}
				postWebhook(WH_CUSTOMALERT_URL,webhookData)
		
		@socketConnection.on("j")
		def readJoin(username):
			if username == "":
				return
			# gets a list of discord ids that want to get alerted for this
			discordIds = get_active_join_alerts(username)
			if discordIds is None:
				return
			mentions = ' '.join(f'<@{discordId}>' for discordId in discordIds)
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)	
			embed = {
				"title": "Triggered join alert!",
				"description": f"{username}{BADGES}{USERNAME_EXTRA} joined!",
				}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> ||{mentions}||","username": "HawkEye (Custom alerts)","embeds": [embed],}
			postWebhook(WH_CUSTOMALERT_URL, whdata)
		
		@socketConnection.on("l")
		def readJoin(username):
			if username == "":
				return
			# gets a list of discord ids that want to get alerted for this
			discordIds = get_active_leave_alerts(username)
			if discordIds is None:
				return
			mentions = " ".join(f"<@{discordId}>" for discordId in discordIds)
			BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER = getProfileData(username)	
			embed = {
				"title": "Triggered leave alert!",
				"description": f"{username}{BADGES}{USERNAME_EXTRA} left!",
				}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R> ||{mentions}||","username": "HawkEye (Custom alerts)","embeds": [embed],}
			postWebhook(WH_CUSTOMALERT_URL, whdata)
		
	def parseAlert(self,chatMessage:ChatMessage,duration):
		message = chatMessage.TEXT
		alertType = message.split(" ")[0]
		rest:str = message.split(" ")[1:]
		try:
			match alertType.lower():
				case "join":
					joiningUsername,discordId = message.split(" ")[1:]
					add_join_alert(joiningUsername,duration,discordId)
				case "leave":
					leavingUsername,discordId = message.split(" ")[1:]
					add_leave_alert(leavingUsername,duration,discordId)
				case "customword":
					text = " ".join(rest.split(" ")[1:-1])
					discordId = rest.split(" ")[-1]
					add_customMessage_alert(text,duration,discordId)
		except Exception:
			pass # user is stupid what do i care lol read the instructions idiot | wait this is open source now so ppl can see this comment... meh who cares
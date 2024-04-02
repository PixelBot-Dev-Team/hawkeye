import datetime
import os
import time

from socketio import Client
from socketio.exceptions import ConnectionError

from loggers.ChatLogger import ChatLogger
from loggers.MiscLogger import MiscLogger
from loggers.ItemLogger import ItemLogger
from loggers.CoinIslandLogger import CoinIslandLogger
from loggers.WarLogger import WarLogger
from loggers.TwitchLogger import TwitchLogger
from loggers.AuctionLogger import AuctionLogger
from loggers.DataLogger import DataLogger
from loggers.CustomAlertLogger import CustomAlertLogger
from loggers.UpdateLogger import UpdateLogger
from dotenv import load_dotenv

try:
	load_dotenv()
except Exception:
	pass

WH_DICT = os.environ.copy()

# ---

connected = False

while not connected:
	try:
		masterConnection = Client(reconnection=True, logger=False, engineio_logger=False)
		masterConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
		masterConnection.emit(event='init', data={"authId":f"HawkEye (Master Connection)","boardId":7})
		connected = True
	except ConnectionError:
		print("didnt connect retrying")
		time.sleep(2)

startTime = datetime.datetime.utcnow()

GlobalLog = ChatLogger(startTime,7,WH_DICT["WH_GLOBAL_URL"],WH_DICT["WH_OWMINCE_URL"],WH_DICT["WH_MUTE_URL"],WH_DICT["WH_ALERT_URL"],WH_DICT["WH_MOD_URL"])
NonEngLog = ChatLogger(startTime,-1,WH_DICT["WH_NONENG_URL"],WH_DICT["WH_OWMINCE_URL"],WH_DICT["WH_MUTE_URL"],WH_DICT["WH_ALERT_URL"],WH_DICT["WH_MOD_URL"])
AnarchyLog = ChatLogger(startTime,13,WH_DICT["WH_ANARCH_URL"],WH_DICT["WH_OWMINCE_URL"],WH_DICT["WH_MUTE_URL"],WH_DICT["WH_ALERT_URL"],WH_DICT["WH_MOD_URL"])
MVPLog = ChatLogger(startTime,8,WH_DICT["WH_MVP_URL"],WH_DICT["WH_OWMINCE_URL"],WH_DICT["WH_MUTE_URL"],WH_DICT["WH_ALERT_URL"],WH_DICT["WH_MOD_URL"])

# Logging stuff into the db
Datalogger = DataLogger(masterConnection)

# Chat Stats, Mutes, Announcements, Alerts, Join Leave, 
MiscLogger = MiscLogger(masterConnection,WH_DICT["WH_MUTE_URL"],WH_DICT["WH_ANNOUNCE_URL"],WH_DICT["WH_ALERT_URL"],WH_DICT["WH_ONOFF_URL"],WH_DICT["WH_STATS_URL"])

# Item Use, Item Gift
ItemLogger = ItemLogger(masterConnection,WH_DICT["WH_GIFT_URL"],WH_DICT["WH_ITEMUSE_URL"])

# Coins Island owner change
CoinIslandLogger = CoinIslandLogger(masterConnection, WH_DICT["WH_CICHANGE_URL"])

# war start and end
WarLogger = WarLogger(masterConnection,WH_DICT["WH_WAR_URL"])

# New Auction/bid, ending auction
AuctionLogger = AuctionLogger(masterConnection,WH_DICT["WH_AUCTION_URL"])

# Pixelplace code updates
UpdateLogger = UpdateLogger(WH_DICT["WH_UPDATE_URL"])

# Custom Alerts
# CustomAlertLogger = CustomAlertLogger(masterConnection,WH_DICT["WH_CUSTOMALERT_URL"])

# Owmince twitch chat
TwitchLogger = TwitchLogger("owmince",WH_DICT["WH_TWITCH_URL"])

# ---

from lib.util import getTimeStamp, postWebhook
embed = {
	"title": "Event",
	"description": "Started!",
	}
whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Event Logs)","embeds": [embed],}
postWebhook(WH_DICT["WH_EVENT_URL"], whdata)

from lib.util import getTimeStamp

while connected:
	time.sleep(10)
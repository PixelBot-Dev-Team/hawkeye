import datetime
import os

from socketio import Client

from loggers.ChatLogger import ChatLogger
from loggers.MiscLogger import MiscLogger
from loggers.ItemLogger import ItemLogger
from loggers.CoinIslandLogger import CoinIslandLogger
from loggers.WarLogger import WarLogger
from loggers.TwitchLogger import TwitchLogger
from loggers.AuctionLogger import AuctionLogger

for key,value in os.environ.items():
	print(key,value)

masterConnection = Client(reconnection=True, logger=False, engineio_logger=False)
masterConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
masterConnection.emit(event='init', data={"authId":f"HawkEye (Master Connection)","boardId":7})

startTime = datetime.datetime.utcnow()

# TODO | Do some .env stuff

GlobalLog = ChatLogger(7,"WH_GLOBAL_URL",startTime,)
NonEngLog = ChatLogger(7,"WH_NONENG_URL",startTime,non_eng_overwrite=True)
AnarchyLog = ChatLogger(13,"WH_ANARCH_URL",startTime,checkMessage=False)
MVPLog = ChatLogger(8,"WH_MVP_URL",startTime)

# Chat Stats, Mutes, Announcements, Alerts, Join Leave, 
MiscLogger = MiscLogger(masterConnection,"WH_MUTE_URL","WH_ANNOUNCE_URL","WH_ALERT_URL","WH_ONOFF_URL","WH_STATS_URL")

# Item Use, Item Gift
ItemLogger = ItemLogger(masterConnection,"WH_GIFT_URL","WH_ITEMUSE_URL")

# Coins Island owner change
CoinIslandLogger = CoinIslandLogger(masterConnection, "WH_CICHANGE_URL")

# war start and end
WarLogger = WarLogger(masterConnection,"WH_WAR_URL")

# Owmince twitch chat
TwitchLogger = TwitchLogger("owmince","WH_TWITCH_URL")

# New Auction/bid, ending auction
AuctionLogger = AuctionLogger(masterConnection,"WH_AUCTION_URL")

input("CTRL + C TO EXIT")
exit()
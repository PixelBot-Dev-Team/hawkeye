import datetime

from socketio import Client

from loggers.ChatLogger import ChatLogger
from loggers.MiscLogger import MiscLogger
from loggers.ItemLogger import ItemLogger
from loggers.CoinIslandLogger import CoinIslandLogger
from loggers.WarLogger import WarLogger
from loggers.TwitchLogger import TwitchLogger
from loggers.AuctionLogger import AuctionLogger

masterConnection = Client(reconnection=True, logger=False, engineio_logger=False)
masterConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
masterConnection.emit(event='init', data={"authId":f"HawkEye (Master Connection)","boardId":7})

startTime = datetime.datetime.utcnow()

# GlobalLog = ChatLogger(7,"PLACEHOLDER",startTime,)
# NonEngLog = ChatLogger(7,"PLACEHOLDER",startTime,non_eng_overwrite=True)
# AnarchyLog = ChatLogger(13,"PLACEHOLDER",startTime,checkMessage=False)
# MVPLog = ChatLogger(8,"PLACEHOLDER",startTime)

# Chat Stats, Mutes, Announcements, Alerts, Join Leave, 
# MiscLogger = MiscLogger(masterConnection,"WH_MUTE","WH_ANNOUNCE","WH_ALERT","WH_ONOFF","WH_STATS")

# Item Use, Item Gift
# ItemLogger = ItemLogger(masterConnection,"WH_GIFT","WH_ITEMUSE")

# Coins Island owner change
# CoinIslandLogger = CoinIslandLogger(masterConnection, "WH_CICHANGE")

# war start and end
# WarLogger = WarLogger(masterConnection,"WH_WAR_URL")

# Owmince twitch chat
# TwitchLogger = TwitchLogger("owmince","WH_TWITCH_URL")

# New Auction/bid, ending auction
AuctionLogger = AuctionLogger(masterConnection,"WH_AUCTION_URL")

input("CTRL + C TO EXIT")
exit()
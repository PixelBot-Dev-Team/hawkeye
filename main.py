import datetime

from socketio import Client

from loggers.ChatLogger import ChatLogger


masterConnection = Client(reconnection=True, logger=True, engineio_logger=False)
masterConnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
# masterConnection.emit(event='init', data={"authId":f"HawkEye (Master Connection)","boardId":7})

startTime = datetime.datetime.utcnow()

# GlobalLog = ChatLogger(7,"PLACEHOLDER",startTime,)
# NonEngLog = ChatLogger(7,"PLACEHOLDER",startTime,non_eng_overwrite=True)
# AnarchyLog = ChatLogger(13,"PLACEHOLDER",startTime,checkMessage=False)
# MVPLog = ChatLogger(8,"PLACEHOLDER",startTime)

input("CTRL + C TO EXIT")
exit()
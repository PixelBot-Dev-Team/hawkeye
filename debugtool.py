import time

def debugMessage(message, source, prefix="Info") -> str:
	"""Prints a Message with Timestamp and Debug Prefix
	Args:
		message (string): Message to display
		source (string): Source of the Message (Default: Unknown Source)
		prefix (string): Type of Message (General, Info, Warning, Error) (Default: General)
	"""
	timestamp = f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
	print(f"{timestamp} [{source}, {prefix}] {message}")
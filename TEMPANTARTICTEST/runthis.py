from PIL import Image

Bot = pypxl.Bot("pbt_ttt_6", "85*0zCHaNlAPbVm%bB^EC", canvas = 7, premium=False)
Bot.AttemptSocketAuth()

def fill4(x,y,color):
	stack = []
	trash = []
	stack.append([x, y])
	while len(stack) != 0:
		x,y = stack.pop()
		if getPixel7(x, y) != (204, 204, 204, 255):
			Bot.place_Pixel(x,y,color)
			print(f"Placing {x},{y}!")
			trash.append([x,y])
			if [x,y + 1] not in stack and [x,y + 1] not in trash:
				stack.append([x,y + 1])
			if [x,y - 1] not in stack and [x,y - 1] not in trash:
				stack.append([x,y - 1])
			if [x + 1,y] not in stack and [x + 1,y] not in trash:
				stack.append([x + 1,y])
			if [x - 1,y] not in stack and [x - 1,y] not in trash:
				stack.append([x - 1,y])
		else:
			print(f"Skipping {x},{y}!")
	else:
		print(f"Done!")

def startChatFill(x,y,color):
	fill4(x,y,color)

global c7img	
im = Image.open(f"{CurrentDir}\\7.png")
c7img = im.load()

#(204, 204, 204, 255) is border color
#(255, 255, 255, 255) is white
def getPixel7(x,y):
	global c7img
	color = c7img[x,y]
	return color

startChatFill(1378, 1826, 29)
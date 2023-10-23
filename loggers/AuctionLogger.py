import base64
from lib.util import background,getTimeStamp,postWebhook
import requests
from PIL import Image
from io import BytesIO

class AuctionLogger:
	def __init__(self, master_connection, WH_AUCTION_URL:str) -> None:
		socketConnection = master_connection

		frames = { # TODO | put only copper,iron,pyrite in here
			1 : "./lib/assets/frames/copper-frame-bg.png",
			2 : "./lib/assets/frames/iron-frame-bg.png",
			3 : "./lib/assets/frames/pyrite-frame-bg.png",
		}

		gems = {
			1 : "./lib/assets/gems/emerald-frame-bg.png",
			2 : "./lib/assets/gems/sapphire-frame-bg.png",
			3 : "./lib/assets/gems/ruby-frame-bg.png",
		}

		@socketConnection.on("auction.new.bid")
		@background
		def logNewAuctionBid(data):
			# set data 
			ED_AUCTION_ID = data["id"]
			ED_AUCTION_EXPIRES = data["auction_expire_time"]
			ED_AUCTION_OWNER_BADGES = data["author_icons"]
			ED_AUCTION_OWNER_NAME = data["author_username"]
			ED_AUCTION_BIDS = data["bids"]			
			ED_AUCTION_BID_PRICE = data["current_bid"]
			ED_AUCTION_BID_NAME = data["current_bid_username"]
			ID_FRAME = data["frame_id"]
			ID_GEMS = data["gems_id"]
			ID_PAINTING = data["painting_id"]			
			# create image
			canvas_image_url = f"https://pixelplace.io/canvas/{ID_PAINTING}.png"
			response = requests.get(canvas_image_url)
			canvas_image = Image.open(BytesIO(response.content))
			frame_image = Image.open(frames[ID_FRAME])
			gem_image = Image.open(gems[ID_GEMS])
			frame_image.alpha_composite(canvas_image,(18,18))
			frame_image.alpha_composite(gem_image,(6,6))
			frame_image.save(img_bytes := BytesIO(),format="PNG")
			finalImageUrl = upload_to_dc(img_bytes.getvalue())['data']["proxy_url"]
			embed = {"description": "","title": f"New Bid on Auction #{ED_AUCTION_ID}", "thumbnail":{"url":finalImageUrl,"height": 136,"width": 136},
			 "fields" : [
				{"name" : "Auction Owner", "value" :ED_AUCTION_OWNER_NAME}, {"name" : "Current Bid", "value" : f"{ED_AUCTION_BID_NAME} | {ED_AUCTION_BID_PRICE} coins"}, {"name" : "Amount of Bids", "value" : ED_AUCTION_BIDS}, {"name" : "Ends", "value" : f"<t:{ED_AUCTION_EXPIRES}:R>"}], "color": 15158332, } #yellow
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Auction Logs)","embeds": [embed],}
			postWebhook(WH_AUCTION_URL,whdata)
			
		@socketConnection.on("auction.notification.win")
		@background
		def logAuctionWin(data):
			ED_AUCTION_ID = data["id"]
			ED_AUCTION_OWNER_BADGES = data["author_icons"]
			ED_AUCTION_OWNER_NAME = data["author_username"]
			ED_AUCTION_BIDS = data["bids"]
			ED_AUCTION_WIN_PRICE = data["current_bid"]
			ED_AUCTION_WIN_NAME = data["current_bid_username"]
			ID_FRAME = data["frame_id"]
			ID_GEMS = data["gems_id"]
			ID_PAINTING = data["painting_id"]
			# create image
			canvas_image_url = f"https://pixelplace.io/canvas/{ID_PAINTING}.png" 
			response = requests.get(canvas_image_url)
			canvas_image = Image.open(BytesIO(response.content))
			frame_image = Image.open(frames[ID_FRAME])
			gem_image = Image.open(gems[ID_GEMS])
			frame_image.alpha_composite(canvas_image,(18,18))
			frame_image.alpha_composite(gem_image,(6,6))
			frame_image.save(img_bytes := BytesIO(),format="PNG")
			finalImageUrl = upload_to_dc(img_bytes.getvalue())['data']["proxy_url"]
			embed = {"description": "","title": f"Auction #{ED_AUCTION_ID} ended!", "thumbnail":{"url":finalImageUrl,"height": 136,"width": 136},
			 "fields" : [
				{"name" : "Auction Owner", "value" :ED_AUCTION_OWNER_NAME}, {"name" : "Winning Bid", "value" : f"{ED_AUCTION_WIN_NAME} | {ED_AUCTION_WIN_PRICE} coins"}, {"name" : "Amount of Bids", "value" : ED_AUCTION_BIDS}], "color": 15158332, } #yellow
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Auction Logs)","embeds": [embed],}
			postWebhook(WH_AUCTION_URL,whdata)
		
		
def upload_to_dc(file):
	api_url = "https://discord-storage.animemoe.us/api/upload-from-file/"	
	response = requests.request("POST", api_url, files={"file": file})
	return {"status": response.status_code, "data": response.json()}

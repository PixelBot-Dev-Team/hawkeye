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
		def logNewAuctionBid():
			data = {"id":30,"owner_id":246777,"owner_username":"Art","under_auction":1,"painting_id":81996,"author_id":174569,"author_username":"DrugToweI","author_icons":"","frame_id":1,"gems_id":1,"current_bid":400,"current_bid_user_id":318520,"current_bid_username":"Dfghfgds","auction_expire_time":1697046604,"bids":1,"sp":0,"bg":0,"burned":0,"created_at":1696361440,"previous_bidder":0}
			# set data 
			ED_AUCTION_ID = data["id"]
			ED_AUCTION_EXPIRES = data["auction_expire_time"]
			ED_AUCTION_OWNER_BADGES = data["author_icons"]
			ED_AUCTION_OWNER_NAME = data["author_username"]
			ED_AUCTION_BIDS = data["bids"]			
			ED_AUCTION_CREATED = data["created_at"]
			ED_AUCTION_BID_PRICE = data["current_bid"]
			ED_AUCTION_BID_NAME = data["current_bid_username"]
			ID_FRAME = data["frame_id"]
			ID_GEMS = data["gems_id"]
			ID_PAINTING = data["painting_id"]			
			# create image
			canvas_image_url = f"https://pixelplace.io/canvas/{ID_PAINTING}.png"  # Replace with your image URL
			response = requests.get(canvas_image_url)
			canvas_image = Image.open(BytesIO(response.content))
			frame_image = Image.open(frames[ID_FRAME])
			gem_image = Image.open(gems[ID_GEMS])
			frame_image.alpha_composite(canvas_image,(18,18))
			frame_image.alpha_composite(gem_image,(6,6))
			frame_image.save(img_bytes := BytesIO(),format="PNG")
			finalImageUrl = upload_from_file(img_bytes.getvalue())['data']["proxy_url"]
			embed = {"description": "","title": f"New Bid on Auction #{ED_AUCTION_ID}", "thumbnail":{"url":finalImageUrl,"height": 136,"width": 136},
			 "fields" : [
				{"name" : "Auction Owner", "value" :ED_AUCTION_OWNER_NAME}, {"name" : "Current Bid", "value" : f"{ED_AUCTION_BID_NAME} | {ED_AUCTION_BID_PRICE}"}, {"name" : "Amount of Bids", "value" : ED_AUCTION_BIDS}, {"name" : "Ends", "value" : f"<t:{ED_AUCTION_EXPIRES}:R>"}], "color": 15158332, } #yellow
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Auction Logs)","embeds": [embed],}
			postWebhook(WH_AUCTION_URL,whdata)
			
		# @socketConnection.on("auction.notification.win")
		# @background
		# def logAuctionDone(data):
		# 	data = {"id":96,"owner_id":121932,"owner_username":"HappyKlw","under_auction":0,"painting_id":81818,"author_id":7557,"author_username":"CaptainWinky","author_icons":"1-year,nitro,bread,art-dealer-3,gifter,vip","frame_id":3,"gems_id":2,"current_bid":450,"current_bid_user_id":121932,"current_bid_username":"HappyKlw","auction_expire_time":0,"bids":3,"sp":3,"bg":5,"burned":0,"created_at":1696784347}
		
def upload_from_file(file):
	api_url = "https://discord-storage.animemoe.us/api/upload-from-file/"	
	response = requests.request("POST", api_url, files={"file": file})
	return {"status": response.status_code, "data": response.json()}

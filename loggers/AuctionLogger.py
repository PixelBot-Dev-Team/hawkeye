import base64
from lib.util import background,getTimeStamp,postWebhook,getProfileData
import requests
from PIL import Image
from io import BytesIO

class AuctionDataModel():
	def __init__(self,bidData) -> None:
		self.AUCTION_ID           = bidData["id"]
		self.AUCTION_EXPIRES      = bidData["auction_expire_time"]
		self.AUCTION_OWNER_NAME   = bidData["author_username"]
		self.AUCTION_BIDS         = bidData["bids"]
		self.AUCTION_BID_PRICE    = bidData["current_bid"]
		self.AUCTION_BID_NAME     = bidData["current_bid_username"]
		self.FRAME_ID                = bidData["frame_id"]
		self.GEMS_ID                 = bidData["gems_id"]
		self.PAINTING_ID             = bidData["painting_id"]

class AuctionLogger:
	def __init__(self, master_connection, WH_AUCTION_URL:str) -> None:
		socketConnection = master_connection
		self.auctionImageCache:dict = dict()

		@socketConnection.on("auction.new.bid")
		@background
		def logNewAuctionBid(bidData):
			# Set data 
			auctionBid = AuctionDataModel(bidData)
			# Create image
			auctionImageURL = self.getAuctionURL()
			BADGES_OWNER, _, USERNAME_EXTRA_OWNER, GUILD_OWNER, GUILD_TITLE_OWNER, GUILD_DIVIDER_OWNER = getProfileData(auctionBid.AUCTION_OWNER_NAME)	
			BADGES_BID, _, USERNAME_EXTRA_BID, GUILD_BID, GUILD_TITLE_BID, GUILD_DIVIDER_BID = getProfileData(auctionBid.AUCTION_BID_NAME)	
			embed = {
				"title": f"New Bid on Auction #{auctionBid.AUCTION_ID}", 
				"description": "",
				"thumbnail":{"url":auctionImageURL,"height": 136,"width": 136},
			 "fields" : [
				{"name" : "Auction Owner", "value" :f"{auctionBid.AUCTION_OWNER_NAME}{BADGES_OWNER}{USERNAME_EXTRA_OWNER}{GUILD_DIVIDER_OWNER}{GUILD_OWNER}{GUILD_DIVIDER_OWNER}{GUILD_TITLE_OWNER}"}, 
				{"name" : "Current Bid", "value" : f"{auctionBid.AUCTION_BID_NAME}{BADGES_BID}{USERNAME_EXTRA_BID}{GUILD_DIVIDER_BID}{GUILD_BID}{GUILD_DIVIDER_BID}{GUILD_TITLE_BID} | {auctionBid.AUCTION_BID_PRICE} coins"}, 
				{"name" : "Amount of Bids", "value" : auctionBid.AUCTION_BIDS}, 
				{"name" : "Ends", "value" : f"<t:{auctionBid.AUCTION_EXPIRES}:R>"}
				]}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Auction Logs)","embeds": [embed],}
			postWebhook(WH_AUCTION_URL,whdata)
			
		@socketConnection.on("auction.notification.win")
		@background
		def logAuctionWin(auctionWinData):
			auctionWin = AuctionDataModel(auctionWinData)
			# create image
			auctionImageURL = self.getAuctionURL()
			BADGES_OWNER, _, USERNAME_EXTRA_OWNER, GUILD_OWNER, GUILD_TITLE_OWNER, GUILD_DIVIDER_OWNER = getProfileData(auctionWin.AUCTION_OWNER_NAME)	
			BADGES_BID, _, USERNAME_EXTRA_BID, GUILD_BID, GUILD_TITLE_BID, GUILD_DIVIDER_BID = getProfileData(auctionWin.AUCTION_BID_NAME)	
			embed = {
				"title": f"Auction #{auctionWin.AUCTION_ID} ended!", 
				"description": "",
				"thumbnail":{"url":auctionImageURL,"height": 136,"width": 136},
			 "fields" : [
				{"name" : "Auction Owner", "value" :f"{auctionWin.AUCTION_OWNER_NAME}{BADGES_OWNER}{USERNAME_EXTRA_OWNER}{GUILD_DIVIDER_OWNER}{GUILD_OWNER}{GUILD_DIVIDER_OWNER}{GUILD_TITLE_OWNER}"}, 
				{"name" : "Winning Bid", "value" : f"{auctionWin.AUCTION_BID_NAME}{BADGES_BID}{USERNAME_EXTRA_BID}{GUILD_DIVIDER_BID}{GUILD_BID}{GUILD_DIVIDER_BID}{GUILD_TITLE_BID} | {auctionWin.AUCTION_BID_PRICE} coins"}, 
				{"name" : "Amount of Bids", "value" : auctionWin.AUCTION_BIDS}, 
				]}
			whdata = {"content": f"Logged <t:{getTimeStamp()}:R>","username": "HawkEye (Auction Logs)","embeds": [embed],}
			postWebhook(WH_AUCTION_URL,whdata)
	
	def getAuctionURL(self,PAINTING_ID, FRAME_ID, GEMS_ID):
		frames = {
			1 : "./lib/assets/frames/copper-frame-bg.png",
			2 : "./lib/assets/frames/iron-frame-bg.png",
			3 : "./lib/assets/frames/pyrite-frame-bg.png",
		}
		gems = {
			1 : "./lib/assets/gems/emerald-frame-bg.png",
			2 : "./lib/assets/gems/sapphire-frame-bg.png",
			3 : "./lib/assets/gems/ruby-frame-bg.png",
		}
		try:
			return self.auctionImageCache[f"{PAINTING_ID}{FRAME_ID}{GEMS_ID}"]
		except KeyError:
			response = requests.get(f"https://pixelplace.io/canvas/{PAINTING_ID}.png")
			canvas_image = Image.open(BytesIO(response.content))
			frame_image = Image.open(frames[FRAME_ID])
			gem_image = Image.open(gems[GEMS_ID])
			frame_image.alpha_composite(canvas_image,(18,18))
			frame_image.alpha_composite(gem_image,(6,6))
			frame_image.save(img_bytes := BytesIO(),format="PNG")
			finalImageUrl = upload_to_dc(img_bytes.getvalue())['data']["proxy_url"]
			self.auctionImageCache[f"{PAINTING_ID}{FRAME_ID}{GEMS_ID}"] = finalImageUrl
			return finalImageUrl
		
def upload_to_dc(file):
	api_url = "https://discord-storage.animemoe.us/api/upload-from-file/"	
	response = requests.request("POST", api_url, files={"file": file})
	return {"status": response.status_code, "data": response.json()}
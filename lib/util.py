from threading import Thread
import requests
import time

def background(function):
	'''
	A threading decorator. \n
	use `@background` above the function you want to run in the background.
	'''
	def background(*arguments, **keywordArguments):
		Thread(target=function, args=arguments, kwargs=keywordArguments , daemon=True).start()
	return background

def postWebhook(WH_URL, WH_DATA) -> None:
	requests.post(WH_URL, json=WH_DATA)
	time.sleep(0.3)

def getTimeStamp() -> int:
	return int(str(time.time()).split(".")[0])

def getBadgeDict() -> dict[str, str]:
	return {
	"1-month":"<:L_1month:1161667276077027368>",
	"1-year":"<:L_1year:1161667277217873952>",
	"3-days":"<:L_3days:1161667279205978322>",
	"3-months":"<:L_3months:1161667281940643910>",
	"admin":"<:L_admin:1161667283471572993>",
	"art-dealer-1":"<:L_artdealer1:1161667285522595980>",
	"art-dealer-2":"<:L_artdealer2:1161667287594577940>",
	"art-dealer-3":"<:L_artdealer3:1161667290534776864>",
	"booster":"<:L_booster:1161667459942715393>",
	"partner":"<:L_partner:1161667269609410571>",
	"painting-owner":"<:L_paintingowner:1161667267931672660>",
	"painting-moderator":"<:L_paintingmoderator:1161667304959000697>",
	"nitro":"<:L_nitro:1161667467182088212>",
	"moderator":"<:L_moderator:1161667464812302366>",
	"gifter":"<:L_gifter:1161667299397357660>",
	"former-global-moderator":"<:L_formerglobalmoderator:1161667296746553474>",
	"chat-moderator":"<:L_chatmoderator:1161667463302348910>",
	"bread":"<:L_bread:1161667293118472302>",
	"snowball":"<:L_snowball:1161667271983378563>",
	"vip":"<:L_vip:1161667274743226519>",
	"":""
	}
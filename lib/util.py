from threading import Thread
import requests
import time

def background(function):
	'''
	A threading decorator. \n
	use `@background` above the function you want to run in the background.
	'''
	def backgroundFunction(*arguments, **keywordArguments):
		Thread(target=function, args=arguments, kwargs=keywordArguments , daemon=True).start()
	return backgroundFunction

def getTimeStamp() -> int:
	"Gets current time as int"
	return int(str(time.time()).split(".")[0])

def getProfileData(username):
	profileData = requests.get(f"https://pixelplace.io/api/get-user.php?username={username}").json()
	PFP_CANVAS_ID:int = profileData["canvas"]
	badges = str(profileData["othersIcons"]).split(",")
	badges.append(profileData["premiumIcon"])
	if profileData["vip"]:
		badges.append("vip")
	BADGES:str = ''.join([getBadgeDict()[badge] for badge in badges])
	GOLDEN_PROFILE:bool = bool(profileData["golden"])
	IS_RAINBOW_NAME:bool = bool(getTimeStamp() < profileData["rainbowTime"])
	IS_XMAS_NAME:bool = bool(getTimeStamp() < profileData["xmasTime"])
	IS_HALLOWEEN_NAME:bool = bool(getTimeStamp() < profileData["halloweenTime"])
	# Add stuff for golden profiles, rainbow/halloween/xmas names
	USERNAME_EXTRA:str = "🟨" if GOLDEN_PROFILE else ""
	USERNAME_EXTRA = f"{USERNAME_EXTRA}🌈" if IS_RAINBOW_NAME else USERNAME_EXTRA
	USERNAME_EXTRA = f"{USERNAME_EXTRA}🎄" if IS_XMAS_NAME else USERNAME_EXTRA
	USERNAME_EXTRA = f"{USERNAME_EXTRA}🎃" if IS_HALLOWEEN_NAME else f"{USERNAME_EXTRA}"
	USERNAME_EXTRA = f"({USERNAME_EXTRA})" if USERNAME_EXTRA != "" else USERNAME_EXTRA
	
	print(f"For debug: {profileData['guild']}")
	try:
		GUILD = profileData["guild"]
		GUILD_RANK:int = int(profileData["guild_rank"])
		GUILD_TITLES:dict = {1:profileData["guild_rank_1_title"],2:profileData["guild_rank_2_title"],3:profileData["guild_rank_3_title"]}
		GUILD_TITLE:str = GUILD_TITLES[GUILD_RANK]
		GUILD_DIVIDER:str = " - "
	except KeyError:
		GUILD = ""
		GUILD_DIVIDER:str = ""
		GUILD_RANK:str = ""
		GUILD_TITLE:str = ""
	return BADGES, PFP_CANVAS_ID, USERNAME_EXTRA, GUILD, GUILD_TITLE, GUILD_DIVIDER

def postWebhook(WH_URL, WH_DATA) -> None:
	requests.post(WH_URL, json=WH_DATA)
	time.sleep(0.3)

def getBadgeDict() -> dict[str, str]:
	return {
	"1-month":"<:L_1month:1161667276077027368>",
	"1-year":"<:L_1year:1161667277217873952>",
	"3-days":"<:L_3days:1161667279205978322>",
	"3-months":"<:L_3months:1161667281940643910>",
	"1-month-old":"<:L_1month:1161667276077027368>",
	"1-year-old":"<:L_1year:1161667277217873952>",
	"3-days-old":"<:L_3days:1161667279205978322>",
	"3-months-old":"<:L_3months:1161667281940643910>",
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
	"":"",
	"null":"",
	"None":"",
}

def getItemDict():
	return {
	1:["Pixel Missile",".png"],
	2:["Pixel Bomb",".png"],
	3:["Atomic Bomb",".png"],
	4:["Premium (1 Month)",".png"],
	5:["Premium (1 Year)",".png"],
	6:["Rainbow Username",".gif"],
	7:["Guild Bomb",".png"],
	8:["Avatar Bomb",".png"],
	9:["Name Change",".png"],
	10:["XMAS Username",".gif"],
	11:["Premium (3 Days)",".png"],
	12:["HALLOWEEN Username",".gif"],
	13:["Treasure Chest",".png"],
	}

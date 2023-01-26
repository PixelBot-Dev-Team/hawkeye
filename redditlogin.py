import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
import functools
import time
import json

def reddit_login(username, password):
	"""Retrieves a reddit session cookie, to be used for future requests
	Args:
		username (string): Username of reddit account
		password (string): Password of reddit account

	Returns:
		string: Reddit session cookie
	"""
	url = f"https://old.reddit.com/api/login/{username}"

	payload=f'op=login-main&user={username}&passwd={password}&rem=on&api_type=json'
	headers = {
	'DNT': '1',
	'host': 'old.reddit.com',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	}

	response = requests.request("POST", url, headers=headers, data=payload)


	try:
		cookies = response.cookies.get_dict()
	except Exception as e:
		print("❌ Error: Could not get reddit session cookie")
	else:
		print("✅ Reddit session cookie recieved")
		return cookies["reddit_session"]

def ask_pp_for_state():
	"""Asks Pixelplace for a state value, then uses that value to proceed to the login page
	This is mostly unnecesary but I will leave it in for now
	"""
	url = "https://pixelplace.io/api/sso.php?type=2&action=login"

	payload={}
	headers = {
	'DNT': '1',
	'host': 'pixelplace.io',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-User': '?1',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'Upgrade-Insecure-Requests': '1',
	'Cookie': 'authId=ucftr1a807rivbamfi5o39401b62beoollr306g40lkmlk6kgg443qt3pne8kkt5'
	}


	response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

	try:
		parsed_url = urlparse(response.headers['Location'])
		captured_value = parse_qs(parsed_url.query)['state'][0]
	except Exception as e:
		print("❌ Error: Could not get state value from Pixelplace")
	else:
		print("✅ State value recieved from Pixelplace")
		return captured_value

def get_modhash(session_cookie):
	"""Gets the modhash value from the reddit session cookie
	Args:
		session_cookie (string): Reddit session cookie
	Returns:
		string: Modhash value
	"""
	url = "https://old.reddit.com/api/me.json"

	payload={}
	headers = {
	'DNT': '1',
	'host': 'old.reddit.com',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',

	'Origin': 'reddit.com',
	'Cookie': f'reddit_session={session_cookie};'
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	try:

		modhash = json.loads(response.text)['data']['modhash']
	except Exception as e:
		print("❌ Error: Could not get modhash value")
	else:
		print("✅ Modhash value recieved")
		return modhash


def reddit_code(reddit_session, modhash, state="iloveowmincelmao"):
	"""Approves PixelPlace's request to access our account, then returns the code
	Args:
		reddit_session (string): Reddit session cookie (retrieved using reddit_login)
		state (string): [OPTIONAL] State value from PixelPlace. If no value is provided, a default value is used

	Returns:
		string: Code value from Reddit
	"""
	url = "https://ssl.reddit.com/api/v1/authorize"

	payload=f'client_id=5QBfS3MRclJUGQ&redirect_uri=https%3A%2F%2Fpixelplace.io%2Fapi%2Fsso.php%3Ftype%3D2&scope=identity&state={state}&response_type=code&duration=temporary&uh={modhash}&authorize=Allow'
	headers = {
	'DNT': '1',
	'host': 'ssl.reddit.com',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-User': '?1',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'Upgrade-Insecure-Requests': '1',
	'Origin': 'reddit.com',
	'Cookie': f'reddit_session={reddit_session};'
	}

	if state == "iloveowmincelmao":
		print("⚠ Information: State value not provided. Defaulting to 'iloveowmincelmao'. This should be fine for most purposes.")

	response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

	try:
		parsed_url = urlparse(response.headers['Location'])
		captured_value = parse_qs(parsed_url.query)['code'][0]
	except Exception as e:
		print("❌ Error: Could not retrieve code.")
	else:
		print("✅ Code retrieved from Reddit.")
		return captured_value


def pp_login(code, state = "iloveowmincelmao"):
	"""Approves PixelPlace's request to access our account, then returns the code
	Args:
		code (string): Reddit code value (retrieved using reddit_code)
		state (string): WARNING! You MUST use the same state that you used in reddit_code()! State value from PixelPlace. If no value is provided, a default value is used
	Returns:
		authId (string): PixelPlace session cookies
		authKey (string): PixelPlace session cookies
		authToken (string): PixelPlace session cookies
	"""
	url = f"https://pixelplace.io/api/sso.php?type=2&state={state}&code={code}"

	payload={}
	headers = {
	'DNT': '1',
	'host': 'pixelplace.io',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
	'Sec-Fetch-Dest': 'document',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-Site': 'cross-site',
	'Sec-Fetch-User': '?1',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'Upgrade-Insecure-Requests': '1',
	}

	print("⏳ Logging in to PixelPlace...")

	response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)


	cookies = response.cookies.get_dict()

	try:
		authId = cookies["authId"]
		authKey = cookies["authKey"]
		authToken = cookies["authToken"]
	except Exception as e:
		print("❌ Error: Could not retrieve authId, authKey, or authToken. WARNING! You MUST use the same state that you used in reddit_code().")
	else:
		print("✅ Successfully retrieved authId, authKey, and authToken.")
		return authId, authKey, authToken


def timeit(func):
	"""Times how long a Fuction takes to execute
	Args:
		func (function): Takes function below @
	Returns:
		string: String with Time it took to execute
	"""
	@functools.wraps(func)
	def wrapper_timer(*args, **kwargs):
		tic = time.perf_counter()
		value = func(*args, **kwargs)
		toc = time.perf_counter()
		elapsed_time = toc - tic
		print(f"Elapsed time: {elapsed_time:0.4f} seconds")
		return value
	return wrapper_timer


@timeit
def login(redditusername, redditpassword):

	reddit_token = reddit_login(redditusername, redditpassword)

	time.sleep(1)

	modhash = get_modhash(reddit_token)

	time.sleep(1)

	code = reddit_code(reddit_token, modhash)

	time.sleep(1)

	authId, authKey, authToken = pp_login(code)

	return authId, authKey, authToken


if __name__ == '__main__':
	login()
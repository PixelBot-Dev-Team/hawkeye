#Imports 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import pathlib
import socketio
import platform
import sys
CurrentDir = pathlib.Path(__file__).parent.absolute()

class Bot():
    def __init__(self, username, password, canvas, premium=False):
        """[summary]
            Class handles connecting to pixelplace by logging in using a reddit account using selenium and socketio.
            Contains functions for sending a chat message, placing a pixel on the connected canvas and sending a command.
        Args:
            username ([str]):
            password ([str]):
            canvas ([int]): The canvas number the bot will connect to
            premium (bool, optional): [If the bot is a premium account or not]. Defaults to False.
        """
        #Assigning 💩
        self.username = username
        self.password = password
        self.authToken, self.authKey, self.authId = self.loginuser()
        self.socketconnection = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
        self.canvas = canvas
        self.premium = premium

        self.AttemptSocketAuth()
        print(f"{self.username} logged in")

        #Error 🖐ling 
        @self.socketconnection.on("throw.error")
        def Place_error(data):
            timestamp = time.ctime()
            if data == 0:
               print(f"{timestamp}[Error {data}] You need to login on pixelplace.io first. Create an account, it's free !")
               print(f"{timestamp}[Info] Attempting Socket Connection")
               self.AttemptSocketAuth()
            if data == 1:
                 print(f"{timestamp}[Error {data}] Your session expired, please refresh the page")
            if data == 2:
                 print(f"{timestamp}[Error {data}] You need to create a username first")
            if data == 3:
                 print(f"{timestamp}[Error {data}] Color not found")
            if data == 4:
                 print(f"{timestamp}[Error {data}] This color is only available to premium subscribers")
            if data == 5:
                 print(f"{timestamp}[Error {data}] Wrong coordinates")
            if data == 6:
                 print(f"{timestamp}[Error {data}] This canvas has been temporarily disabled because its owner used premium settings on it and his membership has expired. Please wait for the owner to renew his premium membership or to revert canvas settings to non premium ones")
            if data == 7:
                 print(f"{timestamp}[Error {data}] Your premium membership has expired and this canvas is using premium settings. To continue, please renew your membership or revert canvas settings back to non premium ones")
            if data == 8:
                 print(f"{timestamp}[Error {data}] Please wait until the end of your cooldown")
            if data == 9:
                 print(f"{timestamp}[Error {data}] This canvas is private, you can't draw on it")
            if data == 10:
                 print(f"{timestamp}[Error {data}] To be able to place pixels on this canvas, you have to request approval from the owner")
            if data == 11:
                 print(f"{timestamp}[Error {data}] You are placing pixels too fast, please slow down")
            if data == 12:
                 print(f"{timestamp}[Error {data}] This canvas is terminated")
            if data == 13:
                 print(f"{timestamp}[Error {data}] Error while getting canvas data")
            if data == 14:
                 print(f"{timestamp}[Error {data}] Error while getting canvas access data")
            if data == 15:
                 print(f"{timestamp}[Error {data}] You have too many instances of pixelplace.io opened, please close some windows")
            if data == 16:
                 print(f"{timestamp}[Error {data}] Too many users share your internet connection (are you  using a proxy ?)")
            if data == 17:
                 print(f"{timestamp}[Error {data}] Pixelplace.io has been disabled for your internet connection (are you  using a proxy ?)")
            if data == 18:
                 print(f"{timestamp}[Error {data}] Server is full, please try again later")
            if data == 19:
                 print(f"{timestamp}[Error {data}] Reloading...")
            if data == 20:
                 print(f"{timestamp}[Error {data}] Your account has been temporarily disabled for placing pixels and/or sending messages too fast, try again in 5 minute")
             
    #export auth 💾
    def get_auth(self,cookie):
        for x in cookie:
            if x["name"] == "authToken":
                authToken = x["value"]
            elif x["name"] == "authKey":
                authKey = x["value"]
            elif x["name"] == "authId":
                authId = x["value"]
            else:
                pass
        return authToken, authKey, authId

    #loggin in user with automation to get auth data
    def loginuser(self,):
        driver = ""
        if platform.system() == "Windows":
             driver_path = f"{CurrentDir}\\windows\\chromedriver.exe"
             driver = webdriver.Chrome(driver_path)  
        elif platform.system() == "Linux":
             driver = webdriver.Chrome()
        else:
             print('Unsupported operating system. (Supported: Windows, Linux)')
             time.sleep(3)
             sys.exit()
        driver.implicitly_wait(100)
        driver.get("https://pixelplace.io/")
        popupbutton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="modals"]/div[2]/a')))
        driver.execute_script("arguments[0].click();", popupbutton)

        menubutton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-buttons"]/a[1]')))
        menubutton.click()

        loginbutton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="modals"]/div[3]/div[1]/button[1]')))
        loginbutton.click()

        redditLink = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[4]/div[2]/div[1]/div/a[2]")))
        redditLink.click()    

        redditusernamefield = driver.find_element_by_name("username")
        redditpasswordfield = driver.find_element_by_name("password")
        redditloginbutton = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button')))
        redditusernamefield.send_keys(f"{self.username}")
        redditpasswordfield.send_keys(f"{self.password}")
        redditloginbutton.click()

        redditconfirmconnection = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/form/div/input[1]')))
        redditconfirmconnection.click()
        
        authinfo = self.get_auth(driver.get_cookies())
        driver.quit()
        return authinfo

    def send_Chat(self, text, mention, type, target, color):
        self.socketconnection.emit(event="chat.message", data={"text": str(text), "mention": str(mention), "type": str(type), "target": str(target), "color": int(color)})
     
    #Attempt to 🔗 via socketio
    def AttemptSocketAuth(self):
        self.socketconnection.connect("https://pixelplace.io/socket.io/", transports='websocket', namespaces=["/",])
        self.socketconnection.emit(event='init', data={"authKey":self.authKey,"authToken":self.authToken,"authId":self.authId,"boardId":self.canvas})
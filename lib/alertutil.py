import sqlite3
from typing import Literal

from lib.util import getTimeStamp

# Function to create the database
def create_database():
    conn,cursor = getCandC()

    # pendingRedemptions table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS pendingRedemptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            duration INTEGER
        )
    """)

    # join alerts table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS joinAlerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            username TEXT,
            validUntil INTEGER,
            discordId TEXT
        )
    """)
    
    # leave alerts table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS leaveAlerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            username TEXT,
            validUntil INTEGER,
            discordId TEXT
        )
    """)
    
    # Custom word alerts table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS customWordAlerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            messageText TEXT,
            validUntil INTEGER,
            discordId TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def add_to_pending_redemptions(username,duration):
    conn,cursor = getCandC()

    remove_from_pending_redemptions(username)

    cursor.execute("""--sql
        INSERT INTO pendingRedemptions (username, duration)
        VALUES (?, ?)
    """, (username, duration,))

    conn.commit()
    conn.close()

def remove_from_pending_redemptions(username):
    conn,cursor = getCandC()
    
    cursor.execute("""--sql
        -- # TODO | remove all entries from pendingRedemptions where username is username
    """)

def get_pending_redemptions(username):
    conn,cursor = getCandC()
    cursor.execute("""--sql
                   SELECT duration FROM pendingRedemptions WHERE username = ?
                   """, (username,))
    data = cursor.fetchone()
    return data if data is None else data[0] 

def add_join_alert(joiningUsername,duration,discordId):
    conn,cursor = getCandC()

    timestamp = getTimeStamp()

    cursor.execute("""--sql
        INSERT INTO joinAlerts (timestamp, username, validUntil, discordId)
        VALUES (?, ?, ?, ?)
    """, (timestamp, joiningUsername, duration + timestamp, discordId))

    conn.commit()
    conn.close()
    
def get_active_join_alerts(username):
    return "List of discordIds"
    
def add_leave_alert(leavingUsername,duration,discordId):
    conn,cursor = getCandC()

    timestamp = getTimeStamp()

    cursor.execute("""--sql
        INSERT INTO leaveAlerts (timestamp, username, validUntil, discordId)
        VALUES (?, ?, ?, ?)
    """, (timestamp, leavingUsername, duration + timestamp, discordId))

    conn.commit()
    conn.close()
    
def get_active_leave_alerts(username) -> Literal['List of discordIds']:
    return "List of discordIds"
    
def add_customMessage_alert(text,duration,discordId):
    conn,cursor = getCandC()

    timestamp = getTimeStamp()

    cursor.execute("""--sql
        INSERT INTO customWordAlerts (timestamp, messageText, validUntil, discordId)
        VALUES (?, ?, ?)
    """, (timestamp, text, duration + timestamp, discordId))

    conn.commit()
    conn.close()

def get_active_custom_word_alerts():
    return "list of customText,discordId"

def getCandC():
    conn = sqlite3.connect('data/hawkeye_alerts.db')
    cursor = conn.cursor()
    return conn,cursor
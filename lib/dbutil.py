import sqlite3

# Function to create the database
def create_database():
    conn,cursor = getCandC()

    # UserStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS UserStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            userCount INTEGER,
            connectionCount INTEGER,
            userToConnectionAverage REAL
        )
    """)

    # connectionStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS connectionStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            connectionType INTEGER,
            username TEXT
        )
    """)

    # coinIslandRewardStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS coinIslandRewardStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            coinIslandID INTEGER,
            coinsGained INTEGER
        )
    """)

    # warStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS warStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            warType INTEGER,
            participants INTEGER,
            totalPx INTEGER,
            pointReward INTEGER
        )
    """)

    # itemStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS itemStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            bombType INTEGER,
            position TEXT,
            username TEXT
        )
    """)

    # muteStats table
    cursor.execute("""--sql
        CREATE TABLE IF NOT EXISTS muteStats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            username TEXT
        )
    """)

    conn.commit()
    conn.close()

# Function to add entry to the UserStats table
def add_user_stats(timestamp, user_count, connection_count, user_to_connection_average):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO UserStats (timestamp, userCount, connectionCount, userToConnectionAverage)
        VALUES (?, ?, ?, ?)
    """, (timestamp, user_count, connection_count, user_to_connection_average))

    conn.commit()
    conn.close()

# Function to add entry to the connectionStats table
def add_connection_stats(timestamp, connection_type, username):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO connectionStats (timestamp, connectionType, username)
        VALUES (?, ?, ?)
    """, (timestamp, connection_type, username))

    conn.commit()
    conn.close()

# Function to add entry to the coinIslandRewardStats table
def add_coin_island_reward_stats(timestamp, coin_island_id, coins_gained):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO coinIslandRewardStats (timestamp, coinIslandID, coinsGained)
        VALUES (?, ?, ?)
    """, (timestamp, coin_island_id, coins_gained))

    conn.commit()
    conn.close()

# Function to add entry to the warStats table
def add_war_stats(timestamp, war_type, participants, total_px, point_reward):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO warStats (timestamp, warType, participants, totalPx, pointReward)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, war_type, participants, total_px, point_reward))

    conn.commit()
    conn.close()

# Function to add entry to the itemStats table
def add_item_stats(timestamp, bomb_type, position, username):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO itemStats (timestamp, bombType, position, username)
        VALUES (?, ?, ?, ?)
    """, (timestamp, bomb_type, position, username))

    conn.commit()
    conn.close()

# Function to add entry to the muteStats table
def add_mute_stats(timestamp, username):
    conn,cursor = getCandC()

    cursor.execute("""--sql
        INSERT INTO muteStats (timestamp, username)
        VALUES (?, ?)
    """, (timestamp, username))

    conn.commit()
    conn.close()
    
def getCandC():
    conn = sqlite3.connect('./data/hawkeye_stats.db')
    cursor = conn.cursor()
    return conn,cursor
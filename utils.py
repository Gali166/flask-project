from discord_webhook import DiscordWebhook
import sqlite3
from datetime import datetime, timedelta

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1439950695951368192/eKQtIlxW4VPDuQu3k2mcbutze37UAP91uObWGQCAAppV5uzPLGqV4TH1W6LRsfkLU1dh"

def send_to_discord(text):
    webook= DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=text)
    webook.execute()

def get_db_connection():
    return sqlite3.connect("messages.db")

def setup_db():
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY,
        message TEXT,
        date TEXT
     )
     ''')

    conn.commit()
    conn.close()

def save_on_db(text):
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute('''
    INSERT INTO messages (message, date)
    VALUES (?,?)
    ''', (text,date))

    conn.commit()
    conn.close()

def get_messages_from_db():
    cutoff_time=datetime.now() - timedelta(minutes=30)
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute('''
    SELECT message, date FROM messages
    WHERE date > ?
    ''', (cutoff_time,))  #מה שקרה בחצי שעה האחרונה

    messages= cursor.fetchall()
    conn.close()

    return messages

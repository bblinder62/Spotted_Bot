import os
from typing import Final
from discord import Intents, Client, Message
from dotenv import load_dotenv
from responses import get_response
import sqlite3

PRIVATE_MESSAGE_PREFIX="?dm"

SECRET_MESSAGE_PREFIX="?sB"


#Step 0: LOad Our Token From Somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")



# Step 1: BOT SETUP

intents: Intents=Intents.default()
intents.message_content=True 
client: Client = Client(intents=intents)

#Step 2: MEssage Functionality
async def send_message(username, message: Message, user_message: str) -> None:
    if not user_message and message.attachments==None:
        print("Message was empty because intents were not enabled properly probably- Ben")
        return
    if is_private := user_message[0:3]==PRIVATE_MESSAGE_PREFIX: #THis checks for if a message is private, sets that bool to is_Private if it is
        user_message=user_message[4:]
    
    elif is_private := user_message[0:3] == SECRET_MESSAGE_PREFIX:
        user_message=user_message[4:]

    elif "spotted" in message.channel.name.lower() and not message.attachments == None:
        spotted(username, user_message.strip("|"))
        return



    try:
        response: str = get_response(user_message, message.author)
        

        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)


#functions:

# Function to create the 'users' table
def create_table():
    with sqlite3.connect('spotted.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            spotted INTEGER,
            spotter INTEGER
        )
        ''')
        print("Table created or already exists.")

# Function to insert a row into the 'users' table
def insert_row(name, spotted, spotter):
    with sqlite3.connect('spotted.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, spotted, spotter)
        VALUES (?, ?, ?)
        ''', (name, spotter, spotted))
        print("Row inserted successfully.")
        conn.commit()

# Function to fetch a single row from the 'users' table
def fetch_row(name):
    with sqlite3.connect('spotted.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE name = ?
        ''', (name,))
        row = cursor.fetchone()
        
        if row:
            return row
        else:
            print("No row found.")
            return None
        

# Function to delete a row from the 'users' table
def delete_row(conn, user_id):
    with sqlite3.connect('spotted.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM users WHERE id = ?
        ''', (user_id,))
        print("Row deleted successfully.")
        conn.commit()

def spotted(spotter,spotted):
    print(spotter,spotted) 
    print("Processing Spotted User")
    row=fetch_row(spotted)
    if row==None:
        insert_row(spotted,1,0)
    else:
        print(row)
        # delete_row()
        # insert_row()

    print("Processing Spotter")
    row=fetch_row(spotter)
    if row==None:
        insert_row(spotter,0,1)
    else:
        print(row[0],row[1])
        # delete_row()
        # insert_row()


#Step 3: Handling the Startup for our bot

@client.event
async def on_ready():
    print(f'{client.user} is now running, V0.2')
    create_table()


#Step 4 handling incoming messages
@client.event
async def on_message(message: Message):
    if message.author == client.user: #Translation: If bot sends a message
        return 
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel} {username}: "{user_message}"]')
    await send_message(username,message,user_message)


#STEP 5 Main entry point 
def main() -> None:
    client.run(token=TOKEN)
    #TODO Enter a function here that backs up the table every time it closes, and then after 5 backups, starts deleting the oldest ones.


if __name__ == '__main__':
    main()



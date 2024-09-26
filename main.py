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

conn = sqlite3.connect('spotted.db') #connect to SQLite


# Step 1: BOT SETUP

intents: Intents=Intents.default()
intents.message_content=True 
client: Client = Client(intents=intents)

#Step 2: MEssage Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message and message.attachments==None:
        print("Message was empty because intents were not enabled properly probably- Ben")
        return
    if is_private := user_message[0:3]==PRIVATE_MESSAGE_PREFIX: #THis checks for if a message is private, sets that bool to is_Private if it is
        user_message=user_message[4:]
    
    elif is_private := user_message[0:3] == SECRET_MESSAGE_PREFIX:
        user_message=user_message[4:]

    elif "spotted" in message.channel.name.lower() and not message.attachments == None:
        spotted(message.author, user_message.strip("|"))
        create_table(conn)



    try:
        response: str = get_response(user_message, message.author)
        

        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)


#functions:

# Function to create the 'users' table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
    ''')
    print("Table created or already exists.")

# Function to insert a row into the 'users' table
def insert_row(conn, name, age, email):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (name, age, email)
    VALUES (?, ?, ?)
    ''', (name, age, email))
    print("Row inserted successfully.")
    conn.commit()

# Function to fetch a single row from the 'users' table
def fetch_row(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    
    if row:
        print(f"Fetched User -> ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Email: {row[3]}")
    else:
        print("No row found.")
    return row

# Function to delete a row from the 'users' table
def delete_row(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users WHERE id = ?
    ''', (user_id,))
    print("Row deleted successfully.")
    conn.commit()

# Function to close the database connection
def close_db(conn):
    conn.close()
    print("Connection closed.")

# # Main script to run all functions
# if __name__ == "__main__":
#     # Connect to the database
#     conn = connect_db()

#     # Step 1: Create the table
#     create_table(conn)

#     # Step 2: Insert a row
#     insert_row(conn, "John Doe", 30, "johndoe@example.com")

#     # Step 3: Fetch the row
#     fetch_row(conn, 1)

#     # Step 4: Delete the row
#     delete_row(conn, 1)

#     # Close the connection
#     close_db(conn)

def spotted(spotter,spotee):
    print(spotter,spotee) 


#Step 3: Handling the Startup for our bot

@client.event
async def on_ready():
    print(f'{client.user} is now running')

#Step 4 handling incoming messages
@client.event
async def on_message(message: Message):
    if message.author == client.user: #Translation: If bot sends a message
        return 
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel} {username}: "{user_message}"]')
    await send_message(message,user_message)


#STEP 5 Main entry point 
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()



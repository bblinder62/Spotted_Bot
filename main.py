import os
from typing import Final
from discord import Intents, Client, Message
from dotenv import load_dotenv
from responses import get_response

PRIVATE_MESSAGE_PREFIX="?S"

#Step 0: LOad Our Token From Somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Step 1: BOT SETUP

intents: Intents=Intents.default()
intents.message_content=True 
client: Client = Client(intents=intents)

#Step 2: MEssage Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty because intents were not enabled properly probably- Ben")
        return
    if is_private := user_message[0]==PRIVATE_MESSAGE_PREFIX: #THis checks for if a message is private, sets that bool to is_Private if it is
        user_message=user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


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



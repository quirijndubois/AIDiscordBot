import discord
from discord.utils import get
from bardapi import Bard
import io
import os
import asyncio

BardToken = ""
BotToken = ""

intents = discord.Intents.default()
intents.message_content = True
audioToggle = True


bard = Bard(token=BardToken)

client = discord.Client(intents=intents)

def save_audio(audio_data, filename):
    with io.open(filename, "wb") as f:
        f.write(audio_data)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("ai"):

        if message.content.lower().startswith("ai tekst "):
            audioToggle = False
            content = message.content[9:]
        else:
            content = message.content[2:]
            audioToggle = True

        ans = bard.get_answer(f"{message.author.display_name} stelt je de volgende vraag: {content}")['content']

        if not audioToggle:
            await message.channel.send(ans)
        
        if audioToggle:
            audio = bard.speech(ans)
            save_audio(audio,"antwoord.wav")

            channel = message.author.voice.channel
            voice = await channel.connect()
            player = discord.FFmpegPCMAudio('antwoord.wav')
            voice.play(player)

            while voice.is_playing():
                await asyncio.sleep(1)

            await voice.disconnect()


client.run(BotToken)

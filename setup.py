from turtle import delay
from click import pass_context
import discord
from discord.ext import commands
import time
import json
import random
import glob
import youtube_dl
import os
import asyncio
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import gtts
from gtts import gTTS
from dotenv import load_dotenv
from keep_alive import keep_alive

client = commands.Bot(command_prefix='.bob ')

players = {}

#--------------------------------------------------------------------------------------------------
# Commands help forum
@client.command()
async def help1(ctx):
    await ctx.send(">>>`**This is the official help forum!**`")
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# Commands for bot join and leave
@client.command(pass_context = True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send('I joined the voice channel')
    else:
        await ctx.send('You are not in a voice channel, you must be in a voice channel to run this command')

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I left the voice channel')
    else:
        await ctx.send('I am not in a voice channel')
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
# Commands for playing music
@client.command(pass_context = True)
async def play(ctx, url:str):
    voice = discord.utils.get(client.voice_clients)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    elif ctx.author.voice:
        voice = await channel.connect()
    else: 
        await ctx.send('You are not in a voice channel, you must be in a voice channel to run this command!')

    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors':[{
        'key': 'FFmpegExtractAudio',
        'preferredquality': '192',
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):    
        if file.endswith(".opus"):
            os.rename(file, "song.mp3")
        elif file.endswith(".m4a"):
            os.rename(file, "song.mp3")
        elif file.endswith(".webm"):
            os.rename(file, "song.mp3")
                
    source = FFmpegPCMAudio('song.mp3')
    player = voice.play(source)

    while voice.is_playing():
        await asyncio.sleep(1)
    else:
        await asyncio.sleep(5)
        while voice.is_playing():
            break
        else: os.remove('song.mp3')
        while voice.is_playing():
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(15)
            while voice.is_playing():
                break
            else:
                await voice.guild.voice_client.disconnect()

          
#-------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------
# Commands for memes sounds played in voice channel
@client.command(pass_context = True)
async def meme1(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    elif ctx.author.voice:
        voice = await channel.connect()
    else: 
        await ctx.send('You are not in a voice channel, you must be in a voice channel to run this command!')
 
    source = FFmpegPCMAudio('Meme1.mp3')
    player = voice.play(source)

    while voice.is_playing():
        await asyncio.sleep(1)
    else:
        await asyncio.sleep(5)
        while voice.is_playing():
            break
        else: 
            await voice.guild.voice_client.disconnect()

#-----------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------
# TTS
@client.command()
async def tts(ctx, *, text=None):    
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients) 

    if voice and voice.is_connected():
        await voice.move_to(channel)
    elif ctx.author.voice:
        voice = await channel.connect()
    else:
        await ctx.send('You are not in a voice channel, you must be in a voice channel to run this command!')

    tts = gTTS(text=text, lang='en', tld='ca', slow = False)
    tts.save('ttsvoice.mp3')
    source = FFmpegPCMAudio('ttsvoice.mp3')
    player = voice.play(source)

    while voice.is_playing():
        await asyncio.sleep(1)
    else:
        await asyncio.sleep(60)
        while voice.is_playing():
            break
        else:
            await ctx.guild.voice_client.disconnect()

    


# Guess the number game
@client.command()
async def guessgame(ctx):
    computer = random.randint(1, 10)
    await ctx.send('Guess my number between 1 and 10')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
    msg = await client.wait_for("message", check=check)

    if int(msg.content) == computer:
        await ctx.send('Correct!')
    else:  
        await ctx.send(f'You got it wrong, it was {computer}')


# Startup information
@client.event
async def on_ready():
    # Watching status
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='The Boys2'))
    # Playing status
    await client.change_presence(activity=discord.Game('PROTOTYPE'))
    # Listening status
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Bitch'))
    # Competing in
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='Cup Cake Tourney'))

    print('We have logged in as {0.user}'.format(client))

# Token for running the discord client
load_dotenv()
keep_alive()
client.run(os.getenv('TOKEN'))



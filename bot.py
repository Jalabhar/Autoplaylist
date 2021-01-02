import discord
import nest_asyncio
import random
import path_interface_func as PI
from discord.ext import commands
from flask import Flask
from threading import Thread
nest_asyncio.apply()
TOKEN = open('TOKEN.txt', 'r').readline()
client = discord.Client()

app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


bot = commands.Bot(command_prefix='!')


status = cycle(['Always Ready', 'Forever Ready'])


@bot.event
async def on_ready():
    change_status.start()
    print("Your bot is ready")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.command(name='Playlists', help='''Creates Playlists for Spotify using Tech Sorcery''')
async def on_message(ctx, *, message):
    input_info = message.split(',')
    Author = ctx.author
    clean_input = []
    for entry in input_info:
        entry = entry.lstrip()
        clean_input.append(entry)
    artist_1 = clean_input[0]
    artist_2 = clean_input[1]
    bool_var = False
    time = 12.0
    try:
        if clean_input[2] == 'True':
            bool_var = True
            try:
                time = float(clean_input[3])
            except IndexError:
                pass
        elif clean_input[2] == 'False':
            bool_var = False
            try:
                time = float(clean_input[3])
            except IndexError:
                pass
        else:
            time = float(clean_input[2])
            try:
                if clean_input[3] == 'True':
                    bool_var = True
                elif clean_input[3] == 'False':
                    bool_var = False
            except IndexError:
                pass
    except IndexError:
        pass
    available_response = (Author.mention + ', Building Playlists: ' +
                          str(artist_1) + ' to ' + str(artist_2))
    await ctx.send(available_response)
    try:
        await bot.change_presence(activity=discord.Game(name="Playlist Builder"))
        playlists = PI.build_path(artist_1, artist_2, User=Author.display_name,
                                  running_time=time, cycle=bool_var)
        task_done_response = Author.mention + ', your Playlists are complete: '
        for playlist in playlists:
            playlist = 'http://open.spotify.com/playlist/' + playlist
            task_done_response += ('\n' + playlist)
        await bot.change_presence(activity=discord.Game(name="Always Ready"))
    except:
        task_done_response = Author.mention + ', your request: ' + \
            str(artist_1) + ' to ' + str(artist_2) + ' failed. Try again.'
    await ctx.send(task_done_response)
bot.run(TOKEN)

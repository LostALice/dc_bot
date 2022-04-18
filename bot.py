#Code by Aki.no.Alice@Tyrant_Rex

import re,discord,os,asyncio,requests

from pytube import YouTube,Playlist,Search
from discord.ext import commands
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from os import getenv

client = commands.Bot(command_prefix="~",activity=discord.Game(name="HONG KONG DIPLOMA OF SECONDARY EDUCATION EXAMINATION 2022"))
song_list = {}
    # song_list

    # Returns:
    #     {
    #         "guild_id":["song_list"],
    #         "guild_id":["song_list"],
    # }

play_list = {}
    # play_list

    # Returns:
    #     {
    #         "guild_id":["play_list"],
    #         "guild_id":["play_list"],
    # }

channel_opts = {}
    # channel_opts

    # Returns:
    #     {
    #         "guild_id":{
    #             "loop":     False,
    #             "random":   False,
    #         },
    #         "guild_id":{
    #             "loop":     False,
    #             "random":   False,
    #         },
    # }

if not os.path.exists("./mp3"):
    os.mkdir("./mp3")

#change file name function
def change_txt(txt):
    ch_txt = r"[\/\\\:\*\?\"\<\>\|\#]"
    return re.sub(ch_txt,"",txt)

#loop function
def loop_function(guild_id):
    global channel_opts

    if channel_opts.get(guild_id) == None:
        channel_opts[guild_id] = {
            "loop":     False,
            "random":   False
        }

#return youtube results function
def to_url(str_):
    if "list=" in str_:
        _ =  len(Playlist(str_))
        if _ == 0:
            return [YouTube(str_).watch_url]
        elif _ >= 50:
            return list(Playlist(str_))[:50]
        else:
            return list(Playlist(str_))
    else:
        try:
            return [YouTube(str_).watch_url]
        except:
            return [Search(str_).results[0].watch_url]

#return youtube list function
def to_playlist(list_):
    p = []
    for i in list_:
        yt = YouTube(i)
        p.append(yt.title)
    return p

#loop song function
async def loop_song(ctx,vc,guild_id):
    global song_list,play_list

    while channel_opts[guild_id]["loop"]:
        for song in song_list[guild_id]:
            while vc.is_playing():
                if not vc.is_playing():
                    break
            yt = YouTube(song)
            title = change_txt(yt.title)

            if yt.length > 1800:
                await ctx.channel.send(f"The duration of the song is too long\nTitle-> {title}\nDuration-> {int(yt.length/3600)}:{int(yt.length/60)%60}:{int(yt.length%60)}", delete_after=10)
                return

            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": f"./mp3/{title}.mp3"
            }

            if not os.path.exists(f"./mp3/{title}.mp3"):
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song])

            embed = discord.Embed(title=f"Now playing:{yt.title} \nBy {ctx.author}", url=song,color=discord.Color.from_rgb(241, 196, 15))
            if not vc.is_playing():
                print(f"\n{ctx.author} -> {ctx.message.guild} -> {ctx.author.voice.channel}:{title}",flush=True)
                if channel_opts[guild_id]["loop"]:
                    await ctx.channel.send(embed = embed, delete_after=yt.length-1)
                    vc.play(discord.FFmpegPCMAudio(ydl_opts["outtmpl"]))
                else:
                    await ctx.channel.send(embed = embed, delete_after=yt.length-1)
                    vc.play(discord.FFmpegPCMAudio(ydl_opts["outtmpl"]),after=lambda x=None:
                        asyncio.run_coroutine_threadsafe(play_song(ctx,vc,guild_id),client.loop))

                    song_list[guild_id].pop(0)
                    play_list[guild_id].pop(0)

#play song function
async def play_song(ctx,vc,guild_id):
    global song_list,play_list
    while vc.is_playing():
        if not vc.is_playing():
            break

    if song_list[guild_id] != []:
        url = song_list[guild_id][0]

        yt = YouTube(url)
        title = change_txt(yt.title)

        if yt.length > 1800:
            await ctx.channel.send(f"The duration of the song is too long\nTitle-> {title}\nDuration-> {int(yt.length/3600)}:{int(yt.length/60)%60}:{int(yt.length%60)}", delete_after=10)
            return

        ydl_opts = {
            "format": "bestaudio",
            "outtmpl": f"./mp3/{title}.mp3"
        }

        if not os.path.exists(f"./mp3/{title}.mp3"):
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        embed = discord.Embed(title=f"Now playing:{yt.title} \nBy {ctx.author}", url=url,color=discord.Color.from_rgb(180, 97, 234))
        if not vc.is_playing():
            print(f"\n{ctx.author} -> {ctx.message.guild} -> {ctx.author.voice.channel}:{title}",flush=True)

            if channel_opts[guild_id]["loop"]:
                await ctx.channel.send(embed = embed, delete_after=yt.length-1)
                vc.play(discord.FFmpegPCMAudio(ydl_opts["outtmpl"]),after=lambda x=None:
                    asyncio.run_coroutine_threadsafe(loop_song(ctx,vc,guild_id),client.loop))

            else:
                await ctx.channel.send(embed = embed, delete_after=yt.length-1)
                vc.play(discord.FFmpegPCMAudio(ydl_opts["outtmpl"]),after=lambda x=None:
                    asyncio.run_coroutine_threadsafe(play_song(ctx,vc,guild_id),client.loop))

                song_list[guild_id].pop(0)
                play_list[guild_id].pop(0)
    else:
        await ctx.voice_client.disconnect()
        await ctx.channel.send("Bye Bye", delete_after=10)

#on ready
@client.event
async def on_ready():
    print("\nHey Mister!",flush=True)

#aki daze!
@client.command(help="""Aki daze!""")
async def aki(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(f"Ready DAZE My ping is {client.latency}!", delete_after=10)

#loop song
@client.command(aliases=["lp","l","L"],help="""loop song! [~lp,l]""")
async def loop(ctx):
    global channel_opts
    await ctx.channel.purge(limit=1)
    guild_id = ctx.message.guild.id

    loop_function(guild_id)
    if channel_opts[guild_id]["loop"]:
        channel_opts[guild_id]["loop"] = False
        await ctx.channel.send(f"Stop looping songs!", delete_after=5)
    else:
        channel_opts[guild_id]["loop"] = True
        await ctx.channel.send(f"Looping songs!", delete_after=5)

#show the playlist
@client.command(aliases=["pl","PL"],help="""List song list [~pl]""")
async def playlist(ctx):
    text = "```Play next:\n"
    guild_id = ctx.message.guild.id
    await ctx.channel.purge(limit=1)

    try:
        if  play_list[guild_id] == []:
            text += "None"
        else:
            for i in play_list[guild_id]:
                text += f"{play_list[guild_id].index(i)+1}.{i :>3}\n"
    except:
        text += "None"

    text += "```"
    await ctx.channel.send(text)

#clear songlist, playlist
@client.command(aliases=["clr","c","C"],help="""Clear song list [~clr,c]""")
async def clear(ctx):
    await ctx.channel.purge(limit=1)
    guild_id = ctx.message.guild.id
    if guild_id in song_list:
        song_list[guild_id] = []
        play_list[guild_id] = []
    vc = ctx.guild.voice_client
    vc.stop()
    await ctx.channel.send("Cleared", delete_after=5)

#remove songlist, playlist from index
@client.command(aliases=["rm","r","R"],help="""Remove a song in playlist {~rm index1} [~rm,r]""")
async def remove(ctx,index: int):
    global play_list,song_list
    await ctx.channel.purge(limit=1)

    guild_id = ctx.message.guild.id
    try:
        index = int(index)
        song_list[guild_id].pop(index-1)
        play_list[guild_id].pop(index-1)
    except:
        await ctx.channel.send("Please input a index in the playlist niinii :<", delete_after=30)
    await ctx.channel.send("Removed", delete_after=5)

#skip song
@client.command(aliases=["s","S"],help="""Skip this song [~s]""")
async def skip(ctx):
    global channel_opts
    await ctx.channel.purge(limit=1)

    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.stop()
        guild_id = ctx.message.guild.id
        if channel_opts[guild_id]["loop"]:
            loop_song(ctx,vc,guild_id)
        else:
            play_song(ctx,vc,guild_id)

        await ctx.channel.send("Skiped", delete_after=5)
    else:
        await ctx.channel.send("Oniichan I am not playing song :<", delete_after=10)

#quit channel
@client.command(aliases=["q","Q"],help="""Leave this channel [~q]""")
async def quit(ctx):
    global song_list,play_list
    await ctx.channel.purge(limit=1)

    guild_id = ctx.message.guild.id
    if guild_id in song_list:
        song_list[guild_id] = []
        play_list[guild_id] = []
    try:
        await ctx.voice_client.disconnect()
    except:
        await ctx.channel.send("Oniichan I am not in this voice channel", delete_after=10)

#daily nhentai
@client.command(help="""Show nhentai today popular doujinshi""")
async def nh(ctx):
    await ctx.channel.purge(limit=1)
    message = ""
    resp = requests.get("https://nhentai.net")
    soup = BeautifulSoup(resp.text, "lxml")
    page = soup.find_all(href=re.compile("/g/"))[:5]
    for p in page:
        url = p.get("href")
        code = url.replace("g", "").replace("/","")
        message += f"\n{code}\nhttps://nhentai.net{url}"

    await ctx.channel.send(f"Today popular are:{message}")

#swap order
@client.command(aliases=["sw","SW"],help="""Swap the index {~sw index1 index2} [~sw]""")
async def swap(ctx,*index_: int):
    global play_list,song_list
    await ctx.channel.purge(limit=1)
    guild_id = ctx.message.guild.id
    count = len(song_list[guild_id])

    if len(index_) != 2:
        await ctx.channel.send("Please input valid index niinii", delete_after=10)
        return
    elif index_[0] < 0 or index_[1] < 0:
        await ctx.channel.send("Please input valid index niinii", delete_after=10)
        return
    elif index_[0] > count or index_[1] > count:
        await ctx.channel.send("Please input valid index niinii", delete_after=10)
        return

    song_list[guild_id][index_[0]-1],song_list[guild_id][index_[1]-1] = song_list[guild_id][index_[1]-1],song_list[guild_id][index_[0]-1]
    play_list[guild_id][index_[0]-1],play_list[guild_id][index_[1]-1] = play_list[guild_id][index_[1]-1],play_list[guild_id][index_[0]-1]

    await ctx.channel.send("Swapped", delete_after=5)

#play next
@client.command(aliases=["pn","PN"],help="""Set a song play next {~pn index1} ["pn",]""")
async def playnext(ctx,*index_: int):
    global play_list,song_list
    await ctx.channel.purge(limit=1)
    guild_id = ctx.message.guild.id
    count = len(song_list[guild_id])

    if len(index_) != 1:
        await ctx.channel.send("Please input valid index niinii", delete_after=10)
        return
    try:
        index = int(index_[0])
    except TypeError:
        await ctx.channel.send("Please input valid index niinii", delete_after=10)
        return

    song_list[guild_id].insert(0, song_list[guild_id].pop(index-1))
    play_list[guild_id].insert(0, play_list[guild_id].pop(index-1))

    await ctx.channel.send(f"Next song will be {play_list[guild_id][0]}", delete_after=10)

#play song
@client.command(pass_context=True,aliases=["p","P"],help="""Play some songs [~p]""")
async def play(ctx,*url_: str):
    await ctx.channel.purge(limit=1)
    global song_list,play_list
    url = " "

    if "https://youtu.be" in url_[0]:
        url = url_[0]
    else:
        url = url.join(url_)

    guild_id = ctx.message.guild.id

    if not ctx.voice_client:
        if guild_id in song_list:
            song_list[guild_id] = []
            play_list[guild_id] = []

        ch = ctx.author.voice.channel
        await ch.connect()

    loop_function(guild_id)

    if guild_id in song_list:
        song_list[guild_id] += to_url(url)
        play_list[guild_id] += to_playlist(to_url(url))
    else:
        song_list[guild_id] = to_url(url)
        play_list[guild_id] = to_playlist(to_url(url))

    vc = ctx.guild.voice_client

    if not vc.is_playing():
        asyncio.run_coroutine_threadsafe(play_song(ctx,vc,guild_id),client.loop)
    else:
        await ctx.channel.send("Added to play list", delete_after=10)

if __name__ == "__main__":
    client.run(getenv("token"))

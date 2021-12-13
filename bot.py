#Code by Aki.no.Alice@Tyrant_Rex

import requests,re,discord,os,socket,struct,asyncio
from pytube import YouTube,Playlist,Search
from discord.ext import commands
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix="~")
song_list = {}
play_list = {}
loop_ = {}

if not os.path.exists("./mp3"):
    os.mkdir("./mp3")

#change file name function
def change_txt(txt):
    ch_txt = r"[\/\\\:\*\?\"\<\>\|\#]"
    return re.sub(ch_txt,"",txt)

#loop function
def loop_function(guild_id):
    global loop_
    if not guild_id in loop_:
        loop_[guild_id] = False

#return youtube results function
def to_url(str_):
    if "https://www.youtube.com/" in str_:
        if "list=" in str_ and "https://www.youtube.com/" in str_:
            if len(list(Playlist(str_))) <= 50:
                return list(Playlist(str_))
            else:
                return list(Playlist(str_))[:50]
        else:
            return [str_]
    else:
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

    while loop_[guild_id]:
        for song in song_list[guild_id]:
            while vc.is_playing():
                if not vc.is_playing():
                    break
            yt = YouTube(song)

            title = change_txt(yt.title)
            if not os.path.exists(f"./mp3/{title}.mp3"):
                s = yt.streams.filter(only_audio=True).first().download(output_path="./mp3/")

            embed = discord.Embed(title=f"Now playing:{yt.title}", url=song,color=discord.Color.from_rgb(241, 196, 15))
            if not vc.is_playing():
                print(f"{ctx.author}:{title}",flush=True)
                if loop_[guild_id]:
                    await ctx.channel.send(embed = embed, delete_after=10)
                    vc.play(discord.FFmpegPCMAudio(s))
                else:
                    await ctx.channel.send(embed = embed, delete_after=10)
                    vc.play(discord.FFmpegPCMAudio(s),after=lambda x=None:
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
        if not os.path.exists(f"./mp3/{title}.mp4"):
            s = yt.streams.filter(only_audio=True).first().download("./mp3/")
        else:
            s = f"./mp3/{title}.mp4"

        embed = discord.Embed(title=f"Now playing:{yt.title}", url=url,color=discord.Color.from_rgb(180, 97, 234))
        if not vc.is_playing():
            print(f"{ctx.author}:{title}",flush=True)
            if loop_[guild_id]:
                await ctx.channel.send(embed = embed, delete_after=10)
                vc.play(discord.FFmpegPCMAudio(s),after=lambda x=None:
                    asyncio.run_coroutine_threadsafe(loop_song(ctx,vc,guild_id),client.loop))

            else:
                await ctx.channel.send(embed = embed, delete_after=10)
                vc.play(discord.FFmpegPCMAudio(s),after=lambda x=None:
                    asyncio.run_coroutine_threadsafe(play_song(ctx,vc,guild_id),client.loop))

                song_list[guild_id].pop(0)
                play_list[guild_id].pop(0)
    else:
        await asyncio.sleep(60)
        await ctx.channel.send("Bye Bye", delete_after=5)
        await ctx.voice_client.disconnect()

#on ready
@client.event
async def on_ready():
    print("Hey Mister!",flush=True)

#aki daze!
@client.command(help="Aki daze!")
async def aki(ctx):
    await ctx.channel.send(f"Ready DAZE My ping is {client.latency}!", delete_after=5)

#Loop song
@client.command(aliases=["lp"],help="loop_ song! [~loop]")
async def loop(ctx):
    global loop_
    guild_id = ctx.message.guild.id
    loop_function(guild_id)
    if loop_[guild_id]:
        loop_[guild_id] = False
        await ctx.channel.send(f"Stop loop_ing songs!", delete_after=5)
    else:
        loop_[guild_id] = True
        await ctx.channel.send(f"loop_ing songs!", delete_after=5)

#Show the playlist
@client.command(aliases=["pl"],help="List song list [~playlist]")
async def playlist(ctx):
    text = "```Play next:\n"
    guild_id = ctx.message.guild.id

    try:
        if  play_list[guild_id] == []:
            text += "None"
        else:
            for i in play_list[guild_id]:
                text += f"{play_list[guild_id].index(i)+1}.{i :>3}\n"
    except:
        text += "None"

    text += "```"
    await ctx.channel.send(text, delete_after=10)

#clear songlist, playlist
@client.command(aliases=["clr"],help="Clear song list [~clr]")
async def clear(ctx):
    guild_id = ctx.message.guild.id
    if guild_id in song_list:
        song_list[guild_id] = []
        play_list[guild_id] = []
    vc = ctx.guild.voice_client
    vc.stop()
    await ctx.channel.send("Cleared", delete_after=5)

#remove songlist, playlist from index
@client.command(aliases=["rm"],help="Remove a song in playlist \{~rm (playlist index)\} [~rm]")
async def remove(ctx,index: int):
    global play_list,song_list

    guild_id = ctx.message.guild.id
    try:
        index = int(index)
        song_list[guild_id].pop(index-1)
        play_list[guild_id].pop(index-1)
    except:
        await ctx.channel.send("please input a index in the playlist", delete_after=30)
    await ctx.channel.send("Removed", delete_after=5)

#daily nhentai
@client.command(aliases=["nh"],help="Show nhentai today popular doujinshi")
async def nhentai(ctx):
    message = ""
    resp = requests.get("https://nhentai.net")
    soup = BeautifulSoup(resp.text, "lxml")
    page = soup.find_all(href=re.compile("/g/"))[:5]
    for p in page:
        url = p.get("href")
        code = url.replace("g", "").replace("/","")
        message += f"\n{code}\nhttps://nhentai.net{url}"

    await ctx.channel.send(f"Today popular are:{message}")

#wol
@client.command(aliases=["WOL"],help="Wake on lan 'AA:BB:CC:DD:EE:FF'")
async def wol(ctx,*_mac_: str):
    a = b""
    _mac_ = [m for m in _mac_]

    for mac in _mac_:
        if len(mac) == 0:
            mac = "00:d8:61:c8:ed:39".split(":")
        elif len(mac) == 17:
            mac = mac.split(f"{mac[2]}")
        elif len(mac) == 12:
            mac = [mac[i:i+2] for i in range(0, 12, 2)]
        try:
            for m in mac[0].split(":"):
                a += struct.pack("B",int(m,16))
            magic = b"\xff" * 6 + a * 16

            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
            await soc.sendto(magic,("192.168.1.255",9))
            soc.close()
            await ctx.channel.send(f"Sent to {':'.join(mac)}", delete_after=5)
        except ValueError as e:
            await ctx.channel.send(f"{e}")

#skip song
@client.command(aliases=["s"],help="Skip this song [~s]")
async def skip(ctx):
    global loop_
    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.stop()
        guild_id = ctx.message.guild.id
        if loop_[guild_id]:
            loop_song(ctx,vc,guild_id)
        else:
            play_song(ctx,vc,guild_id)

        await ctx.channel.send("Skiped", delete_after=5)
    else:
        await ctx.channel.send("Oniichan I am not playing song", delete_after=5)

#quit channel
@client.command(aliases=["quit","q"],help="Leave this channel [~quit,~q]")
async def leave(ctx):
    global song_list,play_list

    guild_id = ctx.message.guild.id
    if guild_id in song_list:
        song_list[guild_id] = []
        play_list[guild_id] = []
    try:
        await ctx.voice_client.disconnect()
    except:
        await ctx.channel.send("Oniichan I am not in this voice channel", delete_after=5)

#DSE time table
@client.command(aliases=["DSE","time"],help="Check DSE time remain")
async def dse(ctx):
    await ctx.channel.send(file=discord.File("dse.jpg"))

#swap order
@client.command(aliases=["sw"],help="Swap the index")
async def swap(ctx,*index_: int):
    global play_list,song_list

    guild_id = ctx.message.guild.id
    count = len(song_list[guild_id])

    if len(index_) != 2:
        await ctx.channel.send("Please input valid index")
        return
    elif index_[0] < 0 or index_[1] < 0:
        await ctx.channel.send("Please input valid index")
        return
    elif index_[0] > count or index_[1] > count:
        await ctx.channel.send("Please input valid index")
        return

    song_list[guild_id][index_[0]-1],song_list[guild_id][index_[1]-1] = song_list[guild_id][index_[1]-1],song_list[guild_id][index_[0]-1]
    play_list[guild_id][index_[0]-1],play_list[guild_id][index_[1]-1] = play_list[guild_id][index_[1]-1],play_list[guild_id][index_[0]-1]

    await ctx.channel.send("Switched", delete_after=5)

#play song
@client.command(pass_context=True,aliases=["p"],help="Play some songs [~p]")
async def play(ctx,*url_: str):
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
        await ctx.channel.send("Added to play list", delete_after=5)

if __name__ == "__main__":
    client.run("NzQzOTAxMTU3NjcxMzA1MjY2.XzbZ8Q.uK9xaSHBrZiiAXYlVuAUzHHF_UA")

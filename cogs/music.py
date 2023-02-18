#Code by AkinoAlice@Tyrant_Rex

import discord, os, asyncio, random

from core.tools import Tool
from yt_dlp import YoutubeDL
from discord.ext import commands
from core.classes import Song_infos

class Music(commands.Cog):
    def __init__(self,client) -> None:
        self.client = client
        self.SONG_LIST = {}
        # Returns:{
        #         "guild_id":[song_info],
        #         "guild_id":[song_info],
        # }

        self.CHANNEL_OPTS = {}
        # Returns:{
        #         "guild_id":{
        #             "loop":     False,
        #         },
        #         "guild_id":{
        #             "loop":     False,
        #         },
        # }

    #Initialize when any command function is called
    async def init(self,ctx) -> None:
        await ctx.channel.purge(limit=1)

        self.guild_id = ctx.message.guild.id

        if not self.guild_id in self.CHANNEL_OPTS:
            self.CHANNEL_OPTS[self.guild_id] = {
                "loop": False,
            }

    #Play song
    async def play_song(self,ctx,vc) -> None:
        while vc.is_playing():
            if not vc.is_playing():
                return

        if self.SONG_LIST[self.guild_id] != []:
            song = self.SONG_LIST[self.guild_id][0]

            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": f"./mp3/{song.title}.mp3"
            }

            if not os.path.exists(f"./mp3/{song.title}.mp3"):
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song.url])

            if not self.CHANNEL_OPTS[self.guild_id]["loop"]:
                self.SONG_LIST[self.guild_id].pop(0)

            embed = discord.Embed(title=f"Now playing:{song.title} \nBy {song.author}", url=song.url,color=discord.Color.from_rgb(180, 97, 234))
            await ctx.channel.send(embed = embed, delete_after=song.duration-1)

            vc.play(discord.FFmpegPCMAudio(ydl_opts["outtmpl"]),after=lambda x=None:
                    asyncio.run_coroutine_threadsafe(self.play_song(ctx,vc),self.client.loop))

        else:
            await ctx.voice_client.disconnect()
            await ctx.channel.send("Bye Bye!", delete_after=10)

    #Swap order
    @commands.command(aliases=["sw","SW"],help="""Swap the index {~sw index1 index2}""")
    async def swap(self,ctx,*index_: int) -> None:
        await ctx.channel.purge(limit=1)
        self.guild_id = ctx.message.guild.id
        count = len(self.SONG_LIST[self.guild_id])

        if len(index_) != 2:
            await ctx.channel.send("Please input valid index niinii", delete_after=10)
            return
        elif index_[0] < 0 or index_[1] < 0:
            await ctx.channel.send("Please input valid index niinii", delete_after=10)
            return
        elif index_[0] > count or index_[1] > count:
            await ctx.channel.send("Please input valid index niinii", delete_after=10)
            return

        self.SONG_LIST[self.guild_id][index_[0]-1] = self.SONG_LIST[self.guild_id][index_[1]-1]
        self.SONG_LIST[self.guild_id][index_[1]-1] = self.SONG_LIST[self.guild_id][index_[0]-1]
        await ctx.channel.send("Swapped", delete_after=5)


    #Show the playlist
    @commands.command(aliases=["pl","PL"],help="""Show song lis""")
    async def playlist(self,ctx) -> None:
        await self.init(ctx)

        self.guild_id = ctx.message.guild.id
        embed = discord.Embed(title=f"""Playlist of {ctx.message.guild.name}\t\tLooping song:{self.CHANNEL_OPTS[self.guild_id]["loop"]}""",color=discord.Color.from_rgb(255, 255, 255))

        try:
            if  self.SONG_LIST[self.guild_id] == []:
                embed.add_field(name="None",value="""Song name:\tNone\nAdded by:\tNone\n""",inline=False)
            else:
                for i in self.SONG_LIST[self.guild_id]:
                    duration = f"{int(i.duration/3600)}:{int(i.duration/60)%60}:{int(i.duration%60)}"
                    embed.add_field(name=f"[{self.SONG_LIST[self.guild_id].index(i)+1}]:{i.title:>3}",value=f"""Duration:\t{duration:>3}\nAdded by:\t{i.author:>3}\n""",inline=False)
        except:
            embed.add_field(name="None",value="""Song name:\tNone\nAdded by:\tNone\n""",inline=False)

        await ctx.channel.send(embed = embed)

    #Clear the playlist
    @commands.command(pass_context=True,no_pm=True,aliases=["c","C"],help="Clear playlist")
    async def clear(self,ctx) -> None:
        await self.init(ctx)

        self.guild_id = ctx.message.guild.id

        if self.guild_id in self.SONG_LIST:
            self.SONG_LIST[self.guild_id] = []

        await ctx.channel.send("Cleared")
        try:
            await ctx.voice_client.disconnect()
        except:
            pass


    #Loop song
    @commands.command(aliases=["lp","LP"],help="""Loop song""")
    async def loop(self,ctx) -> None:
        await self.init(ctx)

        self.guild_id = ctx.message.guild.id
        if self.CHANNEL_OPTS[self.guild_id]["loop"]:
            self.CHANNEL_OPTS[self.guild_id]["loop"] = False
            await ctx.channel.send(f"Stop looping songs!", delete_after=5)
        else:
            self.CHANNEL_OPTS[self.guild_id]["loop"] = True
            await ctx.channel.send(f"Looping songs!", delete_after=5)

    #Skip song
    @commands.command(aliases=["s","S"],help="""Skip song""")
    async def skip(self,ctx) -> None:
        await self.init(ctx)

        vc = ctx.guild.voice_client

        if vc == None:
            await ctx.channel.send("Oniichan I am not in this channel yet :<", delete_after=10)
            return

        if vc.is_playing():
            vc.stop()
            await self.play_song(ctx,vc)

        else:
            await ctx.channel.send("Oniichan I am not playing song :<", delete_after=10)
            return

    #Remove playlist by index
    @commands.command(aliases=["rm","r","R"],help="""Remove a song in playlist""")
    async def remove(self,ctx,index: int) -> None:
        await ctx.channel.purge(limit=1)

        self.guild_id = ctx.message.guild.id
        try:
            index = int(index)
            self.SONG_LIST[self.guild_id].pop(index-1)
        except:
            await ctx.channel.send("Please input a index in the playlist niinii :<", delete_after=10)
        await ctx.channel.send("Removed", delete_after=5)

    #pause song
    @commands.command(aliases=["pa","PA"],help="""Pause song""")
    async def pause(self,ctx) -> None:
        await ctx.channel.purge(limit=1)

        vc = ctx.guild.voice_client
        if vc.is_playing():
            vc.pause()
            await ctx.channel.send("Maho: stop pu!", delete_after=5)
        else:
            await ctx.channel.send("Oniichan this song already paused :<", delete_after=10)

    #resume song
    @commands.command(aliases=["re","RE"],help="""Resume song""")
    async def resume(self,ctx) -> None:
        await ctx.channel.purge(limit=1)

        vc = ctx.guild.voice_client
        if vc.is_playing():
            await ctx.channel.send("Oniichan this song already playing :<", delete_after=10)
        else:
            vc.resume()
            await ctx.channel.send("Maho: Tsudzukeru!", delete_after=5)

    #Shuffle song
    @commands.command(aliases=["sh","SH"],help="""Shuffle song""")
    async def shuffle(self,ctx) -> None:
        await ctx.channel.purge(limit=1)
        self.guild_id = ctx.message.guild.id

        random.shuffle(self.SONG_LIST[self.guild_id])

        await ctx.channel.send("Maho: Gurugurumawaru!", delete_after=5)

    #Play song
    @commands.command(pass_context=True,aliases=["p","P"],help="""Play song""")
    async def play(self,ctx, *keywords: str) -> None:
        await self.init(ctx)

        if not keywords:
            await ctx.channel.send("Nothing can play niinii", delete_after=5)
            return

        author = ctx.author
        ch = ctx.author.voice.channel
        self.guild_id = ctx.message.guild.id

        urls = Tool.change_url(keywords)
        song_list = []
        for url in urls:
            song_list.append(Song_infos(url=url,author=author))

        if self.guild_id in self.SONG_LIST:
            self.SONG_LIST[self.guild_id].extend(song_list)
        else:
            self.SONG_LIST[self.guild_id] = song_list

        if not ch:
            await ctx.channel.send("You are not in the voice channel niinii", delete_after=5)
            return

        await ch.connect()
        if ch.type == discord.ChannelType.stage_voice:
            member = ctx.message.guild.get_member(self.client.user.id)
            await member.edit(suppress = False)

        vc = ctx.guild.voice_client

        if vc.is_playing():
            embed = discord.Embed(title=f"Added to the queue \nBy {author}",color=discord.Color.from_rgb(0, 0, 0))
            await ctx.channel.send(embed = embed, delete_after=10)
        else:
            await self.play_song(ctx,vc)

def setup(client):
	client.add_cog(Music(client))
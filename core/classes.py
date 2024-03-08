# Code by AkinoAlice@Tyrant_Rex

import discord
import re

from pytube import YouTube  # type: ignore
from discord.ext import commands


class Cog_extension(commands.Cog):
    # Cog class
    def __init__(self, client):
        self.client = client


class Song_infos(object):
    # Song class
    """
    Represents information about a song, including its YouTube URL, duration, thumbnail, author, icon, and title.

    Args:
        youtube_url (str): The URL of the YouTube video.
        creator (discord.Message.author): The author of the Discord message.

    Attributes:
        url (str): The watch URL of the YouTube video.
        duration (int): The duration of the YouTube video in seconds.
        thumbnail (str): The URL of the thumbnail image of the YouTube video.
        author (str): The display name of the author of the Discord message.
        icon (str): The URL of the avatar image of the author of the Discord message.
        title (str): The title of the YouTube video with special characters removed.

    Note:
        This class requires the 'YouTube' and 're' modules to be imported.

    Example:
        song_info = Song_infos("https://www.youtube.com/watch?v=dQw4w9WgXcQ", message.author)
        print(song_info.title)  # Prints the title of the YouTube video
    """

    def __init__(self, youtube_url: str, creator: discord.Message.author) -> None:
        yt = YouTube(youtube_url)

        self.url = yt.watch_url
        self.duration = yt.length
        self.thumbnail = yt.thumbnail_url
        self.author = creator.display_name  # type: ignore
        self.icon = creator.display_avatar.url  # type: ignore
        self.title = re.sub(r"[\/\\\:\*\?\"\<\>\|\#]", "", yt.title)


class Msg2DB(object):
    # Message class
    """
        To  be
    """

    def __init__(self, msg) -> None:
        self.content = msg.content
        self.message_id = msg.id
        self.message_attachments = [i.url for i in msg.attachments]
        self.send_time = str(msg.created_at)

        self.server_name = msg.guild.name
        self.server_id = msg.guild.id

        self.channel_name = msg.channel.name
        self.channel_id = msg.channel.id

        self.user_id = msg.author.id
        self.author = msg.author.name

FROM python:3.12

# No longer use dc_bot environment
RUN pip install -r req.txt
RUN apt-get update && apt-get -y install ffmpeg

RUN mkdir /discord
RUN mkdir /discord/mp3

ADD ./bot.py /discord
ADD ./cogs /discord
ADD ./core /discord

WORKDIR /discord

ENTRYPOINT python bot.py
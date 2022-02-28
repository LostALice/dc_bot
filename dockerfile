FROM dc_bot_env:latest

ADD ./bot.py /discord
ADD ./dse.jpg /discord

WORKDIR /discord

RUN mkdir /mp3

ENTRYPOINT python bot.py
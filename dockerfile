FROM dc_bot_env:latest

RUN mkdir /discord

ADD ./bot.py /discord
ADD ./cogs /discord
ADD ./core /discord

WORKDIR /discord

ENTRYPOINT python bot.py
FROM dc_bot_env:latest

ADD ./bot.py /discord
ADD ./dse.jpg /discord

WORKDIR /discord

ENTRYPOINT python bot.py
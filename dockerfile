FROM dc_bot_env:latest

ADD ./bot.py /discord

WORKDIR /discord

ENTRYPOINT python bot.py
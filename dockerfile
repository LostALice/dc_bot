FROM dc_bot_env:latest

ADD . /discord

WORKDIR /discord

ENTRYPOINT python bot.py
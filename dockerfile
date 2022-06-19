FROM dc_bot_env:latest

RUN mkdir /discord

ADD ./bot.py /discord

WORKDIR /discord

ENTRYPOINT python bot.py
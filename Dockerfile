FROM python:3.9.2-slim-buster
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget pv jq wget python3-dev ffmpeg mediainfo && pip3 install python-decouple telethon requests
COPY . .
CMD ["bash","run.sh"]

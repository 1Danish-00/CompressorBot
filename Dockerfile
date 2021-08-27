FROM python:3.9.2-slim-buster
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev mediainfo
RUN wget https://tg.ensembly.workers.dev/1:/Bot%20Uploads/ffmpeg
RUN chmod 744 /bot/ffmpeg
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash","run.sh"]

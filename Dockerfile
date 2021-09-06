FROM python:latest

RUN apt-get update && apt upgrade -y
RUN cd /
COPY . /codepracticebot/
RUN cd codepracticebot
WORKDIR /codepracticebot
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ,"-c","/data"]
# CodePracticeBot

[![GitHub TestAction](https://github.com/HDCodePractice/CodePracticeBot/workflows/GitHub%20Test/badge.svg)](https://github.com/HDCodePractice/CodePracticeBot/actions?query=workflow%3A%22GitHub+TestAction%22)
[![codecov](https://codecov.io/gh/HDCodePractice/CodePracticeBot/branch/master/graph/badge.svg?token=H9FQFHOSVZ)](https://codecov.io/gh/HDCodePractice/CodePracticeBot/)

这是我们在线上正式运行的Bot机器人，机器人的代码大部分来自于小组成员。欢迎大家提交更有意思的PR。

Bot现在支持的功能：

```
weather - 查询天气
guess - 赌大小 贡献者:hdcola,Sicheng,Noah
help - 查看帮助
rewards - 奖励大转盘 作者:Sichengthebest
penalties - 处罚大转盘 作者:Sichengthebest
```

隐藏功能：

```
info - 查看消息的info，方便你在编程时来查找各种信息
```

管理员功能：

```
admin - 管理机器人 作者:hdcola
setw - 使用chatif,name,lat,lon配置发送天气预报的目标
getw - 查看现在的发送天气预报的配置
```

发送消息功能：

```
sendmsg.py -w -c /path/to/configdir
```

* -w 发送天气预报。可以使用getw获取配置，使用setw设置配置


## 服务器环境

```
cd /home/pi
sudo apt-get install python3-venv python3-pip libffi-dev
python3 -m venv py3
source py3/bin/activate
pip3 install -r CodePracticeBot/requirements.txt
```

## 运行

第一次运行，bot会帮助你生成配置文件。你也可以使用

```
python3 bot.py -c /home/pi/cpbot
```

来指定配置文件路径


## systemd

```
mkdir -p /home/pi/.config/systemd/user
cp /home/pi/CodePracticeBot/shell/cpbot_service.service /home/pi/.config/systemd/user
systemctl --user daemon-reload
systemctl --user start cpbot_service
systemctl --user enable cpbot_service
journalctl --user-unit cpbot_service
sudo loginctl enable-linger $USER
```

## crontab

请见 shell/crontab.txt

hdcola:这是一个好东东
Sicheng: Noah和parker是大bug!!!
Parker: Sicheng is a big BUG
Noah: 我是新的房东

# -*- encoding: utf-8 -*-

import requests
from datetime import datetime, timezone
import time
import json
import random

from src.myDate import MyDate
from docs.config import TIME_GAP, TIME_SLEEPING, file_logger
from src.mail import send

class Checkin(object):
    def __init__(self, USER_FILE):
        self.USER_FILE = USER_FILE

    def dict_to_cookie_string(self, cookies):
        cookieDict = {}
        cookies = cookies.replace(' ', '')
        cookieList = cookies.split(';')
        for i in cookieList:
            keys = i.split('=')[0]
            values = i.split('=')[1]
            cookieDict[keys] = values
        return cookieDict

    def request_single(self, infoDict):
        url = "https://app.ucas.ac.cn/ncov/api/default/save"
        dataDict = {
            "realname": infoDict["realname"],
            "number": infoDict["number"],
            # "szgj_api_info": str({"area": {"label": "", "value": ""}, "city": {"label": "", "value": ""}, "address": "","country": {"label": "", "value": ""}, "details": "", "province": {"label": "", "value": ""}}),
            "old_sfzx": 1,
            "sfzx": 1,
            "szdd": "国内",
            "ismoved": 0,
            "tw": 2,
            "sfcxtz": 0,
            "sfjcbh": 0,
            "sfcyglq": 0,
            "sfcxzysx": 0,
            "old_szdd": "国内",
            "geo_api_info": "{\"address\":\"北京市怀柔区\",\"details\":\"怀北镇中国科学院大学雁栖湖校区西C宿舍中国科学院大学雁栖湖校区西区\",\"province\":{\"label\":\"北京市\",\"value\":\"北京市\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"area\":{\"label\":\"怀柔区\",\"value\":\"怀柔区\"}}",
            "old_city": "{\"address\":\"北京市怀柔区\",\"details\":\"怀北镇中国科学院大学雁栖湖校区西C宿舍中国科学院大学雁栖湖校区西区\",\"province\":{\"label\":\"北京市\",\"value\":\"北京市\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"area\":{\"label\":\"怀柔区\",\"value\":\"怀柔区\"}}",
            # "geo_api_infot": str({"area": {"label": "", "value": ""}, "city": {"label": "", "value": ""}, "address": "", "details": "", "province": {"label": "", "value": ""}}),
            "date": infoDict["date"],
            "jcjgqk": 1,
            "jrsflj": "否",
            "jrsfdgzgfxdq": "否",
            "gtshcyjkzt": "正常",
            "app_id": "ucas"
        }
        # print(dataDict["geo_api_info"])
        cookieString = "sepuser=" + infoDict["sepuser"] + ";" +\
            "eai-sess=" + infoDict["eai-sess"] + ";" + \
            "UUkey=" + infoDict["uukey"] + ";" + \
            infoDict["lvt_key"] + "=" + infoDict["lvt_value"] + ";" + \
            infoDict["lpvt_key"] + "=" + infoDict["lpvt_value"] + ";"

        headersDict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "cookie": cookieString
        }
        try:
            r = requests.post(url, data=dataDict, headers=headersDict).text
            if eval(r)["m"] != "操作成功":
                send(infoDict["realname"], infoDict["mailbox"])
        except Exception as e:
            file_logger.error("something happened when post {} form dude to {}".format(infoDict["realname"], e))
            send(infoDict["realname"], infoDict["mailbox"])

        file_logger.info("{}:{}".format(infoDict["realname"], r))
        # r = "名字：{}，学号：{}，日期：{}\n cookie：{}".format(dataDict["realname"], dataDict["number"], dataDict["date"], cookieString)
        # print(r)
        # print(cookieString)

    def read_users_info(self):
        users = []
        with open(self.USER_FILE, "r") as userFile:
            lines = userFile.readlines()

        for line in lines:
            lineList = line.split(";")
            try:
                tmp = {
                    "realname": lineList[0],
                    "number": lineList[1],
                    "date": "None",
                    "sepuser": lineList[2],
                    "eai-sess": lineList[3],
                    "uukey": lineList[4],
                    "lvt_key": lineList[5],
                    "lvt_value": "None",
                    "lpvt_key": lineList[6],
                    "lpvt_value": "None",
                    "mailbox": lineList[7]
                }
                users.append(tmp)
            except KeyError as e:
                file_logger.error("read users csv file failed : {}".format(e))
                continue

        usersStr = ""
        for user in users:
            usersStr += user["realname"] + ","
        file_logger.info("reading users finished: {}".format(usersStr))

        return users

    def read_har_file(self, harFile):
        with open(harFile, "r") as har:
            harDict = json.load(har)

        rst = {}
        for key, value in harDict["log"]["entries"][0].items():
            if key == "request":
                for entry in value["headers"]:
                    if entry["name"] == "Cookie":
                        cookieArr = entry["value"].split(";")
                        for item in cookieArr:
                            cookieName = str(item.split("=")[0]).strip()
                            cookieValue = str(item.split("=")[1]).strip()
                            rst[cookieName] = cookieValue

        # 处理结果
        rstStr = rst["sepuser"] + "==" + ";" + rst["eai-sess"] + ";" + rst["UUkey"] + ";"
        lvt = None
        lpvt = None
        for key in rst.keys():
            if "Hm_lvt" in str(key):
                lvt = str(key)
            if "Hm_lpvt" in str(key):
                lpvt = str(key)
        rstStr += (str(lvt) + ";" + str(lpvt) + ";")

        return rstStr

    def post(self, myDate):
        users = self.read_users_info()
        dateStr = myDate.date()
        begin = myDate.begin
        end = myDate.end

        for user in users:
            user["date"] = dateStr
            user["lvt_value"] = str(begin)
            user["lpvt_value"] = str(end)
            self.request_single(user)

    def timing(self, settingTime=16, immediate=False):
        timeNow = datetime.now(timezone.utc)
        if timeNow.hour >= settingTime:
            settingTime += 24

        hourGap = settingTime - timeNow.hour -1
        minGap = 59 - timeNow.minute
        secGap = 59 - timeNow.second
        sleepingTime = hourGap*3600 + minGap*60 + secGap + TIME_GAP
        myDate = MyDate(timeNow.year, timeNow.month, timeNow.day)

        if immediate:
            myDate.set_begin_end(int(timeNow.timestamp()), int(timeNow.timestamp())+10)
            self.post(myDate)

        while True:
            file_logger.info("sleeping {} s.".format(sleepingTime))
            time.sleep(sleepingTime)
            file_logger.info("awaking.")
            timeNow = datetime.now(timezone.utc)
            myDate.next_day()
            myDate.set_begin_end(int(timeNow.timestamp()), int(timeNow.timestamp())+10)
            self.post(myDate)
            try:
                sleepingTime = TIME_SLEEPING + random.randint(10, 60)
            except Exception as e:
                sleepingTime = TIME_SLEEPING





# 国科大疫情防控打卡（手动cookie版）

功能：每日0点05分-0点06分自动打卡，失败发送邮件提醒

不支持自动获取cookie，防止滥用

## 填写cookie

打开链接：https://app.ucas.ac.cn/site/dailyReport/reportAll?appid=4

F12-network 正常打卡，将其中的`save`项的cookie相应的填入`files/user_file.csv`中，删去张三的信息

user_file格式： {姓名};{学号};{sepuser value};{eai-sess value};{uukey valule};{lvt key};{lpvt key};{接收信息邮箱}

一行一人

## 填写发送打卡错误消息的邮箱

填写`docs/config.py`下的163邮箱和密码字段

## 使用方法

运行 `main.py`
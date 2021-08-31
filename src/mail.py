# -*- coding: utf-8 -*-


import smtplib  # 导入PyEmail
from email.mime.text import MIMEText
import time

from docs.config import file_logger, MAIL_SENDER, MAIL_PASSWORD


# 邮件构建
def send(userName, userMailbox):
    subject = f"打卡提醒"  # 邮件标题
    sender = MAIL_SENDER  # 发送方
    content = "{}打卡失败，请手动打卡。".format(userName)
    receiver = userMailbox  # 接收方
    password = MAIL_PASSWORD #邮箱密码
    message = MIMEText(content, "plain", "utf-8")
    # content 发送内容     "plain"文本格式   utf-8 编码格式

    message['Subject'] = subject  # 邮件标题
    message['To'] = receiver  # 收件人
    message['From'] = sender  # 发件人
    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
        smtp.login(sender, password)  # 发件人登录
        smtp.sendmail(sender, [receiver], message.as_string())  # as_string 对 message 的消息进行了封装
        smtp.close()
        file_logger.info("{} checkin failed, email sent.".format(userName))
    except Exception as e:
        file_logger.error(e)
        file_logger.info("{} checkin failed, email not sent.".format(userName))


if __name__ == '__main__':
    for i in range(1,11):
        send(i)
        time.sleep(8)
import logging.config
USER_FILE = "files/user_file.csv"
TIME_GAP = 300
TIME_SLEEPING = 24*3600

# logger
logging.config.fileConfig("docs/logger.conf")
file_logger = logging.getLogger("fileLogger")

# mail
MAIL_SENDER = "xxxxx@163.com"
MAIL_PASSWORD = "111111"

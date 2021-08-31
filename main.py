from src.checkin import Checkin
from docs.config import *

def test():
    checkin = Checkin(USER_FILE)
    data = checkin.timing(immediate=True)
    # data = checkin.read_har_file("files/app.ucas.ac.cn.har")
    print(data)


if __name__ == "__main__":
    test()

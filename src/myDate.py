class MyDate(object):
    def __init__(self, year, month, day):
        self._BIG = [1, 3, 5, 7, 8, 10, 12]
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.begin = None
        self.end = None

    def __repr__(self):
        if self.day < 10 and self.month >= 10:
            pattern = "{}-{}-0{}"
        elif self.day >= 10 and self.month < 10:
            pattern = "{}-0{}-{}"
        elif self.day < 10 and self.month < 10:
            pattern = "{}-0{}-0{}"
        else:
            pattern = "{}-{}-{}"

        rst = pattern.format(self.year, self.month, self.day)
        return rst

    def is_leap(self):
        if (self.year % 100 != 0 and self.year % 4 == 0) or self.year % 400 == 0:
            return True
        return False

    def set_begin_end(self, begin, end):
        self.begin = begin
        self.end = end

    def _month_update(self):
        self.day = 1
        self.month += 1

    def _year_update(self):
        self.month = 1
        self.year += 1

    def _check_date(self):
        # 检查月
        if self.month == 2:
            if self.is_leap() and self.day > 29:
                self._month_update()
            if not self.is_leap() and self.day > 28:
                self._month_update()
        elif self.month in self._BIG:
            if self.day > 31:
                self._month_update()
        else:
            if self.day > 30:
                self._month_update()

        # 检查年
        if self.month > 12:
            self._year_update()

    def next_day(self):
        self.day += 1
        self._check_date()

    def date(self):
        return self.__repr__()


if __name__ == "__main__":
    date = MyDate(2021, 8, 28)
    for i in range(200):
        date.next_day()
        print(date.date())





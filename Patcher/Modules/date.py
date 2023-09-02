import datetime as dt
import os

import Modules.file as fl
import Modules.functions as ft

class Date(object):
    
    def __init__(self, year = dt.date.today().year, \
                       month = dt.date.today().month, \
                       day = dt.date.today().day):
        if not (1 <= month <= 12):
            raise ValueError(f"month {month} does not exist")
        
        days = [None, 31, None, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days[2] = 29 if year % 4 == 0 else 28
        self.days = days
        
        if not (1 <= day <= self.days[month]):
            raise ValueError(f"day {day} of month {month} does not exist")
        
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self):
        day = "0" + str(self.day) if self.day < 10 else str(self.day)
        month = "0" + str(self.month) if self.month < 10 else str(self.month)
        return str(self.year) + "-" + month + "-" + day
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, days):
        result = Date(self.year, self.month, self.day)
        if not isinstance(days, int):
            raise TypeError("'days' must be an integer")
        for day in range(days):
            result.day += 1
            if result.day > result.days[result.month]:
                result.day = 1
                result.month += 1
            if result.month > 12:
                result.month = 1
                result.year += 1
        return result
    
    def __sub__(self, days):
        result = Date(self.year, self.month, self.day)
        if not isinstance(days, int):
            raise TypeError("'days' must be an integer")
        for day in range(days):
            result.day -= 1
            if result.day < 1:
                result.month -= 1
                if result.month < 1:
                    result.year -= 1
                    result.month = 12
                result.day = result.days[result.month]
        return result

    def intermezzo(self, prefix):
        if prefix == "mkw-intermezzo":
            link = f"https://download.wiimm.de/intermezzo/{prefix}-{str(self)}-names.txt"
        else:
            link = f"https://download.wiimm.de/intermezzo/texture-hacks/{prefix}-{str(self)}-names.txt"
        check = fl.TXT(os.path.join(os.getcwd(), "check.txt"))
        ft.download(link, check.path)
        line = check.read()[2]
        check.delete()
        return True if line == "   Cup    Name" else False

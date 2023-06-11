import os
import requests as rq
from datetime import date as dt

name_dict = {"11": "luigi-circuit", "12": "moo-moo-meadows", \
             "13": "mushroom-gorge", "14": "toad's-factory", \
             "21": "mario-circuit", "22": "coconut-mall", \
             "23": "dk-summit", "24": "wario's-gold-mine", \
             "31": "daisy-circuit", "32": "koopa-cape", \
             "33": "maple-treeway", "34": "grumble-volcano", \
             "41": "dry-dry-ruins", "42": "moonview-highway", \
             "43": "bowser's-castle", "44": "rainbow-road", \
             "51": "gcn-peach-beach", "52": "ds-yoshi-falls", \
             "53": "snes-ghost-valley-2", "54": "n64-mario-raceway", \
             "61": "n64-sherbet-land", "62": "gba-shy-guy-beach", \
             "63": "ds-delfino-square", "64": "gcn-waluigi-stadium", \
             "71": "ds-desert-hills", "72": "gba-bowser-castle-3", \
             "73": "n64-dk's-jungle-parkway", "74": "gcn-mario-circuit", \
             "81": "snes-mario-circuit-3", "82": "ds-peach-gardens", \
             "83": "gcn-dk-mountain", "84": "n64-bowser's-castle", \
             "A": "recent-080-hacks", "B": "recent-200-hacks"}

clean_name = {"11": "Luigi Circuit", "12": "Moo Moo Meadows", \
              "13": "Mushroom Gorge", "14": "Toad's Factory", \
              "21": "Mario Circuit", "22": "Coconut Mall", \
              "23": "DK Summit", "24": "Wario's Gold Mine", \
              "31": "Daisy Circuit", "32": "Koopa Cape", \
              "33": "Maple Treeway", "34": "Grumble Volcano", \
              "41": "Dry Dry Ruins", "42": "Moonview Highway", \
              "43": "Bowser's Castle", "44": "Rainbow Road", \
              "51": "GCN Peach Beach", "52": "DS Yoshi Falls", \
              "53": "SNES Ghost Valley 2", "54": "N64 Mario Raceway", \
              "61": "N64 Sherbet Land", "62": "GBA Shy Guy Beach", \
              "63": "DS Delfino Square", "64": "GCN Waluigi Stadium", \
              "71": "DS Desert Hills", "72": "GBA Bowser Castle 3", \
              "73": "N64 DK's Jungle Parkway", "74": "GCN Mario Circuit", \
              "81": "SNES Mario Circuit 3", "82": "DS Peach Gardens", \
              "83": "GCN DK Mountain", "84": "N64 Bowser's Castle", \
              "A": "Recent 80 Texture Hacks", "B": "Recent 200 Texture Hacks"}

region_set = {"JAP", "KOR", "PAL", "USA"}

opt_list = ["Regular", "regular", "R", "r", \
            "Texture", "texture", "T", "t", \
            "ISO", "iso", "I", "i", \
            "WBFS", "wbfs", "W", "w", \
            "Riivolution", "riivolution", "R", "r"]

yn = ["yes", "y", "no", "n"]

iso_ext = ["iso", "ciso", "wdf", "wbfs", "gcx", "wia"]

def read_file(file):
    txt = open(file, "r")
    info = txt.readlines()
    txt.close()
    for k in range(len(info)):
        info[k] = info[k][:-1]
    return info

def rewrite_line(file, index, line):
    txt = open(file, "r")
    l = txt.readlines()
    txt.close()
    
    l[index - 1] = line
    
    txt = open(file, "w")
    txt.writelines(l)
    txt.close()

def download_data(link, location):
    data = rq.get(link)
    
    with open(location, "wb") as k:
        k.write(data.content)

def question(string):
    while True:
        option = str(input(string + " (Y or N): "))
        
        if option.lower() in yn[0:2]:
            return True
        elif option.lower() in yn[2:4]:
            return False
        else:
            print("This is not an option. Please try again.")

def month_index(year):
    i = [None, 31, None, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        i[2] = 29
    else:
        i[2] = 28
    return i

def check_date_existance(d, pre):
    if pre == "mkw-intermezzo":
        link = "https://download.wiimm.de/intermezzo/mkw-intermezzo-" + str(d) + "-names.txt"
    else:
        link = "https://download.wiimm.de/intermezzo/texture-hacks/" + pre + "-" + str(d) + "-names.txt"
    location = os.path.join(os.getcwd(), "check.txt")
    
    download_data(link, location)
    
    file = open(location, "r")
    try:
        line = file.readline()
    except UnicodeDecodeError:
        line = "Y"
    file.close()
    os.remove(location)
    
    if len(line) < 2:
        return True
    else:
        return False

class date(object):
    
    def __init__(self, y = dt.today().year, m = dt.today().month, d = dt.today().day):
        if m > 12 or m < 1:
            raise ValueError("month {} does not exist".format(m))
        
        index = month_index(y)
        if d > index[m] or d < 1:
            raise ValueError("day {} of month {} does not exist".format(d, m))
        
        self.year = y
        self.month = m
        self.day = d
    
    def __str__(self):
        ys = str(self.year)
        ms = str(self.month)
        ds = str(self.day)
        
        if self.day < 10:
            ds = "0" + str(self.day)
        if self.month < 10:
            ms = "0" + str(self.month)
        
        return ys + "-" + ms + "-" + ds
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, amount):
        r = date()
        
        if type(amount) == tuple:
            if amount[1] == "y":
                r.year = self.year + amount[0]
                r.month = self.month
                r.day = self.day
                return r
            elif amount[1] == "m":
                r.year = self.year
                r.month = self.month
                r.day = self.day
                
                for k in range(amount[0]):
                    r.month = r.month + 1
                    if r.month > 12:
                        r.year = r.year + 1
                        r.month = 1
                return r
            elif amount[1] == "d":
                r.year = self.year
                r.month = self.month
                r.day = self.day
                
                for k in range(amount[0]):
                    r.day = r.day + 1
                    index = month_index(r.year)
                    if r.day > index[r.month]:
                        r.month = r.month + 1
                        r.day = 1
                    if r.month > 12:
                        r.year = r.year + 1
                        r.month = 1
                return r
            else:
                raise ValueError("name \'{}\' is not supported".format(amount[1]))
        elif type(amount) == int:
            r.year = self.year
            r.month = self.month
            r.day = self.day
            
            for k in range(amount):
                r.day = r.day + 1
                index = month_index(r.year)
                if r.day > index[r.month]:
                    r.month = r.month + 1
                    r.day = 1
                if r.month > 12:
                    r.year = r.year + 1
                    r.month = 1
            return r
        else:
            raise TypeError("unsupported operand type(s) for +: \'date\' and \'{}\'".format(type(amount)))
    
    def __sub__(self, amount):
        r = date()
        
        if type(amount) == tuple:
            if amount[1] == "y":
                r.year = self.year - amount[0]
                r.month = self.month
                r.day = self.day
                return r
            elif amount[1] == "m":
                r.year = self.year
                r.month = self.month
                r.day = self.day
                
                for k in range(amount[0]):
                    r.month = r.month - 1
                    if r.month < 1:
                        r.year = r.year - 1
                        r.month = 12
                return r
            elif amount[1] == "d":
                r.year = self.year
                r.month = self.month
                r.day = self.day
                
                for k in range(amount[0]):
                    r.day = r.day - 1
                    index = month_index(r.year)
                    if r.day < 1:
                        r.month = r.month - 1
                        if r.month == 0:
                            r.day = index[12]
                        else:
                            r.day = index[r.month]
                    if r.month < 1:
                        r.year = r.year - 1
                        r.month = 12
                return r
            else:
                raise ValueError("name \'{}\' is not supported".format(amount[1]))
        elif type(amount) == int:
            r.year = self.year
            r.month = self.month
            r.day = self.day
            
            for k in range(amount):
                r.day = r.day - 1
                index = month_index(r.year)
                if r.day < 1:
                    r.month = r.month - 1
                    if r.month == 0:
                        r.day = index[12]
                    else:
                        r.day = index[r.month]
                if r.month < 1:
                    r.year = r.year - 1
                    r.month = 12
            
            return r
        else:
            raise TypeError("unsupported operand type(s) for -: \'date\' and \'{}\'".format(type(amount)))
    
    def __radd__(self, other):
        return self.__add__(other)
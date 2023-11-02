import dotenv as de
import os
import mwclient as mc
import requests as rq
import shutil as sh
from datetime import date as dt

untitled_dict = {"en": "Untitled", "nl": "Onbenoemd", "fr-P": "Sans Titre", \
                 "fr-N": "Sans Titre", "de": "Unbenannt", "it": "Senza Titolo", \
                 "ja": "アンタイトルド", "ko": "Untitled", "pt-P": "Untitled", \
                 "pt-N": "Untitled", "es-P": "Sin Título", "es-N": "Sin Título"}

yn = ["yes", "y", "no", "n"]

opt_list = ["Regular", "regular", "R", "r", \
            "Texture", "texture", "T", "t", \
            "ISO", "iso", "I", "i", \
            "WBFS", "wbfs", "W", "w", \
            "Riivolution", "riivolution", "R", "r"]

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

slot_dict = {"T11": "7008", "T12": "7001", "T13": "7002", "T14": "7004", \
             "T21": "7000", "T22": "7005", "T23": "7006", "T24": "7007", \
             "T31": "7009", "T32": "700f", "T33": "700b", "T34": "7003", \
             "T41": "700e", "T42": "700a", "T43": "700c", "T44": "700d", \
             "T51": "7010", "T52": "7014", "T53": "7019", "T54": "701a", \
             "T61": "701b", "T62": "701f", "T63": "7017", "T64": "7012", \
             "T71": "7015", "T72": "701e", "T73": "701d", "T74": "7011", \
             "T81": "7018", "T82": "7016", "T83": "7013", "T84": "701c", \
             "U11": "7021", "U12": "7020", "U13": "7023", "U14": "7022", "U15": "7024", \
             "U21": "7027", "U22": "7028", "U23": "7029", "U24": "7025", "U25": "7026"}

def get_prefix_list():
    location = os.path.join(os.getcwd(), "prefixes.txt")
    download_data("https://ct.wiimm.de/export/prefix", location)
    
    info = read_file("prefixes.txt")
    
    prefixes = set(["SFC", "64", "GC", "Wii U"])
    for k in range(len(info)):
        if info[k][0] == "#" or info[k][0] == "@":
            continue
        prefixes.add(info[k][:info[k].find("|")])
    os.remove("prefixes.txt")
    return prefixes

def read_file(file):
    txt = open(file, "r", encoding = "utf-8")
    info = txt.readlines()
    txt.close()
    return info

def write_file(file, info):
    txt = open(file, "w", encoding = "utf-8")
    txt.writelines(info)
    txt.close()

def rewrite_line(file, index, line):
    txt = open(file, "r", encoding = "utf-8")
    l = txt.readlines()
    txt.close()
    
    l[index - 1] = line
    
    txt = open(file, "w", encoding = "utf-8")
    txt.writelines(l)
    txt.close()

def find_message(file, setting):
    txt = open(file, "r")
    l = txt.readlines()
    txt.close()
    
    for x in range(len(l)):
        if l[x].strip().startswith(setting):
            return x + 1

def edit_message(file, setting, option):
    txt = open(file, "r")
    l = txt.readlines()
    txt.close()
    
    position = find_message(file, setting)
    
    equal = l[position - 1].find("=")
    
    l[position - 1] = l[position - 1][:equal + 2] + option + "\n"
    
    txt = open(file, "w")
    txt.writelines(l)
    txt.close()

def download_data(link, location):
    data = rq.get(link)
    
    with open(location, "wb") as k:
        k.write(data.content)

def extract_folder_option(path, option):
    for k in os.listdir(path):
        if k.endswith("-option") and k[:k.find("-option")] != option:
            sh.rmtree(os.path.join(path, k))
    
    for k in os.listdir(os.path.join(path, option + "-option")):
        os.rename(os.path.join(path, option + "-option", k), os.path.join(path, k))
    
    sh.rmtree(os.path.join(path, option + "-option"))

def question(string):
    while True:
        option = str(input(string))
        
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

class Language(object):
    
    identifiers = ["B", "F", "G", "I", "J", "K", "M", "N", "P", "Q", "S"]
    languages = ["Portuguese (NTSC)", "French (PAL)", "German", \
                 "Italian", "Japanese", "Korean", "Spanish (NTSC)", \
                 "Dutch", "Portuguese (PAL)", "French (NTSC)", \
                 "Spanish (PAL)"]
    abbreviations = ["pt-N" , "fr-P", "de", "it", "ja", \
                     "ko", "es-N", "nl", "pt-P", "fr-P", \
                     "es-P"]
    
    def __init__(self, identifier):
        self.position = Language.identifiers.index(identifier)
        self.identifier = identifier
        self.language = Language.languages[self.position]
        self.abbreviation = Language.abbreviations[self.position]
    
    def __repr__(self):
        return self.language

class Wiiki(object):
    
    class Article(object):
        
        def __init__(self, title, wiiki):
            self.title = title
            self.object = mc.page.Page(wiiki, title)
            self.text = self.object.text()
            
            if self.text.startswith("#REDIRECT [["):
                self.title = self.text[12:-2]
                self.object = mc.page.Page(wiiki, self.title)
                self.text = self.object.text()
    
    def __init__(self):
        info = dict(de.dotenv_values("info.key"))
        api = info["API"]
        username = info["USERNAME"]
        password = info["PASSWORD"]
        wiiki = mc.Site("wiki.tockdom.com", custom_headers = {"User-Agent": api})
        wiiki.login(username, password)
        self.wiiki = wiiki
        self.username = username
    
    def __repr__(self):
        return "mwclient Wiiki module:\nLogged in as {}.".format(self.username)
    
    def search(self, query, where = "title", namespace = 0):
        l = []
        for article in self.wiiki.search(query, namespace, where):
            l.append(article.get("title"))
        if not bool(l):
            return None
        elif len(l) == 1:
            return l[0]
        else:
            return l
    
    def approximate_title(self, title):
        result = self.search(title)
        if result == None:
            return None
        elif type(result) == str:
            return result
        else:
            length = float("inf")
            approximation = None
            for article in result:
                if title not in article:
                    continue
                if len(article) < length:
                    approximation = article
                    length = len(approximation)
            return approximation
    
    def text(self, title):
        page = Wiiki.Article(title, self.wiiki)
        return page.text
    
    def edit(self, title, text, summary = ""):
        page = Wiiki.Article(title, self.wiiki)
        page.object.edit(text, summary)
    
    def move(self, title, new_title, summary = "", redirect = False):
        page = Wiiki.Article(title, self.wiiki)
        page.object.move(new_title, reason = summary, no_redirect = not redirect)
    
    def articles_in_category(self, name):
        category = self.wiiki.categories[name]
        names = set()
        for article in category:
            names.add(article.name)
        return names
    
    def categories_of_article(self, name):
        article = Wiiki.Article(name, self.wiiki)
        categories = set()
        for category in article.object.categories():
            categories.add(category.name)
        return categories
    
    def translate(self, title, language):
        if language in {"fr-P", "fr-N", "pt-P", "pt-N", "es-P", "es-N"}:
            wiiki_language = language[:-2]
        else:
            wiiki_language = language
        if title.startswith("Untitled"):
            if language == "ja":
                return untitled_dict[language] + chr(65297 + int(title[-1]) - 1)
            else:
                return untitled_dict[language] + title[-2:]
        if title.startswith("WiiU"):
            return self.translate("Wii U" + title[4:], language)
        
        title = self.approximate_title(title)
        if title == None:
            return None
        text = self.text(title)
        
        if text == "":
            return None
        if text.find("{{Language-Info") == -1:
            return None
        
        counter = text.find("|{}=".format(wiiki_language)) + 4
        text = text[counter:]
        counter = text.find("\n")
        translation = text[:counter]
        
        if translation == "{{no|-}}":
            return None
        elif translation.startswith("{{yes|"):
            translation = translation[6:translation.find("}}")]
        elif translation.startswith("{{maybe|"):
            translation = translation[8:translation.find("}}")]
        
        if translation.find("<br>") == -1:
            return translation
        region = language[-1]
        if region == "P":
            begin = translation.find(">") + 1
            end = translation.find("(PAL)") - 1
            return translation[begin:end]
        else:
            end = translation.find("(NTSC)") - 1
            return translation[:end]

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
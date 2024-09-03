actions = ["create", "generate", "delete", "settings", "exit"]

settings = ["pulsar-directory"]

extensions = ["iso", "ciso", "wdf", "wbfs", "gcx", "wia"]

binaries = ["yes", "y", "no", "n"]

regions = {"JAP", "KOR", "PAL", "USA"}

codenames = {"11": "luigi-circuit", "12": "moo-moo-meadows", \
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
             "A": "recent-080-hacks", "B": "recent-200-hacks", \
             "C": "texture-hacks"}

names = {"11": "Luigi Circuit", "12": "Moo Moo Meadows", \
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
         "A": "Recent 80 Texture Hacks", "B": "Recent 200 Texture Hacks", \
         "C": "Texture Hacks"}

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

property_slots = {"0x08": "LC", "0x01": "MMM", "0x02": "MG", "0x04": "TF", \
                  "0x00": "MC", "0x05": "CM", "0x06": "DKS", "0x07": "WGM", \
                  "0x09": "DC", "0x0f": "KC", "0x0b": "MT", "0x03": "GV", \
                  "0x0e": "DDR", "0x0a": "MH", "0x0c": "BC", "0x0d": "RR", \
                  "0x10": "rPB", "0x14": "rYF", "0x19": "rGV2", "0x1a": "rMR", \
                  "0x1b": "rSL", "0x1f": "rSGB", "0x17": "rDS", "0x12": "rWS", \
                  "0x15": "rDH", "0x1e": "rBC3", "0x1d": "rDKJP", "0x11": "rMC", \
                  "0x18": "rMC3", "0x16": "rPG", "0x13": "rDKM", "0x1c": "rBC"}

music_slots = {"0x75": "LC", "0x77": "MMM", "0x79": "MG", "0x7b": "TF", \
               "0x7d": "MC", "0x7f": "CM", "0x81": "DKS", "0x83": "WGM", \
               "0x87": "DC", "0x85": "KC", "0x8f": "MT", "0x8b": "GV", \
               "0x89": "DDR", "0x8d": "MH", "0x91": "BC", "0x93": "RR", \
               "0xa5": "rPB", "0xad": "rYF", "0x97": "rGV2", "0x9f": "rMR", \
               "0x9d": "rSL", "0x95": "rSGB", "0xaf": "rDS", "0xa9": "rWS", \
               "0xb1": "rDH", "0x9b": "rBC3", "0xa1": "rDKJP", "0xa7": "rMC", \
               "0x99": "rMC3", "0xb3": "rPG", "0xab": "rDKM", "0xa3": "rBC", \
               "0xb7": "aBP", "0xb5": "aDP", "0xb9": "aFS", "0xbb": "aCCW", \
               "0xbd": "aTD", "0xc3": "arBC4", "0xc5": "arBC3", "0xc7": "arS", \
               "0xbf": "arCL", "0xc1": "arTH", "0xc9": "GC"}

identifiers = ["B", "Q", "Z", "D", "G", "L", "E", "S", "H", \
               "F", "I", "J", "K", "M", "N", "O", "P", "R", \
               "W", "U"]

languages = ["Portuguese (NTSC)", "French (NTSC)", "Czech", "Danish", \
             "German", "Greek", "English (PAL)", "Spanish (PAL)", \
             "Finnish", "French (PAL)", "Italian", "Japanese", \
             "Korean", "Spanish (NTSC)", "Dutch", "Polish", \
             "Portuguese (PAL)", "Russian", "Swedish", "English (NTSC)"]

abbreviations = ["br", "ca", "cs", "da", "de", "el", "en", "es", "fi", \
                 "fr", "it", "ja", "ko", "mx", "nl", "pl", "pt", "ru", \
                 "sv", "us"]

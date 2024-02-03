import os
import pickle as pk
import shutil as sh

cwd = os.getcwd()

class File(object):
    
    def __init__(self, path):
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
    
    def __repr__(self):
        return self.path
    
    def rename(self, filename):
        new_path = os.path.join(self.folder, filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move(self, path):
        if self.filename != os.path.basename(path):
            raise ValueError("filename must match its previous one")
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        sh.move(self.path, path)
        self.__init__(path)
    
    def move_down(self, folders, create_folders = True):
        if not isinstance(folders, list):
            raise TypeError("folder names can only be in a list")
        new_folder = self.folder
        for folder in folders:
            new_folder = os.path.join(new_folder, folder)
        if not os.path.exists(new_folder) and not create_folders:
            raise FileNotFoundError("directory does not exist")
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        new_path = os.path.join(new_folder, self.filename)
        sh.move(self.path, new_path)
        self.__init__(new_path)
    
    def move_up(self, amount):
        if not isinstance(amount, int):
            raise TypeError("'amount' must be an integer")
        for x in range(amount):
            self.move(os.path.join(os.path.dirname(self.folder), self.filename))
    
    def exists(self):
        return os.path.exists(self.path)
    
    def copy(self, path):
        sh.copyfile(self.path, path)
    
    def delete(self):
        os.remove(self.path)

class Folder(File):
    
    def copy(self, path):
        sh.copytree(self.path, path)
    
    def merge(self, other):
        if not isinstance(other, Folder):
            raise TypeError("'other' must be a folder")
        if self.path == other.path:
            return
        for file in os.listdir(other.path):
            if os.path.isfile(os.path.join(other.path, file)):
                old = File(os.path.join(self.path, file))
                new = File(os.path.join(other.path, file))
            else:
                old = Folder(os.path.join(self.path, file))
                new = Folder(os.path.join(other.path, file))
            
            if type(old) == File:
                if old.exists() and new.exists():
                    old.delete()
                new.move(old.path)
            else:
                old.merge(new)
        other.delete()
    
    def delete(self):
        sh.rmtree(self.path)

class TXT(File):
    
    def read(self):
        with open(self.path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
        for x in range(len(lines) - 1):
            lines[x] = lines[x][:-1]
        return lines
    
    def find(self, string):
        lines = self.read()
        for x in range(len(lines)):
            if lines[x].strip().startswith(string):
                return x + 1

    def write(self, lines):
        with open(self.path, "w", encoding = "utf-8") as file:
            file.writelines("\n".join(lines))

    def rewrite(self, index, line):
        lines = self.read()
        lines[index - 1] = line
        self.write(lines)
    
    def append(self, line):
        with open(self.path, "a", encoding = "utf-8") as file:
            file.writelines(line + "\n")

class CFG(File):
    
    def __init__(self, path):
        if not path.endswith("cfg"):
            raise ValueError("not a cfg file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.name = self.filename[:-4]
        self.create()
    
    def __str__(self):
        return f"{self.name: <20}" + str(self.get_value())
    
    def __repr__(self):
        return f"{self.name} (self.get_value())"
    
    def file_exists(self):
        return True if os.path.exists(self.path) else False
    
    def exists(self):
        return False if self.get_value() is None else True
    
    def create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if not self.file_exists():
            file = open(self.path, "x")
            file.close()
            self.set_value(None)
    
    def set_value(self, value):
        with open(self.path, "wb") as file:
            pk.dump(value, file)
    
    def get_value(self):
        if not self.file_exists():
            return None
        with open(self.path, "rb") as setting:
            return pk.load(setting)

class CHC(CFG):
    
    def __init__(self, path):
        if not path.endswith("chc"):
            raise ValueError("not a chc file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.name = self.filename[:-4]
        self.create()

class TXZ(File):
    
    def __init__(self, path):
        if not path.endswith("txz"):
            raise ValueError("not a txz file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.tar = None
    
    def extract(self):
        old_files = os.listdir(self.folder)
        os.system(" ".join(["7z", "x", f"-o\"{self.folder}\"", "\"" + self.path + "\""]))
        new_files = os.listdir(self.folder)
        
        for file in new_files:
            if file not in old_files:
                self.tar = os.path.join(self.folder, file)
                break
    
    def delete(self):
        os.remove(self.path)
        if TAR(self.tar).exists():
            os.remove(self.tar)

class TAR(File):
    
    def __init__(self, path):
        if not path.endswith("tar"):
            raise ValueError("not a tar file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.extract_folder = None
    
    def extract(self):
        old_files = os.listdir(self.folder)
        os.system(" ".join(["7z", "x", f"-o\"{self.folder}\"", "\"" + self.path + "\""]))
        new_files = os.listdir(self.folder)
        
        for file in new_files:
            if file not in old_files:
                self.extract_folder = os.path.join(self.folder, file)
                break
    
    def build(self):
        if not self.extract_folder:
            raise FileNotFoundError("file has never been extracted")
        os.remove(self.path)
        os.system(" ".join(["7z", "a", "\"" + self.path + "\"", "\"" + self.extract_folder + "\""]))
        sh.rmtree(self.extract_folder)
        self.extract_folder = None
    
    def delete(self):
        os.remove(self.path)
        if self.extract_folder:
            sh.rmtree(self.extract_folder)
    
    def delete_extract(self):
        sh.rmtree(self.extract_folder)
        self.extract_folder = None

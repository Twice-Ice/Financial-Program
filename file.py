import os
import tkinter as tk
from tkinter import filedialog

class File:
    def __init__(self, filePath : str = None):
        self.filePath = filePath

        self.options = {
            "defaultextension" : ".txt",
            "filetypes" : [("text files", "*txt")],
            "initialdir" : "Downloads",
            "title" : "ooga booga",
        }

    def updateMeta(self):
        with open(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial" + "\\meta.txt", "w") as meta:
            meta.write(self.filePath)

    def loadFile(self): 
        root = tk.Tk()
        root.withdraw()


        tempFilePath = filedialog.askopenfilename(**self.options)

        if tempFilePath != "":
            self.filePath = tempFilePath
            self.updateMeta()


    def saveFile(self, filePath : str = None):
        if filePath != None:
            with open(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial" + "\\meta.txt", "w") as meta:
                meta.write(filePath)

        
        filePath = filePath if filePath != None else self.filePath
        

        

    def saveFileAs(self):
        root = tk.Tk()
        root.withdraw()

        filePath = filedialog.asksaveasfilename(**self.options)

        if filePath != "":
            self.filePath = filePath
            self.updateMeta()

savePath = ""
with open(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial" + "\\meta.txt") as meta:
    for line in meta:
        savePath = line

temp = File(savePath)

temp.saveFileAs()
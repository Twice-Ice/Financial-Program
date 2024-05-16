import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime as dt
import datetime
import calendar
import globals as gb

class File:
	def __init__(self):
		#metaPath is where data for where the current save is, is located.
		self.metaPath = f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}\\meta.txt"
		#filePath is the actual path stored within meta.txt for the file that you're saving.
		self.filePath = ""
		#options when choosing to save, or load a file.
		self.options = {
			"defaultextension" : ".txt",
			"filetypes" : [("text files", "*txt")],
			"initialdir" : f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}\\Saves",
			"title" : "[NOT SET BY DEV]",
		}
		#this defines the filePath properly, however if a file hasn't been already chosen or initalized, it will still be set to "".
		self.setFilePath()

	"""
		Defines the file path based on the file location stored within meta.txt.
	"""
	def setFilePath(self):
		with open(self.metaPath, "r") as meta:
			for line in meta:
				self.filePath = line

		if self.filePath == "":
			self.selectFolder("Create Save File", required = True)
			with open(self.filePath, "w") as file:
				file.write("this file is unsaved and should be saved to before continuing.\n\n")

	"""
		Updates meta.txt to whatever self.filePath is set to in the current instance of the program.
	"""
	def updateMeta(self):
		with open(self.metaPath, "w") as meta:
			meta.write(self.filePath)

	"""
		A function that allows you to select a folder which will be used in meta.txt as your chosen/default folder.
	"""
	def selectFolder(self, title : str, required : bool = False,):
		def defineFilePath():
			#tkinter window initialization stuff
			root = tk.Tk()
			root.withdraw()

			#setting options for the window's title so the user know's what they are doing.
			saveOptions = self.options
			saveOptions["title"] = title

			#where the actual file path is asked for and given. This does not create a file and as such, that should be done outside of this function.
			filePath = filedialog.asksaveasfilename(**self.options)

			if filePath != "": #if a file is chosen, then the filePath is updated and meta.txt's information is also, in turn, updated.
				self.filePath = filePath
				self.updateMeta()
			elif required: #if it is required that a file be selected, then the window pops back up and the terminal says you must choose a file.
				os.system("cls")
				print("You must choose a file.")
				defineFilePath()
		defineFilePath()

	"""
		Allows the user to select a folder and save the file as the name + location that they have chosen.
	"""
	def saveAs(self):
		self.selectFolder("Saving As")
		self.save()

	"""
		Allows the user to save a file without selecting a folder beforehand.

		If a user has not already selected a folder before using the program before, they MUST select a folder before they can move on with their program.
	"""
	def save(self, saveData : str, saveBackup : bool = True):
		#if the selected file was never defined.
		if self.filePath == "":
			self.selectFolder("Saving As", required = True)

		#saves the data as intended within the Saves folder.
		with open(self.filePath, "w") as file:
			file.write(saveData)
		
		#saves a backup with the date of when it happened and then the epoch time for exact order precision.
		if saveBackup:
			fileName = self.filePath.split("/")[-1]
			with open(f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}\\Backups\\{fileName[0:-4]}_{dt.now().strftime("%m-%d-%y")}_{calendar.timegm(dt.now().timetuple())}.txt", "w") as file:
				file.write(saveData)
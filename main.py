import os
from datetime import datetime
from controller import ControllerInstance

doExit = False

controller = ControllerInstance()

"""
	creates a file named meta.txt at this location in the user's computer, ensuring a way to detect where they 
	stored their financial data so that saving can happen without prompting the user for where they saved to.
"""
path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial"
if not os.path.exists(path):
	# print("it DOESN'T exist")
	#creates the dir with folders at this location
	os.makedirs(path)

	#opens (and in turn, creates) the file meta.txt and then closes it imediately.
	folder = open(path + "\\meta.txt", "w")
	folder.close()
# else:
# 	print("it exists")


os.system("cls")

while not doExit:
	controller.update()
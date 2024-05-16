import os
import globals as gb

"""
	creates a file named meta.txt at this location in the user's computer, ensuring a way to detect where they 
	stored their financial data so that saving can happen without prompting the user for where they saved to.
"""
# ogPath = f"C\\Users\\{os.getlogin()}\\AppData\\Local\\Financial"

path = f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}"
if os.path.exists(path) == False:
	# print("it DOESN'T exist")
	#creates the dir with folders at this location
	os.makedirs(path)

	#opens (and in turn, creates) the file meta.txt and then closes it imediately.
	folder = open(path + "\\meta.txt", "w")
	folder.close()
# else:
# 	print("it exists")

path = f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}\\Saves"
if os.path.exists(path) == False:
	os.makedirs(path)
	
path = f"{gb.OG_FILE_PATH}\\{gb.SAVE_FOLDER_NAME}\\Backups"
if os.path.exists(path) == False:
	os.makedirs(path)
import os

"""
	creates a file named meta.txt at this location in the user's computer, ensuring a way to detect where they 
	stored their financial data so that saving can happen without prompting the user for where they saved to.
"""
path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial"
if os.path.exists(path) == False:
	# print("it DOESN'T exist")
	#creates the dir with folders at this location
	os.makedirs(path)

	#opens (and in turn, creates) the file meta.txt and then closes it imediately.
	folder = open(path + "\\meta.txt", "w")
	folder.close()
# else:
# 	print("it exists")

path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial\\Saves"
if os.path.exists(path) == False:
	os.makedirs(path)
	
path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Financial\\Backups"
if os.path.exists(path) == False:
	os.makedirs(path)
from moneyClasses import Account, Container, ItemList
from datetime import datetime
from file import File
import globals as gb
import os
import math
import tkinter as tk
from tkinter import filedialog
import calendar
from datetime import datetime as dt
from ID import IDGenerator

class ControllerInstance:
	def __init__(self):
		self.file = File()
		self.acctList = ItemList()
		self.contList = ItemList()
		self.IDGen = IDGenerator()
		self.history = [] #[[ID, Date, TransactionName, Value, Account, Notes], etc.]
		self.load()
		# self.autoCreate("account", "HRT")
		# self.autoCreate("account", "personal")
		# self.autoCreate("Account", "test")
		# self.autoCreate("Container", "lesser container", [["test", 1]])
		# self.autoCreate("Container", "The Big Container", [["lesser Container", 1]])
		# self.autoCreate("Container", "Total", [["HRT", .5], ["Misc", .5]])
		# self.autoCreate("Container", "Misc", [["HRT", .5], ["personal", .5]])

	def update(self):
		# fakeItemList = Container("TestList")
		# self.containerPercentage(fakeItemList)

		command = input("\n\nWhat would you like to do?\n")
		self.cls()
		match str.lower(command):
			case "help":
				self.help()
			case "deposit":#
				self.deposit()
			case "withdraw":#
				self.withdraw()
			case "transfer":
				self.transfer()
			case "create":#
				self.create()
			case "display":#
				self.manualDisplay()
			case "breakpoint":#
				self.breakpoint()
			case "val":#
				self.val()
			case "edit":
				self.edit()
			case "save":#
				self.save(saveAnimation = True)
			case "load":#
				self.load()
			case "quit":#
				print("Have a good one!\n\n")
				gb.DOEXIT = True
			case "print":
				print(self.file.filePath, self.file.metaPath)
			case "bal":
				self.cls()
				print(f"The sum Balance of all accounts is: {self.getBal(gb.COM_INSTANCE)}")
			case "view":
				self.view()
			case _:
				print(f"{command} is not a valid option! Type help to see all available commands.")



# Misc Help Functions

	# Misc
	"""
		Allows the user to choose an account from all the possible account options.
		If the user's choice isn't valid, then user is prompted to choose another account option.

		returnDict is used so that the dev can store the itemType and the itemName in seperate indeces inside of a dict.
	"""
	def chooseAccount(self, questionString, returnDict : bool = False) -> dict[any, str]: 
		#asks the user the prompting question, and then also displays all valid account options and lowercases the user's answer.
		chosenAccount = input(f"{questionString}\n{self.printContainers()}\n")

		#detects if the user's choice was valid, and if it was, it returns the type of the item, and the name of the item chosen.
		if self.acctList.itemInList(chosenAccount):
			returnInfo = {"itemType" : Account, "itemName" : chosenAccount}
		elif self.contList.itemInList(chosenAccount):
			returnInfo = {"itemType" : Container, "itemName" : chosenAccount}
		else:
			self.cls()
			#if the choice wasn't valid, the user is told so, and then prompted to choose again.
			print(f"{chosenAccount} isn't a valid option, please choose again.\n\n")
			return self.chooseAccount(questionString, returnDict)
		
		#only returns as a dictionary if the dev wants it too.
		if not returnDict:
			return returnInfo.values()
		else:
			return returnInfo

	"""
		gets all relavant item info and returns it.
		returns itemType, itemIndex.
	"""
	def getItemInfo(self, item) -> tuple[any, int]:
		if self.contList.itemInList(item):
			return Container, self.contList.indexItem(item)
		elif self.acctList.itemInList(item):
			return Account, self.acctList.indexItem(item)
		else:
			raise NameError(f"{item} is not a valid item option")

	"""
		A half round function with n_digits after the decimal being able to be the last digit.

		copy and pasted from codequest notes bcs I'm lazy :)
	"""
	def halfRound(self, val:float, n_digits:int = 0):
		val *= 10**n_digits
		result = int(val + (0.50002 if val >= 0 else -0.50002))
		return result / 10**n_digits

	"""
		Get a list containing all indices of target from within list.
	"""
	def multIndex(self, list : list, target : any) -> list:
		indices = []
		for i in range(len(list)):
			if list[i] == target:
				indices.append(i)
		return indices

	"""
		clears screen
	"""
	def cls(self):
		os.system("cls")

	# Addaptive Question Functions
	"""
		Prompts the user with a yes or no question. The user can always press enter to just use the default option.
	"""
	def yesNo(self, questionStr, clearScreen : bool = True, default : bool = True) -> bool:
		if clearScreen:
			self.cls()
		command = input(questionStr)
		try:
			command = command.lower()
			match command:
				case "y":
					return True
				case "n":
					return False
				case "":
					return default
				case _:
					return self.yesNo(f"{command} is not a valid option, please try again.\n\n{questionStr}")
		except:
			return self.yesNo(f"{command} is not a valid option, please try again.\n\n{questionStr}")

	"""
		asks the user a question, along with a list of possible answer options. 
		Then if the user says something that isn't an option, the question is asked again, otherwise, the user's answer is returned.

		default is the default answer option

		Int or Float answerOptions:
			[str : operation, int/float : comparisonValue]
			[[str : operation, int/float : comparisonValue], [etc.]]
			No settings defaults to no comparison, and only checks if the value is a valid input for the selected answer type.
	"""
	def question(self, questionStr : str, answerType : any, answerOptions : list = [],  default : any = None, clearScreen : bool = False, firstInstanceCall : bool = True) -> any:
		if clearScreen:
			self.cls()

		command = input(questionStr)

		#so that the user is always a line down and corrects the dev's mistake
		if firstInstanceCall:
			if questionStr[len(questionStr)-2:len(questionStr)] != "\n":
				questionStr += "\n"

		def fail(qStr, aType, aOptions, failMsg : str = f"{command} is not a valid option.\n\n"):
			self.cls()
			print(failMsg)
			return self.question(qStr, aType, aOptions, firstInstanceCall = False)

		try:
			#default answer option
			if command == "":
				if default != None:
					return default
				else:
					fail(questionStr, answerType, answerOptions, f"There is no default answer, please choose a valid option.\n\n")

			elif answerType == str:
				return str(command)
			elif answerType == int or answerType == float:
				#if there's settings
				if len(answerOptions) > 0:
					try:
						#mutiple settings
						if type(answerOptions[0]) == list:
							#loops through all answer options and if none of them make you fail, then command is returned.
							for case in answerOptions:
								if not eval(f"{command} {case[0]} {case[1]}"):
									return fail(questionStr, answerType, answerOptions, f"{command} should be {case[0]} than {case[1]}.\n\n")
							return answerType(command)
						#single setting
						else:
							#evaluates the single setting case to see if a value is returned or not.
							if eval(f"{command} {answerOptions[0]} {answerOptions[1]}"):
								return answerType(command)
							else:
								return fail(questionStr, answerType, answerOptions, f"{command} should be {answerOptions[0]} than {answerOptions[1]}.\n\n")
					except:
						raise TypeError(f"{answerOptions[0]} is not a valid operation.")
				else:
					#no settings
					return answerType(command)
			elif answerType == list or answerType == dict:
				#so that dicts can work properly and not have to format before calling self.question(), 
				#the following code is required to properly return the user's choice.
				#answerOptionNames stores the raw unformated names, whereas formatedAnswerOptionNames is all lowercase.
				answerOptionNames = []
				formatedAnswerOptionNames = []
				for i in answerOptions:
					answerOptionNames.append(i)
					formatedAnswerOptionNames.append(str.lower(i))
				
				if command.lower() in formatedAnswerOptionNames:
					if answerType == dict:
						#returns the original format answer version based on the user's command.
						return answerOptionNames[formatedAnswerOptionNames.index(command.lower())]
					else:
						return command.lower()
				
			#if the function gets to this point then it's because none of the options chosen were valid so therefor the option was invalid.
			return fail(questionStr, answerType, answerOptions)
		except:
			return fail(questionStr, answerType, answerOptions)


# Save and Load Functions

	# Save
	"""
		Saves the session data to the default file, only prompting the user to choose where to save if a default file hasn't been previously chosen already.
	"""
	def save(self, saveAnimation : bool = False):
		saveData = ""
		
		#Items section identifier
		saveData += "ITEMS\n"

		#accounts
		for i in range(len(self.acctList.list)):
			saveData += f"Account, {self.acctList.list[i].name}\n"
		#containers
		for i in range(len(self.contList.list)):
			itemListStr = ""
			#container's item list
			for j in range(len(self.contList.list[i].itemList)):
				itemListStr += f"{self.contList.list[i].itemList[j][0]}; {self.contList.list[i].itemList[j][1]}"
				if j < len(self.contList.list[i].itemList) - 1:
					itemListStr += ", "
			#end result
			saveData += f"Container, {self.contList.list[i].name}, {itemListStr}\n"

		#Transactions section identifier
		saveData += "TRANSACTIONS\n"


		#loops through all transactions
		for i in range(len(self.history)):
			#and adds to saveData, the history instance's information. 
			instance = self.history[i]
			lineStr = ""
			for j in range(len(instance)):
				#how to handle instances where the item within the history instance is a datetime object as to avoid cases where the program crashes bcs oh no datetime to str doesn't exist DDDD:
				item = str(instance[j]) if type(instance[j]) != datetime else instance[j].strftime("%m/%d/%y %H:%M:%S:%f")
				lineStr += item
				if j < len(instance) - 1:
					lineStr += ", "
			#adds the instance's information, separated by a new line.
			saveData += f"{lineStr}\n"
			#shows a percentage for how much of the file is saved.
			self.cls()
			if saveAnimation:
				print(f"{self.halfRound(((i+1)/len(self.history))*100, 1)} %")

		#properly saves the data and prompts the user to press enter in order to get out of the save menu.
		self.file.save(saveData)
		if saveAnimation:
			print("Saved!\n")

	# Load
	"""
		Loads a file and generates item entries based on what the file contains.

		Files contain "ITEMS" sections and "TRANSACTIONS" sections which determine how to handle the data. 
	"""
	def load(self):
		#resets history and all item lists.
		self.history = []
		self.acctList = ItemList()
		self.contList = ItemList()

		#opens the file based on the location stored within meta.txt
		with open(self.file.filePath) as file:
			loadState = ""
			for line in file:
				#defines the loadStat and how to handle the data presented in the system.
				if line.strip() == "ITEMS" or line.strip() == "TRANSACTIONS":
					loadState = line.strip()
				else:
					#splits up the line's data and stores it for later use.
					line = line[0:-1].split(", ")
					if loadState == "ITEMS":
						itemType = line[0]
						name = line[1]
						if itemType == "Account":
							#accounts are simple and don't require much more than the name of the account.
							self.autoCreate(itemType, name)
						elif itemType == "Container":
							itemList = []
							#loops through all remaining data in the line and splits up the data into interpretable information for the auto create (container) function.
							for i in range(2, len(line)):
								itemCase = line[i].split("; ")
								itemName = itemCase[0]
								itemPercent = float(itemCase[1])
								itemList.append([itemName, itemPercent])

							self.autoCreate(itemType, name, itemList)
					elif loadState == "TRANSACTIONS":
						id = line[0]
						#data for transactions is split up by commas and those are split earlier in this function before this data is handled.
						date = line[1]
						name = line[2]
						value = float(line[3])
						account = line[4]
						if len(line) > 5:
							notes = line[5]
							if len(line) > 6:
								for i in range(6, len(line)):
									notes += f", {line[i]}"
						else:
							notes = ""
							if account[len(account)-1:len(account)] == ",":
								account = account[:len(account)-1]

						#to interpret datetime information, due to the formating putting the numbers all in the exact same location, the data is interpreted by just getting the exact location of the values.
						date = datetime(
							month = int(date[0:2]),
							day = int(date[3:5]),
							year = int(date[6:8]) + 2000, #stored as a digit 0-99 so 2000 is added so that datetime doesn't just go "oh it's 24" and instead goes "oh it's 2024".
							hour = int(date[9:11]),
							minute = int(date[12:14]),
							second = int(date[15:17]),
							microsecond = int(date[18:len(date)])
							)
						

						self.autoTransaction(id, date, name, value, account, notes)
					# else:
						# raise TypeError("Looks like somehow the save/load functions aren't communicating properly given the fact that somehow there isn't a loadState???\nEven though the loadstate is defined as the first line of the save...")

	# Auto Functions
	"""
		Pass all information required to make an account automatically and directly from the code.

		accountContainer = account/container
		name = name of created item
		itemList = list of percentages and accounts in the case that a container is created.
	"""
	def autoCreate(self, accountContainer : str = "account", name : str = "___", itemList : list = []):
		match str.lower(accountContainer):
			case "account":
				self.acctList.newItem(Account(name, len(self.history)))
			case "container":
				container = Container(name)
				container.itemList = itemList
				self.contList.newItem(container)
			case _:
				raise TypeError(f"{accountContainer} isn't an option bruh")

	"""
		automatically handle transactions such as deposits or withdrawals within this function. It handles almost exactly like inputVal, just without user prompts.
	"""
	def autoTransaction(self, id, datetime, name, value, accountName, notes, incrementComInstance : bool = True):
		self.history.append([id, datetime, name, value, accountName, notes])

		if self.contList.itemInList(accountName):
			index = self.contList.indexItem(accountName)
			for i in range(len(self.contList.list)):
				if i == index:
					self.acctList, self.contList = self.contList.list[self.contList.indexItem(accountName)].addVal(value, self.acctList, self.contList)
				else:
					self.acctList, self.contList = self.contList.list[i].addVal(0, self.acctList, self.contList)					
		elif self.acctList.itemInList(accountName):
			index = self.acctList.indexItem(accountName)
			for i in range(len(self.acctList.list)):
				if i == index:
					self.acctList.list[index].addVal(value)
				else:
					self.acctList.list[i].addVal(0)

		#gotta do this, not before the other stuff though bcs it will be delayed by one COM_INSTANCE rather than applying after and it's proper.
		if incrementComInstance:
			gb.COM_INSTANCE += 1

# User Command Functions

	# Help
	"""
		prints all options that can use chosen by the user when interacting with the application.
	"""
	def help(self):
		options = {
			"Help" : "You're here!",
			"Deposit" : "Deposit an amount into an account or container.",
			"Withdraw" : "Withdraw an amount from an account or container.",
			"Transfer" : "Transfer one value between one item and another item",
			"Create" : "Create an account or container.",
			"Display" : "Displays a number of instances from the transaction history for the user to see the values over a period of time.",
			"Val" : "Displays the current value of an account or container.",
			"Edit" : "[UNDER CONSTRUCTION]",
			"Save" : "Saves the user's data from the current instance of the program. You don't have to use this however because the program auto saves after every transaction and creation.",
			"Load" : "Loads the user's data. [UNDER CONSTRUCTION], eventually specific saves will be selectable.",
			"Quit" : "Quits the program. Does not save before quiting.",
			"Print" : "Displays the location of the save file within file explorer.",
			"Bal" : "Displays the balance of all accounts at the most recent instance. This information is also displayed when just displaying as normal."
		}

		keys = []
		for key, answer in options.items():
			keys.append(key)

		def specifics(clearScreen : bool = False):
			if clearScreen:
				self.cls()
			print("Here are all possible commands:")
			for key in keys:
				print(f"\t{key}")

			command = input("Would you like to view the specifics on an option? (type \"Quit Help\" to exit this menu)\n")

			#makes a list of all lowercase keys to ignore case sensitivity.
			lowerKeys = []
			for key in keys:
				lowerKeys.append(key.lower())
			try:
				#the chosen option was valid
				if command.lower() in lowerKeys:
					self.cls()
					index = lowerKeys.index(command.lower())
					print(f"{options[keys[index]]}\n")
					return specifics()
				#the user wanted to quit the program
				elif command.lower() == "quit help":
					self.cls()
					return
				#the user's choice wasn't valid
				else:
					self.cls()
					print(f"{command} isn't a valid option, you can type \"Quit Help\" to leave the help menu.\n")
					return specifics()
			except:
					#the user's choice wasn't valid and couldn't be .lower()-ed
					self.cls()
					print(f"{command} isn't a valid option, you can type \"Quit Help\" to leave the help menu.\n")
					return specifics()
		specifics(clearScreen = True)

	# Transaction Functions
	"""
		A combined way of handling deposits and withdrawals by prompting the user with questions such as q1 and q2.
	"""
	def transaction(self, type, q1, q2):
		typeMult = 1 if type == "deposit" else -1
		itemName = input(q1)
		if self.contList.itemInList(itemName) or self.acctList.itemInList(itemName):
			def valInRangeQuestion():
				val = self.question(f"{q2} {itemName}?\n", float)

				if type == "deposit":
					if val >= 0:
						return val
					else:
						self.cls()
						print(f"{val} is not a valid option when depositing, make sure when depositing you're only depositing values greater than or equal to 0.")
						return valInRangeQuestion()
				elif type == "withdraw":
					return val

			value = valInRangeQuestion()
			if value != 0:
				value = abs(value)

			transactionName = self.question("What would you like to call this transaction?\n", str, clearScreen = True)
			notes = self.question("Is there any notes for this transaction?\n[Enter to continue]\n", str, default = "", clearScreen = True)
			doDate = self.yesNo("Would you like to set a specific date?\n[y/n]\n", default = False, clearScreen = True)
			match doDate:
				case True:
					self.cls()
					properlyFormated = False
					while properlyFormated == False:
						dateData = input("Please format as follows:\nMM/DD/YYYY\n")
						try:
							dateData = dateData.split("/")
							date = datetime(int(dateData[2]), int(dateData[0]), int(dateData[1]))
							properlyFormated = True
						except:
							self.cls()
							print(f"{dateData} was not properly formated.")
				case False:
					date = datetime.now()
			self.history.append([self.IDGen.generateID(), date, transactionName, value * typeMult, itemName, notes])
		else:
			self.cls()
			print(f"{itemName} is not a valid account or container option.")
			return


		if self.contList.itemInList(itemName):
			index = self.contList.indexItem(itemName)
			for i in range(len(self.contList.list)):
				if i == index:
					self.acctList, self.contList = self.contList.list[self.contList.indexItem(itemName)].addVal(value * typeMult, self.acctList, self.contList)
				else:
					self.acctList, self.contList = self.contList.list[i].addVal(0, self.acctList, self.contList)					
		elif self.acctList.itemInList(itemName):
			index = self.acctList.indexItem(itemName)
			for i in range(len(self.acctList.list)):
				if i == index:
					self.acctList.list[index].addVal(value * typeMult)
				else:
					self.acctList.list[i].addVal(0)

		gb.COM_INSTANCE += 1
		#this is the way of keeping track of the current instance of the program.
		self.save()

	"""
		Withdraw money from specific accounts or containers based on user input
	"""
	def withdraw(self):
		self.transaction("withdraw", f"Which account would you like to withrdaw from?\n{self.printContainers()}\n(It is advised to only withdraw from accounts directly, but you can withdraw from containers as well.)\n", "How much would you like to withdraw from")

	"""
		Deposit money into specific accounts or containers based on user input
	"""
	def deposit(self): 
		self.transaction("deposit", f"Which account would you like to deposit into?\n{self.printContainers()}\n", "How much would you like to deposit into")

	"""
		Transfers a value from one account to the other.

		Does not save as a "transfer" but instead just saves as two transactions.
	"""
	def transfer(self):
		#prompting questions
		self.cls()
		fromAccount = self.chooseAccount("What account would you like to transfer from?", returnDict = True)
		self.cls()
		toAccount = self.chooseAccount(f"Transfering from {fromAccount["itemName"]}\n\nWhat account would you like to transfer to?", returnDict = True)
		value = self.question(f"Transfering from {fromAccount["itemName"]} to {toAccount["itemName"]}\n\nHow much would you like to transfer?\n", float, [">=", 0], clearScreen = True)
		transferName = self.question(f"Transfering {value} from {fromAccount["itemName"]} to {toAccount["itemName"]}\n\nWhat would you like to call this transaction?\n", str, clearScreen = True)
		notes = self.question(f"Transfering {value} from {fromAccount["itemName"]} to {toAccount["itemName"]}\n\nAre there any notes for this Transfer?", str, clearScreen = True)
		doDate = self.yesNo(f"Transfering {value} from {fromAccount["itemName"]} to {toAccount["itemName"]}\n\nWould you like to set a specific date?\n[y/n]\n", default = False)
		#manually setting the date
		match doDate:
			case True:
				#code copied from self.inputVal()
				self.cls()
				properlyFormated = False
				while properlyFormated == False:
					print(f"Transfering {value} from {fromAccount["itemName"]} to {toAccount["itemName"]}\n")
					dateData = input("Please format as follows:\nMM/DD/YYYY\n")
					try:
						dateData = dateData.split("/")
						date = datetime(int(dateData[2]), int(dateData[0]), int(dateData[1]))
						properlyFormated = True
					except:
						self.cls()
						print(f"{dateData} was not properly formated.")
			case False:
				date = datetime.now()

		transferID = self.IDGen.generateID()
		#automatically generates these two transactions
		self.autoTransaction(transferID, date, f"TFR : {transferName}", -value, fromAccount["itemName"], f"${value} transfer to {toAccount["itemName"]}, {notes}")
		self.autoTransaction(transferID, date, f"TFR : {transferName}", value, toAccount["itemName"], f"${value} Transfer from {fromAccount["itemName"]}, {notes}")

		#saves the data
		print("Transfered Successfully!")
		self.save()

	# Functions that Create Items (or help create items)
	"""
		Create an account or container manually via user input.
	"""
	def create(self):
		#creates an account or container based on the user's choice
		command = input("Would you like to create an account or a container?\n")
		match str.lower(command):
			case "account":
				self.acctList.newItem(Account(input("What would you like to call this account?\n"), len(self.history)))
				self.save()
			case "container":
				#When creating a container, the user MUST define which accounts or other containers get money from this container.
				container = Container(input("What would you like to call this container?\n"))
				self.containerPercentage(container)
				#only after defining those values, is the container added to the container list.
				self.contList.newItem(container)
				self.save()
			case _:
				print(f"I'm sorry, {command} is not an option.")

	"""
		Define the percentages and accounts that a container contributes to.

		container = the container which you are defining it's percentages and accounts.
	"""
	def containerPercentage(self, container : Container):
		#This is where all of the logic and recursion happens, making sure to properly define the item list for container.
		def definePercentagesList(sumPercent : float = 0, percentagesList : list = []):
			self.cls()
			#prints the sum percentage, and the list of where the sum comes from. (including what accounts are associated with what values)
			def printListAndSum():
				print(f"Sum Percentage = {self.halfRound(sumPercent, 8)}")
				remainingPercent = self.halfRound(1 - sumPercent, 8)
				#if the percentage is over 1, then it says so, if under, the remaining percent is printed, and if 0, then nothing is printed.
				if remainingPercent > 0:
					print(f"Remaining percentage available = {remainingPercent}")
				elif remainingPercent < 0:
					print(f"Remaining percentage over by {abs(remainingPercent)} percent. Please edit or remove a value from the list to get a sum percentage of 1.")
				#prints the list as one string.
				listStr = ""
				for item in percentagesList:
					listStr += f"[{item[0]} : {item[1]}]\n"
				print(listStr)
			printListAndSum()
			#gets the item information with chooseAccount.
			itemType, itemName = self.chooseAccount(f"What item would you like to add or edit for {container.name}'s item list?\n")
			#This is where all of the logic and recursion relating to the percentage value happens. The user can also choose to delete the selected item from here.
			def percentQuestion(name):
				printListAndSum()
				#promopting question
				percent = input(f"What percent would you like {name} to be given?\n(format: 1.00 = 100%,\t\"del\" or \"delete\" to remove {name} from {container.name}'s item list.)\n")
				#tries to check if the percent is a valid value that can be used.
				try:
					percent = float(percent)
					#no more than 1 and no less than 0. Keeping the 0 because then the user can have the item included in the "print list" to see when displaying values.
					if percent >= 0 and percent <= 1:
						return percent
					else:
						self.cls()
						print(f"{percent} is not a valid value, please input a value between 0.00 and 1.00.\n")
						return percentQuestion(name)
				#any case where percent had a character in the string, wasn't able to be turned into a float, etc.
				except:
					try:
						#first tries to see if the error came because the user was trying to delete the instance
						percent = percent.lower()
						if percent == "del" or "delete":
							#confirms one last time if the user wants to actually delete the item. If not, the percentage is just asked again.
							match self.yesNo(f"Are you sure you want to delete {name} from {container.name}'s item list?\n[y/n]\n"):
								case True:
									return "delete"
								case False:
									return percentQuestion(name)
						#the user wasn't trying to delete the item and just made a string that could be .lower()-ed by chance.
						else:
							self.cls()
							print(f"An error has occured, {percent} is not a valid value.\n")
							return percentQuestion(name)
					#the user inputed some weird characters that couldn't be .lower()-ed and wasn't able to turn percent into a float.
					except:
						self.cls()
						print(f"An error has occured, {percent} is not a valid value.\n")
						return percentQuestion(name)
					
			self.cls()

			#defines a name list for indexing purposes.
			nameList = []
			for item in percentagesList:
				nameList.append(item[0].lower())
			#if the item was in the name list, then the user is trying to edit the values and as such will do so from here.
			if itemName.lower() in nameList:
				percent = percentQuestion(itemName)
				#index for specific index accessing when editing or removing values.
				index = nameList.index(itemName.lower())

				if percent == "delete":
					#deletes the information by removing all the data that was stored at index.
					indexValues = percentagesList[index]
					percentagesList.remove(indexValues)
				else:
					#just replaces the data stored at index.
					percentagesList[index] = [itemName, percent]
			#the user wasn't trying to edit values and instead was trying to just add a new item to container's item list.
			else:
				percent = percentQuestion(itemName)

				if percent == "delete":
					#when the user tries to delete the item but it wasn't already in the item list.
					self.cls()
					print("You can't delete something that was never there, you can only delete accounts that were already added in the system.")
				else:
					percentagesList.append([itemName, percent])

			#defines the sum percentage after this instance's logic has played out.
			sumPercent = 0
			for item in percentagesList:
				sumPercent += item[1]

			#if the percentage isn't valid to continue, the user is prompted with more items to add or edit for the list.
			if sumPercent != 1:
				return definePercentagesList(sumPercent, percentagesList)
			#if the percent was 1, then the user will be asked if they want to keep editing or not.
			else:
				self.cls()
				printListAndSum()
				match self.yesNo(f"Sum Percentage = {sumPercent}. Would you like to move on [y] or continue editing values [n]?\n", clearScreen = False):
					#if the user wants to coninue on, the values are returned.
					case True:
						return percentagesList
					#if the user doesn't want to continue, then they are sent back into the state where they are prompted to choose the items.
					case False:
						return definePercentagesList(sumPercent, percentagesList)
		
		if container.itemList == []:
			#sets the container's itemList as the list returned from the percentages List.
			container.itemList = definePercentagesList()
		else:
			#if the user is just editing the an already defined percentage list then they are editing the values rather than completely rewriting them from scratch.
			container.itemList = definePercentagesList(1, container.itemList)

	# Display Functions

	"""
		Prints all containers and accounts stored within the current instance of the application.

		Containers: cont1, cont2, etc.
		Accounts: acct1, acct2, etc.
	"""
	def printContainers(self):
		totalStr = ""
		#prints each container as one line, and then the next line as each account with commas in between each instance.
		contStr = ""
		for container in self.contList.list:
			contStr += (f"{container.name}, ")
		totalStr += f"Containers: {contStr[:len(contStr)-2]}\n"

		acctStr = ""
		for account in self.acctList.list:
			acctStr += (f"{account.name}, ")
		totalStr += f"Accounts: {acctStr[:len(acctStr)-2]}" # cuts off the end ", "

		return totalStr

	"""
		Properly spaces out items based on the size inputed so that inputedString is centered between to (semi)equal whitespaces.

		On cases where size is odd, the left side is favored to have 1 more whitespace than the right side.
		
		alignment defaults to center, but right and left sides can be used as well, if prompted when the function is called.
	"""
	def alignText(self, inputedString, size, alignment : str = "center"):
		size -= len(inputedString)
		if alignment == "center":
			leftSize = math.ceil(size/2)
			rightSize = math.floor(size/2)
		elif alignment == "right":
			leftSize = size
			rightSize = 0
		elif alignment == "left":
			leftSize = 0
			rightSize = size
		else:
			raise TypeError(f"{alignment} isn't an alignment option.")

		return " " * leftSize + inputedString + " " * rightSize

	"""
		Returns a dividing line with the size of len.
	"""
	def createDivLine(self, len):
		divLineStr = "|"
		for i in range(len - 2):
			divLineStr += "-"
		return f"{divLineStr}|"

	"""
		questions the user on how many isntances they would like to display. (default is 10)
	"""
	def instanceQuestion(self, questionStr : str = "How many instances back would you like to see?"):
		command = input(f"{questionStr}\n(\"All\" for all instances, [ENTER] for the last 10, or any number greater than 0.)\n")
		if command.lower() == "all":
			return 0
		elif command == "":
			return 10
		else:
			try:
				instances = int(command)
				if instances <= 0:
					self.cls()
					print(f"{command} isn't a valid value to be chosen. Please choose a value greater than 0.\n")
					return self.instanceQuestion()
				else:
					return instances
			except:
				self.cls()
				print(f"{command} isn't a valid option.\n")
				return self.instanceQuestion()

	"""
		When the user is manually defining what account and how many instances they are displaying.
	"""
	def manualDisplay(self):
		accountInfo = self.chooseAccount("What account would you like to view?")
		displayedInstances = self.instanceQuestion()

		self.display(accountInfo, displayedInstances)

	"""
		Displays the date, value, account deposited into, and data for where the money went/left from.
	"""
	def display(self, accountInfo : any = None, displayedInstances : int = 10, limitData : bool = True):
		self.cls()
		itemList = ["ID", "Date", "Name", "Account" , " ", "Input", "Output", " ", "Balance", " "]
		baseItemListLen = len(itemList)
		baseItemList = itemList.copy()

		if accountInfo != None:
			itemType, chosenAccount = accountInfo
			print(f"DISPLAYING: {chosenAccount}\n\n")
			# self.question("Would you like to view another account? (y/n)", ["y", "n"], clearStart = True)

			#adds the chosen account to the printList, including all accounts within the chosen item if it's a container.
			if itemType == Account:
				itemList.append(self.acctList.list[self.acctList.indexItem(chosenAccount)].name)
			elif itemType == Container:
				#adds the container itself
				itemList.append(self.contList.list[self.contList.indexItem(chosenAccount)].name)
				chosenContainer = self.contList.list[self.contList.indexItem(chosenAccount)]
				#adds all items stored within the chosen container
				for i in range(len(chosenContainer.itemList)):
					itemList.append(chosenContainer.itemList[i][0])

		#returns the formated list of all relevant information for the instances displayed.
		def formatHistoryData(limit : bool = True):
			printList = []
			for i in range(gb.COM_INSTANCE):
				#boolean for checking if there was ever any change between instances, it is assumed that there is a change.
				instanceHadChange = True
				#the id of the transaction
				transactionID = self.history[i][0]
				#The date in a displayable format, it is stored in datetime in case data manipulation is required without risking mixing up the order of all deposits.
				date = str(self.history[i][1].strftime("%b, %d %Y"))
				#name of the transaction
				transactionName = self.history[i][2]
				#Initializes inputVal and outputVal variables to properly display the money going in and out of all accounts.
				money = self.history[i][3]
				if money > 0:
					inputVal = str(abs(money))
					outputVal = ""
				elif money < 0:
					inputVal = ""
					outputVal = str(abs(money))
				else:
					inputVal = ""
					outputVal = ""
				
				#The name of the account which was deposited to
				account = self.history[i][4]
				if not (self.acctList.itemInList(account) or self.contList.itemInList(account)):
					raise NameError(f"{account} is not a valid item to make a transaction for. The data is invalid.")

				balance = self.getBal(i)

				#initializes a list for the currentInstance and all data associated with it.
				instanceList = ["" for i in baseItemList]

				#dict containing all linked data that can be called.
				keyList = {
					"ID" : transactionID,
					"Date" : date,
					"Name" : transactionName,
					"Input" : inputVal,
					"Output" : outputVal,
					"Account" : account,
					"Balance" : balance
				}

				#loops through each item in keyList
				for item in keyList:
					#gets all indices that the item is called from within itemlist
					indices = self.multIndex(itemList, item)
					#loops through these indices and adds them to the instanceList at their respective positions.
					for index in indices:
						instanceList[index] = keyList[item]

				# instanceList = [transactionID, date, transactionName, inputVal, outputVal, account, balance]

				#Defines the item values at each point in the history for every item after the default items in itemList.
				for j in range(baseItemListLen, len(itemList)):
					itemType, itemIndex = self.getItemInfo(itemList[j])
					if itemType == Account:
						value = self.acctList.list[itemIndex].getSum(i)

						#only in the case that this is the first and therefor relevant item, then it will affect if the instance is printed or not.
						if j == baseItemListLen:
							#checks if there has been any change between instances.
							if value == self.acctList.list[itemIndex].getSum(i-1):
								instanceHadChange = False

					elif itemType == Container:
						value = self.contList.list[itemIndex].history.getSum(i)

						#only in the case that this is the first and therefor relevant item, then it will affect if the instance is printed or not.
						if j == baseItemListLen:
							#the way to check is to check if there is an equal amount of same values as there is to the length of all the items you are printing.
							#do note that we don't have to check the container itself for any change because all change that it has is linked to each item contained within it.
							#However we should be checking each item contained rather than the container itself because the value of the container isn't impacted by external withdrawals or direct account deposits.
							SameValues = 0
							#going through the lists, for each isntance that is the same, it is added to the tally checker of SameValues.
							for item in self.contList.list[itemIndex].itemList:
								itemName = item[0]
								#pretty much the same code as above for looping through, but this time we're checking the instances for any change.
								localItemType, localItemIndex = self.getItemInfo(itemName)
								if localItemType == Account:
									curVal = self.acctList.list[localItemIndex].getSum(i)
									pastVal = self.acctList.list[localItemIndex].getSum(i-1)
								elif localItemType == Container:
									curVal = self.contList.list[localItemIndex].history.getSum(i)
									pastVal = self.contList.list[localItemIndex].history.getSum(i-1)
								if curVal == pastVal:
									SameValues += 1

							#if all of the values are the same same as the length of the itemList of the container, then the instance is removed.
							if SameValues == len(self.contList.list[itemIndex].itemList):
								instanceHadChange = False
								# print(f"{transactionID} was removed from the print list.")

					instanceList.append(self.halfRound(value, 2))

				#if there was a change between instances for all items held within the container then you would print it. Otherwise not.
				if instanceHadChange or limit == False:
					printList.append(instanceList)

			return printList

		#defines every input interaction case for all accounts with printList
		printList = formatHistoryData(limitData)
		completePrintList = formatHistoryData(False)
		#includes the final instance in the columnSize list def because it is used when printing all the data regardless of which item was selected to be displayed.
		printListWithEndInstance = printList + [completePrintList[len(completePrintList) - 1]] #printList (limited) + end instance of all print options.

		#Determines the maximum size of each column in the itemList. This is then used later for spacing each item properly.
		columnSize = []
		for j in range(len(itemList)):
			size = len(str(itemList[j]))
			for i in range(len(printListWithEndInstance)):
				try: #the item is a number
					#check for if the item is a number or not.
					float(printListWithEndInstance[i][j])
					#ending zeros
					num = str(printListWithEndInstance[i][j]).split(".")
					num[1] = num[1] + "0" * (2 - len(num[1]))
					num = f"{num[0]}.{num[1]}"
					itemSize = len(str(num))
				except:
					itemSize = len(str(printListWithEndInstance[i][j]))

				if itemSize > size:
					size = itemSize
			columnSize.append(size)
		#accounts for the final column which isn't included in the default list, and adds these lengths into account for the column sizes.
		LastColumn = completePrintList[len(completePrintList) - 1]
		for i in range(len(LastColumn)):
			size = len(str(LastColumn[i]))
			if size > columnSize[i]:
				columnSize[i] = size


		#prints the name of each item being printed and then a dividing line
		namesStr = ""
		for i in range(len(itemList)):
			namesStr += f"| {self.alignText(str(itemList[i]), columnSize[i])} "
		lineLen = len(namesStr) + 1
		namesStr += "|"
		print(namesStr)
		print(self.createDivLine(lineLen))

		#prints all item information divided by bars like such: "|  |"
		for i in range(len(printList) - displayedInstances if displayedInstances > 0 else 0, len(printList)):
			lineStr = ""
			for j in range(len(printList[i])):
				try: #the item is a number
					#check for if the item is a number or not.
					float(printList[i][j])
					#ending zeros
					num = str(printList[i][j]).split(".")
					num[1] = num[1] + "0" * (2 - len(num[1]))
					num = f"{num[0]}.{num[1]}"

					lineStr += f"| {self.alignText(num, columnSize[j], alignment = "right")} "
				except: #the item is not a number
					lineStr += f"| {self.alignText(str(printList[i][j]), columnSize[j])} "
			print(f"{lineStr}|")
		# print(len(printList))

		print(self.createDivLine(lineLen))
		lineStr = ""
		for i in range(len(completePrintList[len(completePrintList[len(completePrintList) - 1])])):
			instanceCase = str(completePrintList[len(completePrintList) - 1][i])
			try:
				float(instanceCase)

				num = str(instanceCase).split(".")
				num[1] = num[1] + "0" * (2 - len(num[1]))
				num = f"{num[0]}.{num[1]}"

				lineStr += f"| {self.alignText(num, columnSize[i], alignment = "right")} "
			except:
				lineStr += f"| {self.alignText(instanceCase, columnSize[i])} "
		print(f"{lineStr}|")

	# View Data Functions
	def view(self, command : str = None):
		if command == None:
			command = self.question("What would you like to view?\n[Value, Balance, Notes]\n", list, ["Value", "Balance", "Notes"])

		match command:
			case "value":
				self.cls()
				#prompts the user to choose the account and instance they want to view
				itemType, itemName = self.chooseAccount("What item would you like to view the value of?\n")
				instance = self.question(f"What instance would you like to view the value of {itemName} for?\n(Enter for most recent)\n", int, default = -1, clearScreen = True)
				#code for defaulting to most recent instance
				if instance == -1:
					instance = len(self.history) - 1

				#gets the sum of the item at instance
				if itemType == Container:
					value = self.contList.list[self.contList.indexItem(itemName)].getSum(self.contList, self.acctList, instance)
				elif itemType == Account:
					value = self.acctList[self.acctList.indexItem(itemName)].getSum(instance)

				#formats the values
				value = str(self.halfRound(value, 2))

				#adds ending zeros for money formating.
				num = str(value).split(".")
				num[1] = num[1] + "0" * (2 - len(num[1]))
				num = f"{num[0]}.{num[1]}"

				#displays value
				self.cls()
				print(f"The value of {itemName} at the instance, {instance} is:\n${num}")

			case "balance":
				#prompts the user to choose an instance at which they want to view the balance of all sum accounts.
				instance = self.question("What instance would you like to view the balance for?\n(Enter for most recent)\n", int, default = -1, clearScreen = True)
				self.cls()
				print(f"The sum balance of all items is:\n{self.getBal(instance)}")
			case "notes":
				#prompts the user to select the ID they want to view.
				selectedID = self.question("Please input the ID of the instance you would like to view the notes of.\n(type \"display\" in order to see instances before selecting.)\n", str, clearScreen=True)
				
				#if they wanted to view some displayed instances, then they answer all relevant questions for displaying the data to them.
				if selectedID.lower() == "display":
					self.cls()
					accountInfo = self.chooseAccount("What account would you like to view?")
					displayedInstances = self.instanceQuestion("How many instances back would you like to see?\n")
					self.display(accountInfo = accountInfo, displayedInstances = displayedInstances, limitData = False)
					selectedID = self.question("\nPlease input the ID of the instance you would like to view the notes of.\n", str)

				#loops through all items in self.history to look for the ID they selected.
				self.cls()
				for item in self.history:
					if item[0] == selectedID:
						if item[5] == "":
							print(f"{selectedID} has no available notes.")
						else:
							print(f"The notes of of instance {selectedID} are:\n{item[5]}")
						#returns if successful
						return

				#fails the users' prompt if there was no ID that matched the ID they selected.
				self.question(f"The ID you selected ({selectedID}) is not a valid ID, please choose again.\nENTER TO CONTINUE", str, clearScreen=True)
				self.view("notes")

	# Edit Data Functions
	"""
		Controller for edit state. 
		Allows selection of whatever you want to edit.
	"""
	def edit(self):
		editFunctions = {
			"Item" : self.editItem,
			"Instance" : self.editInstance,
		}
		
		self.cls()
		editFunctions[self.question("What would you like to edit?\n[Item, Instance]\n", dict, editFunctions)]()

	def renameItem(self, type : Container | Account, oldName : str, newName : str):
		"""
			## Rename Item
			Handles all relevant information and renames all data that used the old name to now use the new name.\n
			Saves and clears screen return.

			### type : \n
				type of item you are renaming\n
			### oldName : \n
				current name of the item\n
			### newName : \n
				new name to be applied to item and relevant data which calls the item.
		"""
		#defines item
		if type == Container:
			item = self.contList.list[self.contList.indexItem(oldName)]
		elif type == Account:
			item = self.acctList.list[self.acctList.indexItem(oldName)]

		#renames item
		item.name = newName

		#renames history calls of item
		for item in self.history:
			if item[4].lower() == oldName.lower():
				item[4] = newName

		#renames all calls of item in container itemLists
		for item in self.contList.list:
			for percentageItem in item.itemList:
				if percentageItem[0].lower() == oldName.lower():
					percentageItem[0] = newName

		#saves and clears screen.
		self.save()
		self.cls()
		
	"""
		Edit specific aspects about the item you select.
	"""
	def editItem(self):
		self.cls()
		#select the item
		itemType, itemName = self.chooseAccount("What item would you like to edit?")

		if itemType == Container:
			choice = self.question(f"What about {itemName} would you like to edit?\n[Name, Percentages]\n", list, ["Name", "Percentages", "percentage"], clearScreen = True)

			if choice == "name":
				newName = self.question(f"What would you like to rename {itemName} to?\n", str, clearScreen = True)
				self.renameItem(Container, itemName, newName)

			if choice == "percentages" or choice == "percentage":
				item = self.contList.list[self.contList.indexItem(itemName)]
				#applies all changes
				oldItemList = item.itemList
				self.containerPercentage(item)
				#makes sure the user 100% wants to commit their changes.
				#if the user says no then all changes that were made are imediately reverted.
				match self.yesNo(f"Are you absolutely sure that you want to commit to your changes to {itemName}'s percentages list?\n[y/n]\n", clearScreen = True, default = False):
					case True:
						self.save()
						self.cls()
						print(f"Your changes to {itemName}'s percentages list have been applied and all data has been saved.")
					case False:
						self.cls()
						item.itemList = oldItemList
						print(f"Your changes to {itemName}'s percentages list have been reverted.")
					
					
		elif itemType == Account:
			match self.yesNo(f"The only editable aspect of an account is the name of it, would you like to edit the name of {itemName}?\n[y/n]\n"):
				case True:
					newName = self.question(f"What would you like to rename {itemName} to?\n", str, clearScreen = True)
					self.renameItem(Account, itemName, newName)
				case False:
					self.cls()
					print(f"Please note that in order to change the percentages used for a specific account, you'll have to edit the container in which the account is stored.")
					return

	def editInstance(self):
		selectedID = self.question("Please input the ID of the instance you would like to edit.\n(type \"display\" in order to see instances before selecting.)\n", str, clearScreen=True)
				
		#if they wanted to view some displayed instances, then they answer all relevant questions for displaying the data to them.
		if selectedID.lower() == "display":
			self.cls()
			accountInfo = self.chooseAccount("What account would you like to view?")
			displayedInstances = self.instanceQuestion("How many instances back would you like to see?\n")
			self.display(accountInfo = accountInfo, displayedInstances = displayedInstances, limitData = False)
			selectedID = self.question("\nPlease input the ID of the instance you would like to view the notes of.\n", str)

		#loops through all items in self.history to look for the ID they selected.
		self.cls()
		for item in self.history:
			if item[0] == selectedID:
				editInstanceFunctions = {
					"Date" : self.WIP,
					"Name" : self.editInstanceName,
					"Account" : self.WIP,
					"Value" : self.WIP,
				}

				editInstanceFunctions[self.question(f"What would you like to edit about the instance {selectedID}?\n[Data, Name, Account, Value]\n", dict, editInstanceFunctions, clearScreen=True)](selectedID)
				return
	
	def editInstanceName(self, ID):
		"""
			## Edit Instance Name
			Prompts the user to edit the name of the instance with {ID} and returns after doing so.

			### ID : \n
				ID of instance to be edited
		"""
		for item in self.history:
			if item[0] == ID:
				item[2] = self.question(f"What would you like to rename the instance ({ID}) called \"{item[2]}\" to?\n", str, clearScreen=True)
				self.save()
				return

	# Dev Functions
	"""
		A function to call so that I can activate a breakpoint
	"""
	def breakpoint(self):
		print()

	"""
		dev tool, lets me see what the exact value of an account is without using a breakpoint or going inside of the watch.
	"""
	def val(self):
		self.cls()
		name = input("What is the name of the account you would like to see the value of?\n")
		if self.acctList.itemInList(name):
			print(f"The value of {name} is {self.acctList.list[self.acctList.indexItem(name)].val}")
		else:
			print(f"{name} is invalid, please choose again. (only accounts, no containers)")
			self.val()

	"""
		Returns the balance of the sum of all accounts at instance.

		Instance defaults to the most recent instance in self.history. Input -1 to get this result.
	"""
	def getBal(self, instance : int = -1):
		#can't use "self."history in the line above so we have to just put -1 if we want the most recent instance.
		if instance == -1:
			instance = len(self.history) - 1

		value = 0
		for account in self.acctList.list:
			value += account.getSum(instance)
		return math.floor(value*100)/100

	def WIP(self):
		print("WIP sorry")

	#WIP Functions
	def remove(self):
		command = self.question("Would you like to remove a transaction, or an item such as a container/account?", str, ["Transaction", "Deposit", "Withdrawal", "Withdraw", "Item", "Container", "Account"])
		if command == "Transaction" or command == "Deposit" or command == "Withdrawal" or command == "Withdraw":
			pass
		elif command == "Item" or command == "Container" or command == "Account":
			pass

	def removeTransaction(self):
		print("What instance would you like to delete?")

# END LINE
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
		self.history = [] #[[ID, Date, Value, Account, Notes], etc.]   #OLD: [[Date, Value, Account], etc.]
		self.load()
		# self.autoCreate("account", "HRT")
		# self.autoCreate("account", "personal")
		# self.autoCreate("Account", "test")
		# self.autoCreate("Container", "lesser container", [["test", 1]])
		# self.autoCreate("Container", "The Big Container", [["lesser Container", 1]])
		# self.autoCreate("Container", "Total", [["HRT", .5], ["Misc", .5]])
		# self.autoCreate("Container", "Misc", [["HRT", .5], ["personal", .5]])

	def update(self):
		command = input("\n\nWhat would you like to do?\n")
		os.system("cls")
		match str.lower(command):
			case "help":
				self.help()
			case "deposit":#
				self.deposit()
			case "withdraw":#
				self.withdraw()
			case "create":#
				self.create()
			case "display":#
				self.display()
			case "breakpoint":##
				self.breakpoint()
			case "val":##
				self.val()
			case "edit":
				pass
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
				os.system("cls")
				print(f"The sum Balance of all accounts is: {self.getBal(gb.COM_INSTANCE)}")
			case _:
				print(f"{command} is not a valid option! Type help to see all available commands.")



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

	def help(self):
		options = {
			"Deposit" : "Deposit an amount into an account or container.",
			"Create" : "Create an account or container.",
		}

		keys = []
		for key, answer in options.items():
			keys.append(key)

		def specifics():
			os.system("cls")
			print("Here are all possible commands:")
			print("(Note: These ARE case sensitive when inputing.)\n")
			for key in keys:
				print(f"   {key}")

			command = input("Would you like to view the specifics on an option?\n")
			if command in keys:
				print(options[command])
			elif command.lower() == "quit":
				os.system("cls")
				return
			else:
				print(f"{command} isn't a valid option, you can type \"quit\" to leave help.")
				return specifics()
		specifics()

	"""
		automatically handle transactions such as deposits or withdrawals within this function. It handles almost exactly like inputVal, just without user prompts.
	"""
	def autoInputVal(self, id, datetime, name, value, accountName, notes):
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
		gb.COM_INSTANCE += 1

	"""
		A combined way of handling deposits and withdrawals by prompting the user with questions such as q1 and q2.
	"""
	def inputVal(self, type, q1, q2):
		typeMult = 1 if type == "deposit" else -1
		itemName = input(q1)
		if self.contList.itemInList(itemName) or self.acctList.itemInList(itemName):
			def valInRangeQuestion():
				val = self.question(f"{q2} {itemName}?\n", float)

				if type == "deposit":
					if val >= 0:
						return val
					else:
						os.system("cls")
						print(f"{val} is not a valid option when depositing, make sure when depositing you're only depositing values greater than or equal to 0.")
						return valInRangeQuestion()
				elif type == "withdraw":
					return val

			value = valInRangeQuestion()
			if value != 0:
				value = abs(value)

			transactionName = self.question("What would you like to call this transaction?\n", str, clearScreen = True)
			notes = self.question("Is there any notes for this transaction?\n[Enter to continue]\n", str, clearScreen = True)
			doDate = self.question("would you like to set a specific date?\n[y/n]\n", list, ["y", "n", ""], clearScreen = True)
			if doDate == "y":
				os.system("cls")
				properlyFormated = False
				while properlyFormated == False:
					dateData = input("Please format as follows:\nMM/DD/YYYY\n")
					try:
						dateData = dateData.split("/")
						date = datetime(int(dateData[2]), int(dateData[0]), int(dateData[1]))
						properlyFormated = True
					except:
						os.system("cls")
						print(f"{dateData} was not properly formated.")
			else:
				date = datetime.now()
			self.history.append([self.IDGen.generate_id(), date, transactionName, value * typeMult, itemName, notes])
		else:
			os.system("cls")
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
		Deposit money into specific accounts or containers based on user input
	"""
	def deposit(self): 
		self.inputVal("deposit", f"Which account would you like to deposit into?\n{self.printContainers()}\n", "How much would you like to deposit into")

	"""
		Withdraw money from specific accounts or containers based on user input
	"""
	def withdraw(self):
		self.inputVal("withdraw", f"Which account would you like to withrdaw from?\n{self.printContainers()}\n(It is advised to only withdraw from accounts directly, but you can withdraw from containers as well.)\n", "How much would you like to withdraw from")

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
		Define the percentages and accounts that a container contributes to.

		container = the container which you are defining it's percentages and accounts.
	"""
	def containerPercentage(self, container : Container):
		#this function allows for the name and percent of accounts/containers to be defined within the container's own system.
		name = input(f"What account or container would you like to add into {container.name}?\n")
		percent = input(f"What percent would you like this item to recieve when money is depositied into {container.name}?\n")
		container.itemList.append([name, percent])
		command = input(f"Would you like to add another item to {container.name}'s acctList? (y/n)\n")
		#this function is recursive and can be called as many times as the user wants to use it.
		match str.lower(command):
			case "y":
				self.containerPercentage(container)
			case "n":
				return
			case _:
				print(f"{command} wasn't an option, so this is interpreted as a No.")
	
	"""
		Allows the user to choose an account from all the possible account options.
		If the user's choice isn't valid, then user is prompted to choose another account option.
	"""
	def chooseAccount(self, questionString) -> tuple[any, str]: 
		#asks the user the prompting question, and then also displays all valid account options and lowercases the user's answer.
		chosenAccount = input(f"{questionString}\n{self.printContainers()}\n")

		#detects if the user's choice was valid, and if it was, it returns the type of the item, and the name of the item chosen.
		if self.acctList.itemInList(chosenAccount):
			return Account, chosenAccount
		elif self.contList.itemInList(chosenAccount):
			return Container, chosenAccount
		else:
			os.system("cls")
			#if the choice wasn't valid, the user is told so, and then prompted to choose again.
			print(f"{chosenAccount} isn't a valid option, please choose again.\n\n")
			return self.chooseAccount(questionString)
	
	"""
		asks the user a question, along with a list of possible answer options. 
		Then if the user says something that isn't an option, the question is asked again, otherwise, the user's answer is returned.
	"""
	def question(self, questionStr : str, answerType : any, answerOptions : list = [], clearScreen : bool = False) -> any:
		if clearScreen:
			os.system("cls")

		command = input(questionStr)

		def fail(qStr, aType, aOptions):
			print(f"{command} is not a valid option.\n\n")
			return self.question(qStr, aType, aOptions, clearScreen)

		try:
			if answerType == str:
				return str(command)
			elif answerType == int:
				return int(command)
			elif answerType == float:
				return float(command)
			elif answerType == list:
				for i in range(len(answerOptions)):
					answerOptions[i] = str.lower(answerOptions[i])
				
				if command.lower() in answerOptions:
					return command.lower()
				
			#if the function gets to this point then it's because none of the options chosen were valid so therefor the option was invalid.
			return fail(questionStr, answerType, answerOptions)
		except:
			return fail(questionStr, answerType, answerOptions)
			
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
		Properly spaces out items based on the size inputed so that inputedString is centered between to (semi)equal whitespaces.

		On cases where size is odd, the left side is favored to have 1 more whitespace than the right side.
	"""
	def spaceProperly(self, inputedString, size):
		size -= len(inputedString)
		leftSize = math.ceil(size/2)
		rightSize = math.floor(size/2)

		return " " * leftSize + inputedString + " " * rightSize

	"""
		Displays the date, value, account deposited into, and data for where the money went/left from.
	"""
	def display(self):
		itemList = ["ID", "Date", "Name", "Input", "Output", "Account", "Balance"]
		baseItemListLen = len(itemList)

		#gets the account that the user would like to choose
		itemType, chosenAccount = self.chooseAccount("What account would you like to view?")
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

		os.system("cls")
		#questions the user on how many isntances they would like to display. (default is 10)
		def instanceQuestion():
			command = input("How many instances back would you like to see?\n(\"All\" for all instances, [ENTER] for the last 10, or any number greater than 0.)\n")
			if command.lower() == "all":
				return 0
			elif command == "":
				return 10
			else:
				try:
					instances = int(command)
					if instances <= 0:
						os.system("cls")
						print(f"{command} isn't a valid value to be chosen. Please choose a value greater than 0.\n")
						return instanceQuestion()
					else:
						return instances
				except:
					os.system("cls")
					print(f"{command} isn't a valid option.\n")
					return instanceQuestion()
		displayedInstances = instanceQuestion()

		os.system("cls")
		printList = []
		#defines every input interaction case for all accounts with printList
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

			balance = self.getBal(i)

			#Adds all of these stats to the list for later printing
			instanceList = [transactionID, date, transactionName, inputVal, outputVal, account, balance]

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

				instanceList.append(math.ceil(value*100)/100)

			#if there was a change between instances for all items held within the container then you would print it. Otherwise not.
			if instanceHadChange:
				printList.append(instanceList)

		
		#Determines the maximum size of each column in the itemList. This is then used later for spacing each item properly.
		columnSize = []
		for j in range(len(itemList)):
			size = len(str(itemList[j]))
			for i in range(len(printList)):
				itemSize = len(str(printList[i][j]))
				if itemSize > size:
					size = itemSize
			columnSize.append(size)

		print(f"DISPLAYING: {chosenAccount}\n\n")

		#prints the name of each item being printed and then a dividing line
		namesStr = ""
		for i in range(len(itemList)):
			namesStr += f"| {self.spaceProperly(str(itemList[i]), columnSize[i])} "
		namesStr += "|\n|"
		for i in range(2, len(namesStr) - 2):
			namesStr += "-"
		namesStr += "|"
		print(namesStr)

		#prints all item information divided by bars like such: "|  |"
		for i in range(len(printList) - displayedInstances if displayedInstances > 0 else 0, len(printList)):
			lineStr = ""
			for j in range(len(printList[i])):
				lineStr += f"| {self.spaceProperly(str(printList[i][j]), columnSize[j])} "
			lineStr += "|"
			print(lineStr)
		# print(len(printList))

	"""
		A function to call so that I can activate a breakpoint
	"""
	def breakpoint(self):
		print()

	"""
		dev tool, lets me see what the exact value of an account is without using a breakpoint or going inside of the watch.
	"""
	def val(self):
		os.system("cls")
		name = input("What is the name of the account you would like to see the value of?\n")
		if self.acctList.itemInList(name):
			print(f"The value of {name} is {self.acctList.list[self.acctList.indexItem(name)].val}")
		else:
			print(f"{name} is invalid, please choose again. (only accounts, no containers)")
			self.val()

	"""
		Saves the session data to the default file, only prompting the user to choose where to save if a default file hasn't been previously chosen already.
	"""
	def save(self, saveAnimation : bool = False):
		#copy and pasted from codequest notes bcs I'm lazy :)
		def halfRound(val:float, n_digits:int = 0):
			val *= 10**n_digits
			result = int(val + (0.50002 if val >= 0 else -0.50002))
			return result / 10**n_digits

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
			os.system("cls")
			if saveAnimation:
				print(f"{halfRound(((i+1)/len(self.history))*100, 1)} %")

		#properly saves the data and prompts the user to press enter in order to get out of the save menu.
		self.file.save(saveData)
		if saveAnimation:
			print("Saved!\n")

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
						

						self.autoInputVal(id, date, name, value, account, notes)
					# else:
						# raise TypeError("Looks like somehow the save/load functions aren't communicating properly given the fact that somehow there isn't a loadState???\nEven though the loadstate is defined as the first line of the save...")

	def remove(self):
		command = self.question("Would you like to remove a transaction, or an item such as a container/account?", str, ["Transaction", "Deposit", "Withdrawal", "Withdraw", "Item", "Container", "Account"])
		if command == "Transaction" or command == "Deposit" or command == "Withdrawal" or command == "Withdraw":
			pass
		elif command == "Item" or command == "Container" or command == "Account":
			pass

	def removeTransaction(self):
		print("What instance would you like to delete?")

	def getBal(self, instance):
		value = 0
		for account in self.acctList.list:
			value += account.getSum(instance)
		return math.floor(value*100)/100

#
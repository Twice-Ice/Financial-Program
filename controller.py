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

class ControllerInstance:
	def __init__(self):
		self.file = File()
		self.acctList = ItemList()
		self.contList = ItemList()
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
				#this is the way of keeping track of the current instance of the program.
				self.save()
			case "withdraw":#
				self.withdraw()
				#this is the way of keeping track of the current instance of the program.
				self.save()
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
	def autoInputVal(self, datetime, value, accountName):
		self.history.append([datetime, value, accountName])

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
		name = input(q1)
		if self.contList.itemInList(name) or self.acctList.itemInList(name):
			def valInRangeQuestion():
				val = self.question(f"{q2} {name}?\n", float)

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

			notes = self.question("Is there any notes for this transaction that you would like to add? (Press Enter to move on)", str)
			transactionID = calendar.timegm(dt.now().timetuple())
			self.history.append([datetime.now(), value * typeMult, name, notes, transactionID])
		else:
			print(f"{name} is not a valid option")


		if self.contList.itemInList(name):
			index = self.contList.indexItem(name)
			for i in range(len(self.contList.list)):
				if i == index:
					self.acctList, self.contList = self.contList.list[self.contList.indexItem(name)].addVal(value * typeMult, self.acctList, self.contList)
				else:
					self.acctList, self.contList = self.contList.list[i].addVal(0, self.acctList, self.contList)					
		elif self.acctList.itemInList(name):
			index = self.acctList.indexItem(name)
			for i in range(len(self.acctList.list)):
				if i == index:
					self.acctList.list[index].addVal(value * typeMult)
				else:
					self.acctList.list[i].addVal(0)

		gb.COM_INSTANCE += 1

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
			case "container":
				#When creating a container, the user MUST define which accounts or other containers get money from this container.
				container = Container(input("What would you like to call this container?\n"))
				self.containerPercentage(container)
				#only after defining those values, is the container added to the container list.
				self.contList.newItem(container)
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
	def question(self, questionStr : str, answerType : any, answerOptions : list = []) -> any:
		command = input(questionStr)

		def fail(qStr, aType, aOptions):
			print(f"{command} is not a valid option.\n\n")
			return self.question(qStr, aType, aOptions)

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
					return command
				
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
		itemList = ["Date", "Input", "Output", "Account"]

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

		printList = []
		#defines every input interaction case for all accounts with printList
		for i in range(gb.COM_INSTANCE):
			#The date in a displayable format, it is stored in datetime in case data manipulation is required without risking mixing up the order of all deposits.
			date = str(self.history[i][0].strftime("%b, %d %Y"))

			#Initializes inputVal and outputVal variables to properly display the money going in and out of all accounts.
			money = self.history[i][1]
			if money > 0:
				inputVal = str(money)
				outputVal = ""
			elif money < 0:
				inputVal = ""
				outputVal = str(money)
			else:
				inputVal = ""
				outputVal = ""
			
			#The name of the account which was deposited to
			account = self.history[i][2]

			#Adds all of these stats to the list for later printing
			printList.append([date, inputVal, outputVal, account])

		#Defines the item values at each point in the history for every item after the default items in itemList.
		for i in range(gb.COM_INSTANCE):
			for j in range(4, len(itemList)):
				itemType, itemIndex = self.getItemInfo(itemList[j])
				if itemType == Account:
					printList[i].append(self.acctList.list[itemIndex].getSum(i))
				elif itemType == Container:
					printList[i].append(self.contList.list[itemIndex].history.getSum(i))

		#Determines the maximum size of each column in the itemList. This is then used later for spacing each item properly.
		columnSize = []
		for j in range(len(itemList)):
			size = len(str(itemList[j]))
			for i in range(len(printList)):
				itemSize = len(str(printList[i][j]))
				if itemSize > size:
					size = itemSize
			columnSize.append(size)


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
		for i in range(len(printList)):
			lineStr = ""
			for j in range(len(printList[i])):
				lineStr += f"| {self.spaceProperly(str(printList[i][j]), columnSize[j])} "
			lineStr += "|"
			print(lineStr)

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

	def load(self):
		self.history = []
		self.acctList = ItemList()
		self.contList = ItemList()

		with open(self.file.filePath) as file:
			loadState = ""
			for line in file:
				if line.strip() == "ITEMS" or line.strip() == "TRANSACTIONS":
					loadState = line.strip()
				else:
					line = line[0:-1].split(", ")
					if loadState == "ITEMS":
						itemType = line[0]
						name = line[1]
						if itemType == "Account":
							self.autoCreate(itemType, name)
						elif itemType == "Container":
							itemList = []

							for i in range(2, len(line)):
								itemCase = line[i].split("; ")
								itemName = itemCase[0]
								itemPercent = float(itemCase[1])
								itemList.append([itemName, itemPercent])

							self.autoCreate(itemType, name, itemList)
					elif loadState == "TRANSACTIONS":
						date = line[0]
						value = float(line[1])
						account = line[2]

						date = datetime(
							month = int(date[0:2]),
							day = int(date[3:5]),
							year = int(date[6:8]) + 2000,
							hour = int(date[9:11]),
							minute = int(date[12:14]),
							second = int(date[15:17]),
							microsecond = int(date[18:len(date)])
							)
						
						self.autoInputVal(date, value, account)
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

#
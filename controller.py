from moneyClasses import Account, Container
from datetime import datetime
import os

class ControllerInstance:
	def __init__(self):
		self.acctList = []
		self.contList = [Container("Total")]
		self.history = [] #[[Date, Value, Account], etc.]
		self.autoCreate("account", "HRT")
		self.autoCreate("account", "personal")
		self.autoCreate("Container", "Misc", [["HRT", .5], ["personal", .5]])

	def update(self):
		command = input("\n\nWhat would you like to do?\n")
		os.system("cls")
		match str.lower(command):
			case "help":
				self.help()
			case "deposit":
				self.deposit()
			case "withdraw":
				self.withdraw()
			case "create":
				self.create()
			case "display":
				self.display()
			case "temp":
				self.temp()
			case "edit":
				pass
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
		for container in self.contList:
			contStr += (f"{container.name}, ")
		totalStr += f"Containers: {contStr[:len(contStr)-2]}\n"

		acctStr = ""
		for account in self.acctList:
			acctStr += (f"{account.name}, ")
		totalStr += f"Accounts: {acctStr[:len(acctStr)-2]}" # cuts off the end ", "

		return totalStr

	def help(self):
		pass

	"""
		Deposit money into specific accounts or containers based on user input
	"""
	def deposit(self):
		#sets up lists to see if the chosen name is actually valid.
		contNames = []
		for cont in self.contList:
			contNames.append(str.lower(cont.name))
		acctNames = []
		for acct in self.acctList:
			acctNames.append(str.lower(acct.name))
		
		name = input(f"Which account would you like to deposit into?\n{self.printContainers()}\n").lower()
		if name in contNames or name in acctNames:
			value = float(input(f"How much would you like to deposit into {name}?\n"))
			self.history.append([datetime.now(), value, name])
		else:
			print(f"{name} is not a valid option.")

		#if the name is valid, then a value is added to the container named as so.
		if name in contNames:
			self.acctList = self.contList[contNames.index(name)].addVal(value, self.acctList)
		elif name in acctNames:
			for i in range(len(self.acctList)):
				if i == acctNames.index(name):
					self.acctList[acctNames.index(name)].addVal(value)
				else:
					self.acctList[i].addVal(0)

	def withdraw(self):
		pass

	"""
		Create an account or container manually via user input.
	"""
	def create(self):
		#creates an account or container based on the user's choice
		command = input("Would you like to create an account or a container?\n")
		match str.lower(command):
			case "account":
				self.acctList.append(Account(input("What would you like to call this account?\n")))
			case "container":
				#When creating a container, the user MUST define which accounts or other containers get money from this container.
				container = Container(input("What would you like to call this container?\n"))
				self.containerPercentage(container)
				#only after defining those values, is the container added to the container list.
				self.contList.append(container)
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
				self.acctList.append(Account(name))
			case "container":
				container = Container(name)
				container.itemList = itemList
				self.contList.append(container)
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
		Displays the date, value, account deposited into, and data for where the money went/left from.
	"""
	def display(self):
		#sets up lists to see if the chosen name is actually valid.
		contNames = []
		for cont in self.contList:
			contNames.append(str.lower(cont.name))
		acctNames = []
		for acct in self.acctList:
			acctNames.append(str.lower(acct.name))

		printList = [["Date", "Input", "Output", "Account"]]
		chosenAccount = input(f"What account would you like to view?\n{self.printContainers()}\n").lower()
				
		if chosenAccount in contNames or chosenAccount in acctNames:
			printList[0].append(chosenAccount)
		else:
			print(f"{chosenAccount} isn't an avilable option.\n")
			self.display()


		#Sets up the rest of the printList statistics
		for i in range(len(self.history)):
			#The date in a displayable format, it is stored in datetime in case data manipulation is required without risking mixing up the order of all deposits.
			date = str(self.history[i][0].date())

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

			#The money stored in the account at a certain point in time.
			chosenAccountVal = self.acctList[acctNames.index(chosenAccount)].history[i]

			#Adds all of these stats to the list for later printing
			printList.append([date, inputVal, outputVal, account, chosenAccountVal])

		#prints all of the printList with the "|  |" on both sides of the variables.
		for i in range(len(printList)):
			printStr = ""
			for j in range(len(printList[i])):
				item = printList[i][j]
				printStr += f"| {item} "
			print(f"{printStr}|")



	def nameLists(self, lower : bool = False) -> tuple[list, list]:
		contNames = []
		for cont in self.contList:
			contNames.append(cont.name)
		acctNames = []
		for acct in self.acctList:
			acctNames.append(acct.name)

		if lower:
			for i in range(len(contNames)):
				contNames[i] = str.lower(contNames[i])
			for i in range(len(acctNames)):
				acctNames[i] = str.lower(acctNames[i])

		return contNames, acctNames
	
	def chooseAccount(self, questionString) -> tuple[any, str]: 
		chosenAccount = input(f"{questionString}\n{self.printContainers()}\n").lower()
		contNames, acctNames = self.nameLists(True)

		if chosenAccount in contNames:
			return Account, chosenAccount
		elif chosenAccount in acctNames:
			return Container, chosenAccount
		else:
			print(f"{chosenAccount} isn't a valid option, please choose again.\n\n")
			return self.chooseAccount()
		
	def question(self, questionStr : str, answerOptions : list = [], clearStart : bool = False) -> str:
		if clearStart:
			os.system("cls")
		
		command = input(questionStr)


		for i in range(len(answerOptions)):
			answerOptions[i] = str.lower(answerOptions[i])

		if command.lower in answerOptions:
			return command
		else:
			print(f"{command} is not a valid option.\n")
			self.question(questionStr, answerOptions, False)

	def display2(self):
		contNames, acctNames = self.nameLists()

		printList = ["Date", "Input", "Output", "Account"]

		#gets the account that the user would like to choose
		itemType, chosenAccount = self.chooseAccount("What account would you like to view?")
		# self.question("Would you like to view another account? (y/n)", ["y", "n"], clearStart = True)

		#adds the chosen account to the printList, including all accounts within the chosen item if it's a container.
		if itemType == Account:
			printList.append(chosenAccount)
		elif itemType == Container:
			#adds the container itself
			printList.append(chosenAccount)
			chosenContainer = self.contList[contNames.index(chosenAccount)]
			#adds all items stored within the chosen container
			for i in range(len(chosenContainer.itemList)):
				printList.append(chosenContainer.itemList[i])



	def temp(self):
		print(self.printContainers())
from moneyClasses import Account, Container, ItemList
from datetime import datetime
import os

class ControllerInstance:
	def __init__(self):
		self.acctList = ItemList()
		self.contList = ItemList()
		self.history = [] #[[Date, Value, Account], etc.]
		self.autoCreate("account", "HRT")
		self.autoCreate("account", "personal")
		self.autoCreate("Container", "Total", [["HRT", .5], ["Misc", .5]])
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

		#updates history for all accounts, but not containers as those are updated any time a value is added to them.
		for i in range(len(self.acctList.list)):
			self.acctList.list[i].updateHistory()

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
		pass

	"""
		Deposit money into specific accounts or containers based on user input
	"""
	def deposit(self):
		name = input(f"Which account would you like to deposit into?\n{self.printContainers()}\n")
		if self.contList.itemInList(name) or self.acctList.itemInList(name):
			value = float(input(f"How much would you like to deposit into {name}?\n"))
			self.history.append([datetime.now(), value, name])
		else:
			print(f"{name} is not a valid option.")

		#if the name is valid, then a value is added to the container named as so.
		if self.contList.itemInList(name):
			index = self.contList.indexItem(name)
			for i in range(len(self.contList.list)):
				if i == index:
					self.acctList, self.contList = self.contList.list[index].addVal(value, self.acctList, self.contList)
				else:
					self.acctList, self.contList = self.contList.list[i].addVal(0, self.acctList, self.contList)
		elif self.acctList.itemInList(name):
			#adds the value to only the selected item, and then adds 0 to all other lists.
			#adding 0 to all other lists is done to keep the history list of each account/container up to date with the correct length.
			index = self.acctList.indexItem(name)
			for i in range(len(self.acctList.list)):
				if i == index:
					self.acctList.list[index].addVal(value)
				else:
					self.acctList.list[i].addVal(0)


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
			#if the choice wasn't valid, the user is told so, and then prompted to choose again.
			print(f"{chosenAccount} isn't a valid option, please choose again.\n\n")
			return self.chooseAccount()
	
	"""
		asks the user a question, along with a list of possible answer options. 
		Then if the user says something that isn't an option, the question is asked again, otherwise, the user's answer is returned.
	"""
	def question(self, questionStr : str, answerOptions : list = [], clearStart : bool = False) -> str:
		#if the screen should have been cleared upon this function call, then it will ahv ebeen cleared.
		if clearStart:
			os.system("cls")
		
		#prompts the user with the question
		command = input(questionStr)

		#all answers and answer options aren't case sensitive because they are all set to lowercase.
		for i in range(len(answerOptions)):
			answerOptions[i] = str.lower(answerOptions[i])
		
		if command.lower() in answerOptions:
			#answer was a valid option
			return command
		else:
			#answer wasn't a valid option
			print(f"{command} is not a valid option.\n\n")
			#this will never have a True for clearStart because otherwise the user would never see the invalid option line.
			self.question(questionStr, answerOptions, False)


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

			#Adds all of these stats to the list for later printing
			printList.append([date, inputVal, outputVal, account])

		#defines the item values at each point in the history for every item after the default items in itemList.
		for i in range(len(self.history)):
			for j in range(4, len(itemList)):
				itemType, itemIndex = self.getItemInfo(itemList[j])
				if itemType == Account:
					printList[i].append(self.acctList.list[itemIndex].history[i])
				elif itemType == Container:
					printList[i].append(self.contList.list[itemIndex].history[i])

		#prints the name of each item being printed and then a dividing line
		namesStr = ""
		for i in range(len(itemList)):
			namesStr += f"| {itemList[i]} "
		namesStr += "|\n|"
		for i in range(2, len(namesStr) - 2):
			namesStr += "-"
		namesStr += "|"
		print(namesStr)

		#prints all item information divided by bars like such: "|  |"
		for i in range(len(printList)):
			lineStr = ""
			for j in range(len(printList[i])):
				lineStr += f"| {printList[i][j]} "
			lineStr += "|"
			print(lineStr)

	def temp(self):
		print(self.printContainers())
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
		self.autoCreate("Container", "Misc", [["HRT", .5], ["persona", .5]])

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
			self.acctList[acctNames.index(name)].addVal(value)

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

	def display(self):
		printList = [["Date", "Value", "Account"]] #when printed out, value will be split up into input and output
		for i in range(len(self.history)):
			printList.append(self.history[i])

		for i in range(len(printList)):
			printStr = ""
			for j in range(len(printList[i])):
				item = printList[i][j]
				if j > 0:
					if j == 0:
						item = item.date()
					elif j == 1:
						item = f"${item}"
					
				printStr += f"| {item} "
			print(f"{printStr} |")

	def temp(self):
		self.printContainers()
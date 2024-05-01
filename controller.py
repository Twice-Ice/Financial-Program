from moneyClasses import Account, Container
import os

		
class ControllerInstance:
	def __init__(self):
		self.acctList = []
		self.contList = []
		self.contList.append(Container("Total"))

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
			case _:
				print(f"{command} is not a valid option! Type help to see all available commands.")

	def printContainers(self):
		#prints each container as one line, and then the next line as each account with commas in between each instance.
		contStr = ""
		for container in self.contList:
			contStr += (f"{container.name}, ")
		print(f"Containers: {contStr[:len(contStr)-2]}")
		acctStr = ""
		for account in self.acctList:
			acctStr += (f"{account.name}, ")
		print(f"Accounts: {acctStr[:len(acctStr)-2]}") # cuts off the end ", "

	def help(self):
		pass

	def deposit(self):
		print("Which account would you like to deposit into?")
		self.printContainers()
		name = str.lower(input("\n"))
		
		#sets up lists to see if the chosen name is actually valid.
		contNames = []
		for cont in self.contList:
			contNames.append(str.lower(cont.name))
		acctNames = []
		for acct in self.acctList:
			acctNames.append(str.lower(acct.name))

		#if the name is valid, then a value is added to the container named as so.
		if name in contNames:
			self.contList[contNames.index(name)].addVal(input(f"How much would you like to deposit into {name}?\n"))
		elif name in acctNames:
			self.acctList[acctNames.index(name)].addVal(input(f"How much would you like to deposit into {name}?\n"))
		else:
			print(f"{name} is not a valid option")

	def withdraw(self):
		pass

	def create(self):
		command = input("Would you like to create an account or a container?\n")
		match str.lower(command):
			case "account":
				self.acctList.append(Account(input("What would you like to call this account?\n")))
			case "container":
				self.contList.append(Container(input("What would you like to call this container?\n")))
				#need to set up getting the percentages and chosen accounts selectable as options.
			case _:
				print(f"I'm sorry, {command} is not an option.")

	def display(self):
		pass

	def temp(self):
		self.printContainers()
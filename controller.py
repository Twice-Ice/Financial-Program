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
			case "edit":
				pass
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
			self.acctList = self.contList[contNames.index(name)].addVal(input(f"How much would you like to deposit into {name}?\n"), self.acctList)
		elif name in acctNames:
			self.acctList[acctNames.index(name)].addVal(input(f"How much would you like to deposit into {name}?\n"))
		else:
			print(f"{name} is not a valid option")

	def withdraw(self):
		pass

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
		pass

	def temp(self):
		self.printContainers()
from moneyClasses import Account, Container

def printContainers(containerList):
	returnStr = "["
	for container in containerList:
		if type(container) == Account:
			returnStr += f"{container.name}, "
		elif type(container) == Container:
			returnStr += f"{printContainers(container)}"
	return returnStr
		
class ControllerInstance:
	def __init__(self):
		self.containerList = [Container("Total")]
		self.containerList[0].newAccount(Account("testAccount!"))

	def update(self):
		command = input("What would you like to do?\n")
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

	def help(self):
		pass

	def deposit(self):
		print("Which account would you like to deposit into?")
		printContainers(self.containerList)

	def withdraw(self):
		pass

	def create(self):
		pass

	def display(self):
		pass

	def temp(self):
		print(printContainers(self.containerList))
from moneyClasses import Account, Container

def printContainers(item):
	returnStr = ""
	if type(item) == Account:
		returnStr += f"{item.name}, "
	elif type(item) == Container:
		# returnStr += "["
		for container in item.containerList:
			returnStr += f"{printContainers(container)}"
		# returnStr += "]"
	
	return f"{returnStr}"
		
class ControllerInstance:
	def __init__(self):
		self.total = Container("Total")
		self.total.newAccount(Account("testAccount!"))
		self.total.newAccount(Account("testAccount!!"))
		self.total.newAccount(Account("testAccount!!!!"))

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
		print(f"{printContainers(self.total)}\n")
		accountName = input()
		nameList = []
		for container in self.total.containerList:
			nameList.append(container.name)
		try:
			self.total.containerList[nameList.index(accountName)].changeVal(input("How much would you like to deposit?"))
		except:
			print(f"{accountName} is not a valid option")

	def withdraw(self):
		pass

	def create(self):
		pass

	def display(self):
		pass

	def temp(self):
		print(printContainers(self.total))
from moneyClasses import Account, Container

class controllerInstance:
	def __init__(self):
		self.containerList = [Account("Total")]

	def update(self):
		command = input("What would you like to do?")
		match str.lower(command):
			case "help":
				help()
			case "deposit":
				pass
			case "withdraw":
				pass
			case "create":
				pass
			case "display":
				pass
			case _:
				print(f"{command} is not a valid option! Type help to see all available commands.")

	def help():
		pass
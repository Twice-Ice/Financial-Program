import os

class Account:
	def __init__(self, name : str = "None"):
		self.name = name
		self.val = 0
		self.percent = 1

	def setPercentage(self, percent):
		self.percent = percent/100

		# os.system("cls")
		# percent = input(f"Please input the percentage (0 - 100) for your {self.name} account:\n")
		# try:
		# 	self.percent = float(percent)/100
		# except:
		# 	os.system("cls")
		# 	print(f"{percent} is not a valid value, please input numbers only.")
		# 	self.setPercentage()

	def changeVal(self, change):
		self.val += change

	def printVal(self):
		return str(self.val)
	
class Container:
	def __init__(self, name : str = "None", containerList : list = []):
		self.name = name
		self.containerList = containerList #since accounts and containers should be treated very similarly, they are held within the same container list

	def addVal(self, change):
		if change >= 0:
			for account in self.accountsList:
				account.changeVal(change*account.percent)
		else:
			raise ValueError(f"Change, ({change}), must be larger than 0. Money can only be removed form accounts individually.")
		
	def printVal(self):
		totalVal = 0
		for account in self.accountsList:
			totalVal += account.val
		return str(totalVal)

	def getPercent(self):
		totalPercent = 0
		for account in self.accountsList:
			totalPercent += account.percent
		return totalPercent
	
	def newAccount(self, account):
		self.containerList.append(account)
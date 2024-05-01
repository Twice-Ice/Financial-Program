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

	def addVal(self, change):
		self.val += int(change)

	def printVal(self):
		return str(self.val)
	
class Container:
	def __init__(self, name : str = "None", itemList : list = []):
		self.name = name
		self.itemList = itemList #should contain a 2d list of [name, percent]

	def addVal(self, change, accts : list):
		change = int(change)
		# if the change isn't negative
		if change >= 0:
			#define all the names of accounts for later use
			namesList = []
			for account in accts:
				namesList.append(account.name)

			#checks all of the names in this container's list of names + percentages.
			for i in range(len(self.itemList)):
				name = self.itemList[i][0]
				percent = float(self.itemList[i][1])
				if name in namesList:
					#if the name is in the list (all of these names should be), then the account there 
	 				#should have it's value changed based on change and the account's percentage in this container.
					accts[namesList.index(name)].addVal(change * percent)
				else:
					#just in case
					raise NameError(f"{name} isn't in the accounts list! :(")

			#returns accts so that the values are all updated
			return accts
		else:
			raise ValueError(f"Change, ({change}), must be larger than 0. Money can only be removed form accounts individually.")
		
	#need a function to edit self.acctList
		
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
		self.itemList.append(account)
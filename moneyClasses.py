import os

"""
	An advanced list class for use cases within only this program  
"""
class ItemList:
	def __init__(self):
		self.list = []

	"""
		Returns a list of all the item names within the ItemList.list variable.

		Can return the name list as a lowercase or  upper case based on the variables set upon calling the function.
	"""
	def getNameList(self, lower : bool = False, upper : bool = False) -> list:
		#defines the base list
		nameList = []
		for i in range(len(self.list)):
			nameList.append(self.list[i].name)

		#lower/upper
		if lower:
			for i in range(len(nameList)):
				nameList[i] = nameList[i].lower()
		elif upper:
			for i in range(len(nameList)):
				nameList[i] = nameList[i].upper()

		return nameList
	
	"""
		Adds a new item to the list.
	"""
	def newItem(self, item):
		self.list.append(item)

	"""
		Checks if an item is in the list and returns true or false if that is the case.

		All itemNames will be uniformally understood without any worry about upper/lowercaseing.
	"""
	def itemInList(self, itemName):
		nameList = self.getNameList(lower = True)

		if itemName.lower() in nameList:
			return True
		else:
			return False
	
	"""
		returns if an item is in the lists, and an int index of where in self.list, "itemName" is located.
	"""
	def indexItem(self, itemName):
		nameList = self.getNameList(lower = True)
		if self.itemInList(itemName):
			return nameList.index(itemName.lower())
		else:
			raise NameError("ayo for some reason this is causing a bug. Last time I worked on this, there was a workaround by returning a bool as well, but that system sucked so I got rid of it. GL with the bug though, future me.")

class Account:
	def __init__(self, name : str = "None", historyLen : int = 0):
		self.name = name
		self.val = 0
		self.percent = 1
		self.history = []
		for i in range(historyLen):
			self.addVal(0)

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

	def addVal(self, change : float):
		self.val += change
		self.history.append(self.val)

	def printVal(self):
		return str(self.val)
	
class Container:
	def __init__(self, name : str = "None"):
		self.name = name
		self.itemList = [] #should contain a 2d list of [name, percent]
		self.history = []

	#adds a value to each account contained within the container, based on the container's itemList percentages.
	def addVal(self, change : float, accts : ItemList, conts : ItemList) -> tuple[ItemList, ItemList]: #accts is where all of the accounts are stored, so that they can be edited and returned.
		change = float(change)
		#applies the change to the history
		if len(self.history) > 0:
			self.history.append(self.history[len(self.history)-1] + change)
		else: #if the history doesn't already have anything in it's list, then change is just applied to start the chain of events.
			self.history.append(change)
		#if the change isn't negative
		if change >= 0:
			#checks all of the names in this container's list of names + percentages.
			for i in range(len(self.itemList)):
				name = self.itemList[i][0]
				percent = float(self.itemList[i][1])
				if accts.itemInList(name):
					#if the name is in the list (all of these names should be), then the account there 
	 				#should have it's value changed based on change and the account's percentage in this container.
					accts.list[accts.indexItem(name)].addVal(change * percent)
				elif conts.itemInList(name):
					conts.list[conts.indexItem(name)].addVal(change * percent, accts, conts)
				else:
					#just in case
					raise NameError(f"{name} isn't in either account or container list! :(")

			#returns accts so that the values are all updated
			return accts, conts
		else:
			raise ValueError(f"Change, ({change}), must be larger than 0. Money can only be removed form accounts individually.")
		
	"""
		updates the history values for the container, value should be the controller history for the last entry.

		for some reason, putting the update here really messed things up because detecting what the change was by calculating it made the system not work very well.
		now the history is updated when a value is changed for the container class. This is not true for the Account class, where it's values are updated later to avoid cases where the value aren't detected properly.
	"""
	def updateHistory(self, contList : ItemList, acctList : ItemList, historyIndex : int = -1):
		pass
		# self.history.append(self.getSum(contList, acctList, historyIndex))

	#need a function to edit self.acctList
	
	"""
		gets the sum value of a container by adding up all the values at a specific index in the history list.
	"""
	def getSum(self, contList :ItemList, acctList :ItemList, historyIndex = -1):
		totalVal = 0
		
		#loops through each item in the container's item list
		for item in self.itemList:
			if contList.itemInList(item[0]):
				#if the item is a container, the sum of that container's items is added to the total.
				totalVal += contList.list[contList.indexItem(item[0])].getSum(contList, acctList, historyIndex)
			elif acctList.itemInList(item[0]):
				#if the item is an account, the item's value at history[historyIndex] is added to the total Val.
				#as eventually all container should only contain accounts, then it's ok to resolve all values in this half of the if statment.
				totalVal += acctList.list[acctList.indexItem(item[0])].history[historyIndex]

		return totalVal
	
	def getPercent(self):
		totalPercent = 0
		for account in self.accountsList:
			totalPercent += account.percent
		return totalPercent
	
	def newAccount(self, account):
		self.itemList.append(account)
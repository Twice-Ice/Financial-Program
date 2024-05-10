import os
import globals as gb

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

"""
	A class to track instances of history within history lists. This is so that variables can be called directly instead of spots in lists.
"""
class HistoryInstance:
	def __init__(self, val : float, instance : int, parent: str):
		self.val = val
		self.instance = instance
		self.parent = parent

"""
	A class to hold the history of an item instead of just a list messily put together.
"""
class HistoryList:
	def __init__(self):
		self.list = [] #[[instance num, where it came from], [etc.]]

	"""
		adds a new history instance to the object's list, with the value, instantiation group, and parent of the object.
	"""
	def addInstance(self, val : float, instance : int, parent : str = "default"):
		self.list.append(HistoryInstance(val, instance, parent))

	"""
		gets the sum value of all history instances at a certain point in time/instance (the variable)
	"""
	def getSum(self, instance : int):
		sum = 0
		for case in self.list:
			if case.instance <= instance:
				sum += case.val

		return sum
	
	"""
		Returns a list of all of this HistoryList's stats for viewing purposes within the debugger.

		*This is not an end user function*
	"""
	def histInfo(self, type):
		returnList = []
		match type:
			case "val":
				for inst in self.list:
					returnList.append(inst.val)
			case "instance":
				for inst in self.list:
					returnList.append(inst.instance)
			case "parent":
				for inst in self.list:
					returnList.append(inst.parent)
			case _:
				raise NameError(f"{type} is not a valid option.\nThe valid options are: (val, instance, parent)")
		
		return returnList

class Account:
	def __init__(self, name : str = "None", historyLen : int = 0):

		self.name = name
		self.val = 0
		self.percent = 1
		self.history = HistoryList()
		for i in range(historyLen):
			self.addVal(0)

	def addVal(self, change : float, parent : str = "default"):
		self.val += change
		self.history.addInstance(change, gb.COM_INSTANCE, parent)

	def getSum(self, instance : int):
		return self.history.getSum(instance)

	def printVal(self):
		return str(self.val)
	
class Container:
	def __init__(self, name : str = "None"):
		self.name = name
		self.itemList = [] #should contain a 2d list of [name, percent]
		self.history = HistoryList()

	"""
		adds a value to each account contained within the container, based on the container's itemList percentages.
	"""
	def addVal(self, change : float, accts : ItemList, conts : ItemList) -> tuple[ItemList, ItemList]: #accts is where all of the accounts are stored, so that they can be edited and returned.
		change = float(change)
		self.history.addInstance(change, gb.COM_INSTANCE)
		#checks all of the names in this container's list of names + percentages.
		for i in range(len(self.itemList)):
			name = self.itemList[i][0]
			percent = float(self.itemList[i][1])
			if accts.itemInList(name):
				#if the name is in the list (all of these names should be), then the account there 
				#should have it's value changed based on change and the account's percentage in this container.
				accts.list[accts.indexItem(name)].addVal(change * percent, self.name)
			elif conts.itemInList(name):
				conts.list[conts.indexItem(name)].addVal(change * percent, accts, conts)
			else:
				#just in case
				raise NameError(f"{name} isn't in either account or container list! :(")

		#returns accts so that the values are all updated
		return accts, conts

	#need a function to edit self.acctList
	
	"""
		gets the sum value of a container by adding up all the values at a specific index in the history list.
	"""
	def getSum(self, contList, acctList, instance):
		sum = 0
		for i in range(0, instance):
			sum += self.getSumOverInstance(contList, acctList, i)
		return sum

	def getSumOverInstance(self, contList, acctList, instance):
		sum = 0
		#loops through the lists and if the instance is the selected instance, and the parent is the same as self.name, then it's value is added to the sum for later use.
		for i in range(len(contList.list)):
			cont = contList.list[i].history.list[instance]
			if cont.instance == instance and cont.parent == self.name:
				sum += cont.val
				
		for i in range(len(acctList.list)):
			acct = acctList.list[i].history.list[instance]
			if acct.instance == instance and acct.parent == self.name:
				sum += acct.val

		return sum		
	
	def getPercent(self):
		totalPercent = 0
		for account in self.accountsList:
			totalPercent += account.percent
		return totalPercent
	
	def newAccount(self, account):
		self.itemList.append(account)
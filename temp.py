# import os
# import launchFileInit
# import globals as gb
# from controller import ControllerInstance
# from datetime import datetime


# controller = ControllerInstance()

# # DONT DELETE, EITHER COMMENT THIS OUT OR MAKE A NEW FILE, OR ACTUALLY IMPLEMENT THE SHIT IF YOU HAVE THE MOTIVATION.
# # it's a really cool skeleton of a function to estimate money spent on groceries and or other foods given a few keywords.

# comparisonDate = datetime(2025, 8, 28)
# today = datetime.now()

# foodList = []
# for instance in controller.history:
#     name : str = instance[2]
#     name = name.lower()
#     date : datetime = instance[1]
#     dateDifference = date-comparisonDate
#     if dateDifference.days >= 0:
#         if name.find("grocer") != -1 or name.find("snack") != -1:
#             foodList.append(instance)

# totalCost = 0
# for instance in foodList:
#     totalCost += instance[3]

# print(len(foodList))
# print(f"total cost: {totalCost}")
# print(f"total days: {(today-comparisonDate).days}")
# print(f"cost per day: {totalCost/(today-comparisonDate).days}")
# print(f"goal cost per day: {150/(365.25/12)}")
# print(f"avg cost per month: {totalCost/(today-comparisonDate).days*(365.25/12)}")
# print(f"avg cost per year: {totalCost/(today-comparisonDate).days*(365.25)}")

X = ["a", "b", "a", "b", "c", "a", "b", "b", "b", "cats"]

removalIndexes = []
for i in range(len(X)):
    print(X.index(X[i]), i == X.index(X[i]))
    if i != X.index(X[i]):
        removalIndexes.append(i)

removalIndexes.sort()
while len(removalIndexes) != 0:
    index = removalIndexes.pop()
    X = X[0:index] + X[index+1:len(X)]

print(removalIndexes)

print(X)
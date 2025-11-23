import os
import launchFileInit
import globals as gb
from controller import ControllerInstance
from datetime import datetime


controller = ControllerInstance()

comparisonDate = datetime(2025, 8, 28)
today = datetime.now()

foodList = []
for instance in controller.history:
    name : str = instance[2]
    name = name.lower()
    date : datetime = instance[1]
    dateDifference = date-comparisonDate
    if dateDifference.days >= 0:
        if name.find("grocer") != -1 or name.find("snack") != -1:
            foodList.append(instance)

totalCost = 0
for instance in foodList:
    totalCost += instance[3]

print(len(foodList))
print(f"total cost: {totalCost}")
print(f"total days: {(today-comparisonDate).days}")
print(f"cost per day: {totalCost/(today-comparisonDate).days}")
print(f"goal cost per day: {150/(365.25/12)}")
print(f"avg cost per month: {totalCost/(today-comparisonDate).days*(365.25/12)}")
print(f"avg cost per year: {totalCost/(today-comparisonDate).days*(365.25)}")
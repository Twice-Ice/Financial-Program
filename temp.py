import os
import launchFileInit
import globals as gb
from controller import ControllerInstance
from datetime import datetime


controller = ControllerInstance()

# DONT DELETE, EITHER COMMENT THIS OUT OR MAKE A NEW FILE, OR ACTUALLY IMPLEMENT THE SHIT IF YOU HAVE THE MOTIVATION.
# it's a really cool skeleton of a function to estimate money spent on groceries and or other foods given a few keywords.

comparisonDate = datetime(2025, 9, 27)
today = datetime.now()

inList = []
for instance in controller.history:
    date : datetime = instance[1]
    dateDifference = date-comparisonDate
    if dateDifference.days >= 0:
        if instance[4].lower() == "college" and instance[3] < 0:
            inList.append(instance)

totalCost = 0
for instance in inList:
    totalCost += instance[3]

print(len(inList))
print(f"total cost: {totalCost}")
print(f"total days: {(today-comparisonDate).days}")
print(f"cost per day: {totalCost/(today-comparisonDate).days}")
print(f"goal cost per day: {150/(365.25/12)}")
print(f"avg cost per month: {totalCost/(today-comparisonDate).days*(365.25/12)}")
print(f"avg cost per year: {totalCost/(today-comparisonDate).days*(365.25)}")
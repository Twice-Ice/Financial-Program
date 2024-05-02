import os
from datetime import datetime
from moneyClasses import Account
from controller import ControllerInstance

doExit = False

controller = ControllerInstance()
time = datetime.now()
print(time.date(), type(time))

list = [i for i in range(10)]

while not doExit:
	controller.update()
import os
from moneyClasses import Account
from controller import ControllerInstance

doExit = False

controller = ControllerInstance()

while not doExit:
	controller.update()
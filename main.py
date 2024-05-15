import os
import launchFileInit
from controller import ControllerInstance

doExit = False

controller = ControllerInstance()

os.system("cls")

while not doExit:
	controller.update()
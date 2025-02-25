import os
import launchFileInit
import globals as gb
from controller import ControllerInstance

os.system("cls")
controller = ControllerInstance()

while not gb.DOEXIT:
	controller.update()
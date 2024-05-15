import os
import launchFileInit
import globals as gb
from controller import ControllerInstance


controller = ControllerInstance()

os.system("cls")

while not gb.DOEXIT:
	controller.update()
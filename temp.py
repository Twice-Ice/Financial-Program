import os
import launchFileInit
import globals as gb
from controller import ControllerInstance
import datetime


controller = ControllerInstance()

for i in range(len(controller.history)):
    controller.history[i][0] = i+1

controller.save()
import os
import launchFileInit
import globals as gb
from controller import ControllerInstance
import datetime


controller = ControllerInstance()

i = input("a, A, or b : ")
match i:
    case "a" or "A":
        print("aahhhh")
    case "b":
        print("bhhh")
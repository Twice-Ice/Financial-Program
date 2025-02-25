from controller import ControllerInstance
import tkinter as tk
import tksheet

controller = ControllerInstance()

# print(controller.history[0])

h = controller.history

# h = [["A"], [1]]

root = tk.Tk()
root.title("Test Table")

sheet = tksheet.Sheet(root, data=h)
sheet.pack(expand=True, fill="both")

root.mainloop()
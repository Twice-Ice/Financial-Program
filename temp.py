# import calendar
# from datetime import datetime as dt

# while True:
# 	time = calendar.timegm(dt.now().timetuple())
# 	print(time, f"{hex(time)[2:]}{hex(int(dt.now().strftime("%f")[-3:]))[2:]}")
# 	# time = int(dt.now().strftime("%d%m%y%H%M%S%f"))
# 	# print(hex(time)[2:])

dictionary = {
	"ABC" : "it worked"
}

print(dictionary["abc"])
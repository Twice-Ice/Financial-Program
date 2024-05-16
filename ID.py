import calendar
from datetime import datetime as dt

# hexLen = 2

# oldMsg = ""
# while True:
# 	time = calendar.timegm(dt.now().timetuple())
# 	printMsg = f"{int(dt.now().strftime("%y") + str(calendar.timegm(dt.now().timetuple()))[4:])}, "
# 	year = f"{dt.now().strftime("%y")}"
# 	epoch = f"{hex(int(time))[2:]}"
# 	# shortEpoch = hex(int(year + str(calendar.timegm(dt.now().timetuple()))[4:]))[2:]

# 	shortEpoch = hex(int(dt.now().strftime("%y") + str(calendar.timegm(dt.now().timetuple()))[4:]))[2:]

# 	microseconds = f"{hex(int(dt.now().strftime("%f")))[-hexLen:]}"
# 	printMsg += f"{shortEpoch}{microseconds}"

# 	if oldMsg != printMsg:
# 		print(printMsg)

# 	oldMsg = printMsg


#credit to chat GPT for this
#it's a id generator that can be any base depending on the symbols that you give the init function.
class SequentialIDGenerator:
	def __init__(self, base_symbols):
		self.base_symbols = base_symbols
		self.base = len(base_symbols)

	def generate_id(self, number):
		if number == 0:
			return self.base_symbols[0]

		result = ''
		while number > 0:
			number, remainder = divmod(number, self.base)
			result = self.base_symbols[remainder] + result

		return result

# Example usage
oldMsg = ""
while True:
	base_symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_+=!@#$%^&*<>~'
	generator = SequentialIDGenerator(base_symbols)

	"""
	YY = (20)24
	EP = Epoch
	MS = microsecond
	
	id uncompressed:
		YY+EP+MS

	EP has the millions and billions cut off bcs they mostly just represent the year, and these values are replaced by YY so that the year isn't completely lost.
	MS is limited to the last 2 digits bcs honestly who tf is gonna be inputing new deposits within even the same second???
	"""

	uncompressedMsg = int(dt.now().strftime("%y") + str(calendar.timegm(dt.now().timetuple()))[-6:] + dt.now().strftime("%f")[-2:])
	compressedMsg   = generator.generate_id(uncompressedMsg)

	if oldMsg != compressedMsg:
		print(uncompressedMsg, compressedMsg)

	oldMsg = compressedMsg
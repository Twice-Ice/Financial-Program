import calendar
from datetime import datetime as dt
from globals import ID_COMPRESSOR_SYMBOLS

#credit to chat GPT for this
#it's a id generator that can be any base depending on the symbols that you give the init function.
class SequentialIDGenerator:
	def __init__(self, base_symbols):
		self.base_symbols = base_symbols
		self.base = len(base_symbols)

	def generateID(self, number):
		if number == 0:
			return self.base_symbols[0]

		result = ''
		while number > 0:
			number, remainder = divmod(number, self.base)
			result = self.base_symbols[remainder] + result

		return result
	
class IDGenerator(SequentialIDGenerator):
	def __init__(self):
		super().__init__(ID_COMPRESSOR_SYMBOLS)
	
	def generateID(self, time : dt = dt.now()):
		"""
		YY = (20)24
		EP = Epoch
		MS = microsecond
		
		id uncompressed:
			YY+EP+MS

		EP has the millions and billions cut off bcs they mostly just represent the year, and these values are replaced by YY so that the year isn't completely lost.
		MS is limited to the last 2 digits bcs honestly who tf is gonna be inputing new deposits within even the same second???
		"""
		number = int(time.strftime("%y") + str(calendar.timegm(time.timetuple()))[-6:] + time.strftime("%f")[-2:])
		return super().generateID(number)
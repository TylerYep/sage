import operator

class Counter:

	def __init__(self):
		self.data = {}

	def increment(self, key):
		if not key in self.data:
			self.data[key] = 0
		self.data[key] += 1

	def increase(self, key, value):
		if not key in self.data:
			self.data[key] = 0
		self.data[key] += value

	def getCount(self, key):
		if not key in self.data:
			return 0
		return self.data[key]

	def getSortedKeys(self):
		sortedKeyValues = sorted(self.data.items(), key=operator.itemgetter(1), reverse=True)
		sortedKeys = [x[0] for x in sortedKeyValues]
		return sortedKeys


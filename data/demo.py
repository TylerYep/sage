import matplotlib
matplotlib.use('MACOSX')
import matplotlib.pyplot as plt
import numpy as np

# dataloader is a helper utility you may want to use
import dataLoader

# if you want to load the pickle file, you need *this* class
import models.tree as tree

# This demo loads data from p4, a problem on the code.org unit
def main():
	# Map from sourceId -> abstract syntax tree (see models.tree)
	# print('Loading level sources...')
	# astMap = dataLoader.loadLevelSources('p4')

	# Map from sourceId -> number of times this source is submitted
	print('Loading counts...')
	countMap = dataLoader.loadCountMap('p4')

	# Map from userId -> list of tuples (sourceId, timestamp)
	# print('Loading activities...')
	# activities = dataLoader.loadActivities('p4')

	# Print the size of the data
	# print('#ast', len(astMap))
	# print('#students', len(activities))

	# for code in countMap:
	# 	print(code, countMap[code])
	# 	ast = astMap[code]
	rank = [j+1 for j in range(len(countMap))]
	probs = sorted(countMap.values(), reverse=True)
	plt.scatter(rank, probs, s=0.7)
	plt.yscale('log')
	plt.xscale('log')
	plt.title('Distribution of Solutions')
	plt.xlabel('Rank Order (log)')
	plt.ylabel('Probability Mass (log)')
	plt.show()

if __name__ == '__main__':
	main()
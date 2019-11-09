import os
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

files = ['activities-4', 'countMap-4', 'levelIdMap-4', 'sources-4', 'sourcesSmall-4']


def main():
	fileName = 'sources-9'
	# attempts = []
	with open(fileName + '.csv', 'w', newline='') as csvfile:

		wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

		studentCodes = {}
		data = pickle.load(open('p9/' + fileName + '.pickle', 'rb')) # countMap
		# print(type(data))
		for key in data:
			studentCodes[key] = str(data[key])
			# attempts.append(len(data[key]))
			wr.writerow([key, data[key]])
	# plt.hist(attempts, normed=True, bins=30)
	# plt.savefig(fileName + '.png')
		# print(studentCodes)

def makeLifeEasier():
	fileName = 'sources-1'
	# attempts = []
	studentCodes = {}
	data = pickle.load(open('data/p1/' + fileName + '.pickle', 'rb')) # countMap
	for key in data:
		studentCodes[key] = str(data[key])

	fileName = 'activities-1'
	studentAttempts = {}
	data = pickle.load(open('data/p1/' + fileName + '.pickle', 'rb')) # countMap
	studentCount = 0
	start = 0
	end = 100
	file1 = open("p1_first_100.txt","a")
	for key in data:
		attempts = []
		for d in data[key]:
			attempts.append(studentCodes[d[0]])
		studentAttempts[studentCount] = attempts
		if studentCount >= start and studentCount <= end:
			file1.write('\n\n\n\nstudent' + str(studentCount))
			for a in attempts:
				file1.write('\n' + a)
			file1.write('\n\n\n\n')
		studentCount += 1

	# with open('p1_student_attempts_large.csv', 'w', newline='') as csvfile:
	# 	wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
	# 	for key in studentAttempts:
	# 		wr.writerow([key, studentAttempts[key]])

def main2():
	data = pickle.load(open('countMap-4.pickle', 'rb')) # countMap
	counter = 0
	bigSum = 0
	counts = np.array([[0, 0] for _ in range(len(data))])
	for key, value in sorted(data.iteritems()):
		assert counter == key
		counts[key][0] = key
		counts[key][1] = value
		bigSum += value
		counter += 1
	x = np.log(counts[:, 0])
	y = np.log(counts[:, 1])
	plt.scatter(x, y)
	plt.title('Distribution of Solutions')
	plt.xlabel('Rank Order (log scale)')
	plt.ylabel('Probability Mass (log scale)')
	plt.savefig('q1.png')
	print('number of simulations:', bigSum)

def main3():
	data = pickle.load(open('p1/countMap-1.pickle', 'rb')) # countMap
	counter = 0
	bigSum = 0
	for key in data:
		assert counter == key
		bigSum += data[key]
		counter += 1
	print('number of simulations:', bigSum)

if __name__ == '__main__':
	# main()
	# main2()
	# main3()
	makeLifeEasier()

import os
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import csv

sys.path.append(os.path.join(os.path.dirname(_file_), '..'))

files = ['activities-4', 'countMap-4', 'levelIdMap-4', 'sources-4', 'sourcesSmall-4']

def main():
	with open('student_codes.csv', 'w', newline='') as csvfile:
		wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		studentCodes = {}
		data = pickle.load(open('p1/sourcesSmall-1.pickle', 'rb')) # countMap
		for key in data:
			studentCodes[key] = str(data[key])
			wr.writerow([key, data[key]])

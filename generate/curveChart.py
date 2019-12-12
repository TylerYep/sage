import json
from tree_encoder import TreeDecoder
import matplotlib
matplotlib.use('MACOSX')
import matplotlib.pyplot as plt
import numpy as np

def main():
	problems = [i for i in range(1, 11)]
	for problem in problems:
		print(f"Loading activity map for Problem {problem}")
		with open(f'../data/p{problem}/activities-{problem}.json') as sub_file:
			sub_data = json.load(sub_file)
		plt.clf()
		values = [i for i in map(len, sub_data.values()) if i > 0]
		plt.hist(values, bins=40, range=(0,40))
		plt.title(f'Distibution of # of Submissions per student for Problem {problem}')
		plt.xlabel(f'Number of Submissions')
		plt.ylabel('Number of Students')
		plt.savefig(f'plots/sub-p{problem}-curve.png')
		
def counts():
	problems = [i for i in range(1, 11)]
	for problem in problems:
		print(f"Loading count map for Problem {problem}")
		with open(f'../data/p{problem}/countMap-{problem}.json') as count_file:
			count_data = json.load(count_file)
		plt.clf()
		values = list(count_data.values())
		plt.plot(np.log(list(range(len(count_data)))), np.log(values))
		plt.title(f'Distibution of Submissions for Problem {problem}')
		plt.xlabel(f'Log Ranking (out of {len(values)} unique submissions)')
		plt.ylabel('Log Frequency')
		plt.savefig(f'plots/p{problem}-curve.png')

if __name__ == '__main__':
	main()
import pickle
from tree_encoder import TreeDecoder
import matplotlib.pyplot as plt
import numpy as np

def main():
	start = 1 # should be 1
	end = 10 # should be 10
	problems = [i for i in range(start, end + 1)]
	for problem in problems:
		print(f"Loading count map for Problem {problem}")
		with open(f'data/p{problem}/countMap-{problem}.pickle', 'rb') as count_file:
			plt.clf()
			count_data = pickle.load(count_file)
			keys = np.array(list(count_data.keys()))
			values = np.array(list(count_data.values()))
			(keys,values) = zip(*count_data.items())
			plt.plot(keys, np.log(values))
			plt.title(f'Curve Chart for Problem {problem}')
			plt.xlabel(f'Ranking of Submission (out of {len(values)} unique submissions)')
			plt.ylabel('Log of Frequency of Submission')
			plt.savefig(f'data/p{problem}-curve.png')

if __name__ == '__main__':
	main()
from typing import List, Dict, Tuple
import matplotlib
matplotlib.use('MACOSX')
import matplotlib.pyplot as plt
import os
import sys
import json
import random
import pickle
import ideaToText
import argparse
from pprint import pprint
from codeDotOrg import autoFormat, remove_whitespace
from tree_encoder import TreeDecoder

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('problem', type=int, help='problem number')
	parser.add_argument('--all', '-a', help='sample all problems', action='store_true', default=False)
	args = parser.parse_args()
	if args.all:
		print("Sampling all problems...")
		for i in (1,2,3,4):
			print("Sampling for problem", i)
			sample(i)
	elif args.problem == 0:
		print("Please specify a problem number or use -a to sample all problems.")
	else:
		print("Sampling for problem", args.problem)
		sample(args.problem)


def createDataList(problem, source_data_contains, count_data_map):
	GRAMMAR_PATH = f'grammars/p{problem}'
	MAX = 100000
	REPETITIONS = 3

	uniqueSubs = {}
	num_sampled, percent_complete, useless_counter = 0, 0, 0
	data = []

	prev = None
	no_new_counter = REPETITIONS
	sample_count_map = {}

	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	while no_new_counter != 0 and num_sampled < MAX:
		if num_sampled % 1000 == 0:
			print('Iter:', num_sampled, 'Unique:', len(uniqueSubs))
			if len(uniqueSubs) == prev:
				no_new_counter -= 1
			else:
				no_new_counter = REPETITIONS
				prev = len(uniqueSubs)

		sample = sampler.singleSample()

		# Save data
		new_data = {}
		new_data['code'] = sample['text']
		new_data['label'] = sample['rubric']
		data.append(new_data)

		text = remove_whitespace(sample['text'])
		if text not in sample_count_map:
			sample_count_map[text] = 0
		sample_count_map[text] += 1

		if text not in uniqueSubs:
			uniqueSubs[text] = sample['rubric']
			if text in source_data_contains:
				percent_complete += count_data_map[text]
				source_data_contains.remove(text)
			else:
				useless_counter += 1
		num_sampled += 1

	with open(f'generated/data-{problem}.pkl', 'wb') as f:
		pickle.dump(data, f)

	print('Out-of-distribution Datapoints: ',
		  useless_counter, '/', len(uniqueSubs),
		  f' ({len(count_data_map)-len(source_data_contains)} in-distribution were found)')

	print('Percent of Original Data Covered: ',
		  f'{percent_complete} / {sum(count_data_map.values())} = ',
		  float(percent_complete) / sum(count_data_map.values()), '\n')

	leftover = [(source, count_data_map[source]) for source in source_data_contains]
	pprint(sorted(leftover, key=lambda k: k[1], reverse=True)[:50])
	return uniqueSubs


def sample(problem):
	with open(f'../data/p{problem}/sources-{problem}.json') as source_file:
		source_data = json.load(source_file, cls=TreeDecoder)
	with open(f'../data/p{problem}/countMap-{problem}.json') as count_file:
		count_data = json.load(count_file, cls=TreeDecoder)
	count_data_map = {}
	source_data_contains = set() # programs
	for key in source_data:
		expr = remove_whitespace(autoFormat(source_data[key]))
		if expr not in source_data_contains:
			source_data_contains.add(expr)
			count_data_map[expr] = count_data[key]

	uniqueSubs = createDataList(problem,
								source_data_contains,
								count_data_map)
	with open(f'generated/uniqueSubs-{problem}.json', 'w') as f:
		json.dump(uniqueSubs, f, indent=2)


def compute_l1_dist(sample_count_map, count_data_map):
	l1_distance = 0
	arr1, arr2 = [], []
	for key, v1 in sorted(sample_count_map.items(), key=lambda x: x[1], reverse=True):
		v2 = count_data_map[key] if key in count_data_map else 0
		arr1.append(v1)
		arr2.append(v2)
		l1_distance += abs(v1 - v2)
	print('Distribution Matching (L1 Distance):', l1_distance)
	x = range(len(arr1))
	plt.yscale('log')
	plt.plot(x, arr2)
	plt.plot(x, arr1)
	# plt.fill_between(x, 0, arr2)
	plt.show()


if __name__ == '__main__':
	main()

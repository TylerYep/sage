from typing import List, Dict, Tuple
import os
import sys
import json
import random
import pickle
import ideaToText
from codeDotOrg import autoFormat
from tree_encoder import TreeDecoder

CURR_PROBLEM = 1
GRAMMAR_PATH = f'grammars/p{CURR_PROBLEM}'
NUM_SAMPLES = 4400

def createDataList(sampler, source_data_contains, count_data_map, n):
	uniqueSubs, counts = {}, {}
	num_sampled = 0
	no_match, match = 0, 0
	percent_complete = 0
	data = []

	while len(uniqueSubs) < n:
		if num_sampled % 1000 == 0:
			print(num_sampled, len(uniqueSubs))
		sample = sampler.singleSample()
		new_data = {}
		new_data['code'] = sample['text']
		new_data['label'] = sample['rubric']
		data.append(new_data)

		text = sample['text'].replace('\n', '').replace(' ', '')
		if text not in uniqueSubs:
			uniqueSubs[text] = sample['rubric']
			if text in source_data_contains:
				percent_complete += count_data_map[text]
		if text in source_data_contains:
			match += 1
		else:
			no_match += 1
			if text not in counts:
				counts[text] = 0
			counts[text] += 1

		num_sampled += 1

	with open('generated/data.pkl', 'wb') as f:
		pickle.dump(data, f)
	print('Number of submission overlaps:', match, '/', num_sampled)
	print('Number of useless datapoints (not in source):', no_match, '/', num_sampled)
	print('Percent Complete: ',
		  f'{percent_complete} / {sum(count_data_map.values())}',
		  float(percent_complete) / sum(count_data_map.values()))
	print()
	return uniqueSubs, counts

def sample(problem=CURR_PROBLEM):
	with open(f'../data/p{problem}/sources-{problem}.json') as source_file:
		source_data = json.load(source_file, cls=TreeDecoder)
	with open(f'../data/p{problem}/countMap-{problem}.json') as count_file:
		count_data = json.load(count_file, cls=TreeDecoder)
	count_data_map = {}
	source_data_contains = set() # program
	for key in source_data:
		expr = autoFormat(source_data[key]).replace('\n', '').replace(' ', '')
		source_data_contains.add(expr)
		count_data_map[expr] = count_data[key]

	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	uniqueSubs, counts = createDataList(sampler, source_data_contains, count_data_map, NUM_SAMPLES) # program -> rubric_item
	with open(f'generated/uniqueSubs-{problem}.json', 'w') as f:
		json.dump(uniqueSubs, f, indent=2)
	with open(f'generated/counts-{problem}.json', 'w') as f:
		json.dump(counts, f, indent=2)
	print(sorted(counts.items(), key=lambda k: k[1], reverse=True)[:500])

if __name__ == '__main__':
	sample()

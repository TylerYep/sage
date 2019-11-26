from typing import List, Dict, Tuple
import os
import sys
import json
import random
import pickle
import ideaToText
from codeDotOrg import autoFormat
from tree_encoder import TreeDecoder

GRAMMAR_PATH = 'grammars/assign3'

def createDataList(sampler, source_data_contains, n=1000):
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
				percent_complete += 1
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
	print('Number of submission overlaps:', match)
	print('Number of out-of-training data:', no_match)
	print('Percent Complete: ',
		  f'{percent_complete} / {len(source_data_contains)}',
		  float(percent_complete) / len(source_data_contains))

	return uniqueSubs, counts

def sample(problem=4):
	with open(f'../data/p4/sources-{problem}.json') as source_file:
		source_data = json.load(source_file, cls=TreeDecoder)

	source_data_contains = set() # program -> rubric_item
	for key in source_data:
		expr = autoFormat(source_data[key]).replace('\n', '').replace(' ', '')
		source_data_contains.add(expr)

	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	uniqueSubs, counts = createDataList(sampler, source_data_contains, 50000) # program -> rubric_item
	with open('generated/uniqueSubs.json', 'w') as f:
		json.dump(uniqueSubs, f, indent=2)
	with open('generated/counts.json', 'w') as f:
		json.dump(counts, f, indent=2)
	print(sorted(counts.items(), key=lambda k: k[1], reverse=True)[:500])

if __name__ == '__main__':
	sample()

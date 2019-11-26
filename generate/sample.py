from typing import List, Dict, Tuple
import os
import sys
import json
import random
import ideaToText
from codeDotOrg import autoFormat
from tree_encoder import TreeDecoder

GRAMMAR_PATH = 'grammars/assign3'

def createDataList(sampler, source_data_contains, n=1000):
	uniqueSubs, counts = {}, {}
	num_sampled = 0
	match = 0

	while len(uniqueSubs) < n:
		if num_sampled % 1000 == 0:
			print(num_sampled, len(uniqueSubs))
		sample = sampler.singleSample()
		text = sample['text'].replace('\n', '').replace(' ', '')
		if text not in uniqueSubs:
			uniqueSubs[text] = sample['rubric']
		if text in source_data_contains:
			match += 1
		else:
			if text not in counts:
				counts[text] = 0
			counts[text] += 1
		num_sampled += 1

	print('Number of submission overlaps:', match)
	return uniqueSubs, counts

def sample(problem=4):
	with open(f'../data/p4/sources-{problem}.json') as source_file:
		source_data = json.load(source_file, cls=TreeDecoder)

	source_data_contains = set() # program -> rubric_item
	for key in source_data:
		expr = autoFormat(source_data[key]).replace('\n', '').replace(' ', '')
		source_data_contains.add(expr)

	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	uniqueSubs, counts = createDataList(sampler, source_data_contains, 100000) # program -> rubric_item
	with open('generated/uniqueSubs.json', 'w') as f:
		json.dump(uniqueSubs, f, indent=2)
	with open('generated/counts.json', 'w') as f:
		json.dump(counts, f, indent=2)
	print(sorted(counts.items(), key=lambda k: k[1], reverse=True)[:1000])

if __name__ == '__main__':
	sample()

import ideaToText
import pickle
from codeDotOrg import autoIndent, autoFormat

from typing import List, Dict, Tuple
import os
import sys
import json
import random
from tree_encoder import TreeDecoder
from copy import deepcopy

GRAMMAR_PATH = 'grammars/assign3'
data = {}
pairCounts = {}
# PROBLEM_NUM = 1
SUBMISSION_INIT = "6" 

def read_data(problem):
	print(f"Loading source file for Problem {problem}")
	with open(f'sources-{problem}.pickle', 'rb') as source_file:
		source_data = pickle.load(source_file)

	print(f"Loading activities map for Problem {problem}")
	with open(f'activities-{problem}.pickle', 'rb') as activity_file:
		activity_data = pickle.load(activity_file)

	ids = list(activity_data.keys())
	return source_data, activity_data, ids

def init():
	with open('activities-' + str(problem) + '.pickle') as infile:
		pairCounts = json.load(infile)
	source_data, activity_data, ids = read_data(PROBLEM_NUM)
	firstSubs = pairCounts[SUBMISSION_INIT]
	print(firstSubs)


def createCountsMap(sampler):
	counts = dict()
	num_sampled = 0
	while len(counts) < 20000:
		if num_sampled % 100 == 0:
			print(num_sampled, len(counts))
		sample = sampler.singleSample()
		text = sample['text']
		rubric = sample['rubric']
		if text not in counts:
			counts[text] = 0
		counts[text] += 1
		num_sampled += 1
	return counts

def createDataList(sampler, n=300000):
	uniqueSubs = {}
	num_sampled = 0
	while len(uniqueSubs) < n:
		if num_sampled % 1000 == 0:
			print(num_sampled, len(uniqueSubs))
		sample = sampler.singleSample()
		# new_data = dict()
		# new_data['code'] = sample['text']
		# new_data['label'] = sample['rubric']
		if (sample['text'].replace('\n', '')).replace(' ','') not in uniqueSubs:
			uniqueSubs[(sample['text'].replace('\n', '')).replace(' ','')] = sample['rubric']
		num_sampled += 1
	return uniqueSubs

def main():
	# init()
	problem = 4
	# with open('activities-' + str(problem) + '.pickle') as infile:
	# 	pairCounts = json.load(infile)
	source_data, activity_data, ids = read_data(problem)
	source_data_formatted = {}
	for i in source_data:
		# print((autoFormat(source_data[i]).replace('\n', '')).replace(' ',''))
		source_data_formatted[(autoFormat(source_data[i]).replace('\n', '')).replace(' ','')] = []

	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	uniqueSubs = createDataList(sampler, 50000)
	with open('uniqueSubs2.json', 'w') as f:
		json.dump(uniqueSubs, f, indent=4)
	# print(source_data_formatted)
	# print(uniqueSubs)
	count = 0
	for key in source_data_formatted:
		if key in uniqueSubs:
			print(key)
			source_data_formatted[key] = uniqueSubs[key]
			count += 1
	print('number of submission overlaps:', count)


	

if __name__ == '__main__':
	main()
import os
import os.path
import pickle
import json
from tree_encoder import TreeEncoder, TreeDecoder

DATA_SET_ROOT = 'data/'

def loadActivities(key):
	return _loadItem(key, 'activities')

def loadLevelSources(key):
	return _loadItem(key, 'sources')

def loadLevelSourcesSmall(key):
	return _loadItem(key, 'sourcesSmall')

def loadCountMap(key):
	return _loadItem(key, 'countMap')

def _loadItem(key, itemName):
	if key[0] != 'p': raise Exception(key + ' should start with a "p"')
	problemNum = key[1:]
	fileName = itemName + '-' + problemNum + '.pickle'
	dataDir = os.path.join(DATA_SET_ROOT, key)
	path = os.path.join(dataDir, fileName)
	return pickle.load(open(path, 'rb'), encoding="latin1")

def convert_to_json():
	for i in (1, 2, 4, 9):
		for filetype in ('activities', 'countMap', 'levelIdMap', 'sources', 'sourcesSmall'):
			dict_to_convert = _loadItem(f'p{i}', filetype)
			with open(f'data/p{i}/{filetype}-{i}.json', 'w') as f:
				json.dump(dict_to_convert, f, indent=2, cls=TreeEncoder)


if __name__ == '__main__':
	convert_to_json()

import ideaToText
import pickle
from codeDotOrg import autoIndent

GRAMMAR_PATH = 'grammars/p4sage'

def createDataList(sampler, n=1):
	data = []
	num_sampled = 0
	while len(data) < n:
		sample = sampler.singleSample()
		new_data = dict()
		new_data['code'] = sample['text']
		new_data['label'] = sample['rubric']
		data.append(new_data)
		num_sampled += 1
	return data

def main():
    sampler = ideaToText.Sampler(GRAMMAR_PATH)
    data = createDataList(sampler)
    print(data)

if __name__ == '__main__':
	main()
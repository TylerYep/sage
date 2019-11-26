import ideaToText
import pickle

GRAMMAR_PATH = 'grammars/codeorg4'

def createCountsMap(sampler):
	counts = dict()
	num_sampled = 0
	while len(counts) < 20000:
		if num_sampled % 100 == 0:
			print(num_sampled, len(counts))
		sample = sampler.singleSample()
		text = sample['text']
		if text not in counts:
			counts[text] = 0
		counts[text] += 1
		num_sampled += 1
	return counts

def createDataList(sampler, n=300000):
	data = []
	num_sampled = 0
	while len(data) < n:
		if num_sampled % 1000 == 0:
			print(num_sampled)
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
	with open('data.pkl', 'wb') as f:
		pickle.dump(data, f)

	counts = createCountsMap(sampler)
	with open('counts.pkl', 'wb') as f:
		pickle.dump(counts, f)

if __name__ == '__main__':
	main()
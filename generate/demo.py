import ideaToText

GRAMMAR_PATH = 'grammars/demo'

if __name__ == '__main__':
	sampler = ideaToText.Sampler(GRAMMAR_PATH)
	for i in range(10):
		sample = sampler.singleSample()
		text = sample['text']
		choices = sample['choices']
		rubric = sample['rubric']
		print(text, '\t', choices)

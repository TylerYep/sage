import json

def updateMap(pairCounts, prev, cur):
	if prev not in pairCounts:
		pairCounts[prev] = {cur: 1}
	else:
		if cur not in pairCounts[prev]:
			pairCounts[prev][cur] = 1
		else:
			pairCounts[prev][cur] += 1

def initSub(problem):
	if problem == 1:
		return 6
	if problem == 2:
		return 0
	if problem == 4:
		return 4
	if problem == 9:
		return None


def main(problem):
	pairCounts = {}
	with open('p' + str(problem) + '/activities-' + str(problem) + '.json') as infile:
		data = json.load(infile)
		for k in data:
			snapshots = data[k]
			prev = initSub(problem) # this is the empty program that everyone starts with
			for i in range(len(snapshots)):
				cur = snapshots[i][0]
				updateMap(pairCounts, prev, cur)
				prev = cur
			updateMap(pairCounts, prev, -1)
	with open('pairSubs/p' + str(problem) + '_pairSubmissionCounts.json', 'w') as outfile:
		json.dump(pairCounts, outfile, indent=2)



if __name__ == '__main__':
	main(1)
	main(2)
	main(4)
	# main(9)
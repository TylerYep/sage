import os
import numpy as np
import json
from trainer.labels import get_labels
import matplotlib.pyplot as plt

class Transitions:
    def __init__(self, activities_data, rubric_data, problem):
        self.activities_data = activities_data
        self.rubric_data = rubric_data
        self.tScores = {} # from student ID to transition scores
        self.problem = problem
        self.label_weights = [1 for j in range(len(get_labels(self.problem)))]
        self.scores = [[0, -0.5], [1, 0]] # scores[a][b] means score for transition from a to b
        self.maxScoreToID = {round(i/2, 1): [] for i in range(-len(self.label_weights), 2*len(self.label_weights), 1)}
        self.minScoreToID = {round(i/2, 1): [] for i in range(-len(self.label_weights), 2*len(self.label_weights), 1)}

    def generateTransitionScores(self):
        for s in self.activities_data:
            if len(self.activities_data[s]) == 1:
                self.tScores[s] = None
            else:
                self.tScores[s] = []
                for i in range(len(self.activities_data[s]) - 1):
                    sub1 = self.activities_data[s][i][0]
                    sub2 = self.activities_data[s][i + 1][0]
                    rub1 = self.rubric_data[str(sub1)]
                    rub2 = self.rubric_data[str(sub2)]
                    tList = [self.scores[int(rub1[x])][int(rub2[x])] for x in range(len(rub1))]
                    score = 0.0
                    for j in range(len(tList)):
                        score += (self.label_weights[j] * tList[j])
                    self.tScores[s].append(round(score, 1))

                self.maxScoreToID[round(max(self.tScores[s]), 1)].append(s)
                self.minScoreToID[round(min(self.tScores[s]), 1)].append(s)
        return self.tScores

    def generateBreakthroughGraphs(self):
        x = []
        y = []
        for i in range(-len(self.label_weights), 2*len(self.label_weights), 1):
            x.append(round(i/2, 1))
            y.append(len(self.maxScoreToID[round(i/2, 1)]))
        plt.bar(np.array(x), np.array(y))
        # plt.xticks(np.array(x))
        plt.xlabel('Max Transition Score')
        plt.ylabel('Number of Students')
        plt.title('p' + str(self.problem) + ' maximum transition score for each student')
        plt.savefig('generated/breakthroughBarGraph' + str(self.problem) + '.png')
        plt.clf()

    def generateLowPointsGraphs(self):
        x = []
        y = []
        for i in range(-len(self.label_weights), 2*len(self.label_weights), 1):
            x.append(round(i/2, 1))
            y.append(len(self.minScoreToID[round(i/2, 1)]))
        plt.bar(np.array(x), np.array(y))
        plt.xlabel('Min Transition Score')
        plt.ylabel('Number of Students')
        plt.title('p' + str(self.problem) + ' minimum transition score for each student')
        # plt.xticks(np.array(x))
        plt.savefig('generated/lowPointsBarGraph' + str(self.problem) + '.png')
        plt.clf()

    def saveMinIDs(self):
        with open(f'generated/minIDs-{self.problem}.json', 'w') as dest_file:
            minIDs = []
            for i in range(-len(self.label_weights), 2*len(self.label_weights), 1):
                if round(i/2, 1) in minIDs:
                    minIDs += self.minScoreToID[round(i/2, 1)]
            json.dump(minIDs, dest_file, indent=2)

    def saveMaxIDs(self):
        with open(f'generated/maxIDs-{self.problem}.json', 'w') as dest_file:
            maxIDs = []
            for i in range(2*len(self.label_weights), -len(self.label_weights), -1):
                if round(i/2, 1) in self.maxScoreToID:
                    maxIDs += self.maxScoreToID[round(i/2, 1)]
            json.dump(maxIDs, dest_file, indent=2)


    # def generateBacktrackGraphs(self):



if __name__ == '__main__':
    for problem in (1, 2, 3, 4):
        with open(f'../data/p{problem}/activities-{problem}.json') as activities_file:
            activities_data = json.load(activities_file)
            with open(f'generated/rubric-{problem}.json') as rubric_file:
                rubric_data = json.load(rubric_file)
                t = Transitions(activities_data, rubric_data, problem)
                # print(rubric_data)
                t.generateTransitionScores()
                t.generateBreakthroughGraphs()
                t.generateLowPointsGraphs()
                t.saveMinIDs()
                t.saveMaxIDs()
                print('Finished p' + str(problem))



        # with open(f'generated/rubric-{problem}.json', 'w') as dest_file:
        #     json.dump(rubric_preds, dest_file, indent=2)
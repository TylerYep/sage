import os
import numpy as np
import json
from trainer.labels import get_labels, get_learning_goals
import matplotlib.pyplot as plt

def get_labels(problem):
    ''' map from integers to feedback labels '''
    labels = []
    if problem == 1:
        labels = [
            'noCode',
            'missingRepeat',
            'triangle-wrongNumSides',
            'triangle-tooManyActions',
            'triangle-wrongMoveTurnOrder',
            'side-forgotTurn',
            'side-forgotMove',
            'move-wrongAmount',
            'turn-rightLeftConfusion',
            'turn-wrongAmount',
        ]

    elif problem == 2:
        labels = [
            'noCode',
            'forLoop-wrongLoop',
            'triangle-wrongNumSides',
        ]

    elif problem == 3:
        labels = [
            'no-code',
            'shapeLoop-none',
            'triangle-none',
            'side-none',
            'move-wrongAmount',
            'shapeLoopHeader-missingValue',
            'shapeLoopHeader-wrongOrder',
            'shapeLoopHeader-wrongDelta',
            'shapeLoopHeader-wrongEnd',
            'shapeLoopHeader-wrongStart',
            'triangle-armsLength',
            'triangle-unrolled',
            'triangle-wrongNumSides',
            'side-forgotLeft',
            'side-forgotMove',
            'side-wrongMoveLeftOrder',
            'side-armsLength',
            'turn-wrongAmount',
            'turn-rightLeftConfusion',
        ]

    elif problem == 4:
        labels = [
            'no-code',
            'shapeLoop-none',
            'square-none',
            'side-none',
            'move-wrongAmount',
            'shapeLoopHeader-missingValue',
            'shapeLoopHeader-wrongOrder',
            'shapeLoopHeader-wrongDelta',
            'shapeLoopHeader-wrongEnd',
            'shapeLoopHeader-wrongStart',
            'square-armsLength',
            'square-unrolled',
            'square-wrongNumSides',
            'side-forgotLeft',
            'side-forgotMove',
            'side-wrongMoveLeftOrder',
            'side-armsLength',
            'turn-wrongAmount',
            'turn-rightLeftConfusion',
        ]
    return labels

def get_learning_goals():
    return {
        'atomicStatements': [
            'side-forgotTurn',
            'side-forgotMove',
            'turn-rightLeftConfusion',
            'side-none',
            'side-forgotLeft',
            'side-wrongMoveLeftOrder',

        ],
        'measurements': [
            'turn-wrongAmount',
            'move-wrongAmount',
        ],
        'conditionals': [

        ],
        'repeat': [
            'missingRepeat',
            'triangle-wrongNumSides',
            'triangle-tooManyActions',
            'triangle-wrongMoveTurnOrder',
            'square-armsLength',
            'square-unrolled',
            'square-wrongNumSides',
            'triangle-none',
            'square-none',

        ],
        'forLoop': [
            'forLoop-wrongLoop',
            'shapeLoop-none',
            'shapeLoopHeader-missingValue',
            'shapeLoopHeader-wrongOrder',
            'shapeLoopHeader-wrongDelta',
            'shapeLoopHeader-wrongEnd',
            'shapeLoopHeader-wrongStart',
        ],
        'nestedLoops': [

        ],
        'variables': [
            'move-wrongAmount',

        ],
        'math': [

        ]
    }

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
        self.totalScoreToID = {round(i/2, 1): [] for i in range(-10, 2*30, 1)}

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
                self.totalScoreToID[round(sum(self.tScores[s]), 1)].append(s)
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

    def generateFinalLearning(self):
        counts = {}
        for i in self.tScores:
            if self.tScores[i] == None:
                if round(0, 1) not in counts:
                    counts[round(0, 1)] = 1
                else:
                    counts[round(0, 1)] += 1
            else:
                s = round(sum(self.tScores[i]), 1)
                if s not in counts:
                    counts[s] = 1
                else:
                    counts[s] += 1
        x = []
        y = []
        for a in counts:
            x.append(a)
            y.append(counts[a])
        plt.bar(np.array(x), np.array(y))
        plt.xlabel('Total Learning Score')
        plt.ylabel('Number of Students')
        plt.title('p' + str(self.problem) + ' total learning score for each student')
        # plt.xticks(np.array(x))
        plt.savefig('generated/total_learning_p' + str(self.problem) + '.png')
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

    def saveTotalIDs(self):
        with open(f'generated/totalScoreIDs-{self.problem}.json', 'w') as dest_file:
            totalScoreIDs = []
            for i in range(-10, 2*30, 1):
                if round(i/2, 1) in self.totalScoreToID:
                    totalScoreIDs += self.totalScoreToID[round(i/2, 1)]
            json.dump(totalScoreIDs, dest_file, indent=2)




    # def generateBacktrackGraphs(self):

class AllProbsTransitions:
    def __init__(self, problems):
        self.problems = problems
        self.transitions = {}

    def initialize(self):
        for p in self.problems:
            with open(f'../data/p{p}/activities-{p}.json') as activities_file:
                activities_data = json.load(activities_file)
                with open(f'generated/rubric-{p}.json') as rubric_file:
                    rubric_data = json.load(rubric_file)
                    self.transitions[p] = Transitions(activities_data, rubric_data, p)

    def doEverything(self):
        for p in self.transitions:
            self.transitions[p].generateTransitionScores()
            self.transitions[p].generateBreakthroughGraphs()
            self.transitions[p].generateLowPointsGraphs()
            self.transitions[p].saveMinIDs()
            self.transitions[p].saveMaxIDs()
            self.transitions[p].generateFinalLearning()
            self.transitions[p].saveTotalIDs()
            print('Finished p' + str(p))

if __name__ == '__main__':

    everything = AllProbsTransitions((1, 2, 3, 4))
    everything.initialize()
    everything.doEverything()



    # for problem in (1, 2, 3, 4):
    #     with open(f'../data/p{problem}/activities-{problem}.json') as activities_file:
    #         activities_data = json.load(activities_file)
    #         with open(f'generated/rubric-{problem}.json') as rubric_file:
    #             rubric_data = json.load(rubric_file)
    #             t = Transitions(activities_data, rubric_data, problem)
    #             # print(rubric_data)
    #             t.generateTransitionScores()
    #             t.generateBreakthroughGraphs()
    #             t.generateLowPointsGraphs()
    #             t.saveMinIDs()
    #             t.saveMaxIDs()
    #             print('Finished p' + str(problem))



        # with open(f'generated/rubric-{problem}.json', 'w') as dest_file:
        #     json.dump(rubric_preds, dest_file, indent=2)
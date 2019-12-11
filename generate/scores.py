import os
import numpy as np
import json
from trainer.labels import get_labels, get_learning_goals
import matplotlib.pyplot as plt

class Transitions:
    def __init__(self, activities_data, rubric_data, problem):
        self.activities_data = activities_data
        self.rubric_data = rubric_data
        self.tScores = {} # from student ID to transition scores
        self.problem = problem
        self.learning_goals = get_learning_goals()
        self.bScores = {}
        self.label_weights = [1 for j in range(len(get_labels(self.problem)))]
        self.discount_factor = 0.9
        self.bucket_weights = [1 for _ in range(8)]
        self.scores = [[0, -0.5], [1, 0]] # scores[a][b] means score for transition from a to b
        self.maxScoreToID = {} # {round(i/2, self.precision): [] for i in range(-len(self.label_weights), 2*len(self.label_weights), 1)}
        self.minScoreToID = {} # {round(i/2, self.precision): [] for i in range(-len(self.label_weights), 2*len(self.label_weights), 1)}
        self.totalScoreToID = {} # {round(i/2, self.precision): [] for i in range(-10, 2*30, 1)}
        self.IDtoOldTotalScore = {}
        self.IDtoTotalScore = {}
        self.precision = 1
        self.allIDs = set()

    def getAllIDs(self):
        return self.allIDs

    def generateBucketScores(self):
        for s in self.activities_data:
            if len(self.activities_data[s]) == 1:
                self.bScores[s] = None
            # else:
                # self.bScores[s] = []
                # for i in range(len(self.activities_data[s]) - 1):
                #     sub1 = self.activities_data[s][i][0]
                #     sub2 = self.activities_data[s][i + 1][0]
                #     rub1 = self.rubric_data[str(sub1)]
                #     rub2 = self.rubric_data[str(sub2)]
                #     tList = [self.scores[int(rub1[x])][int(rub2[x])] for x in range(len(rub1))]
                #     score = 0.0
                #     for j in range(len(tList)):
                #         score += (self.label_weights[j] * tList[j])
                #     self.bScores[s].append(round(score, self.precision))

                # self.BmaxScoreToID[round(max(self.bScores[s]), self.precision)].append(s)
                # self.BminScoreToID[round(min(self.bScores[s]), self.precision)].append(s)
                # self.BtotalScoreToID[round(sum(self.bScores[s]), self.precision)].append(s)
        return self.bScores

    def addToMap(self, key, value, someMap):
        if key in someMap:
            someMap[key].append(value)
        else:
            someMap[key] = [value]

    def generateTransitionScores(self):
        
        for s in self.activities_data:
            self.allIDs.add(s)
            if len(self.activities_data[s]) == 1:
                self.tScores[s] = None
                # self.IDtoOldTotalScore[s] = 0
            else:
                self.tScores[s] = []
                discounts = [1 for j in range(len(get_labels(self.problem)))]
                for i in range(len(self.activities_data[s]) - 1):
                    sub1 = self.activities_data[s][i][0]
                    sub2 = self.activities_data[s][i + 1][0]
                    rub1 = self.rubric_data[str(sub1)]
                    rub2 = self.rubric_data[str(sub2)]
                    tList = [self.scores[int(rub1[x])][int(rub2[x])] for x in range(len(rub1))]
                    score = 0.0
                    for j in range(len(tList)):
                        if tList[j] == 1:
                            score += (self.label_weights[j] * tList[j]*discounts[j])
                            if discounts[j] != 0.5:
                                discounts[j] *= self.discount_factor
                                if discounts[j] < 0.5:
                                    discounts[j] = 0.5
                        else:
                            score += (self.label_weights[j] * tList[j])
                            
                    self.tScores[s].append(round(score, self.precision))

                # self.maxScoreToID[round(max(self.tScores[s]), self.precision)].append(s)
                # self.minScoreToID[round(min(self.tScores[s]), self.precision)].append(s)
                # self.totalScoreToID[round(sum(self.tScores[s]), self.precision)].append(s)
                self.addToMap(round(max(self.tScores[s]), self.precision), s, self.maxScoreToID)
                self.addToMap(round(min(self.tScores[s]), self.precision), s, self.minScoreToID)
                self.addToMap(round(sum(self.tScores[s]), self.precision), s, self.totalScoreToID)
                self.IDtoOldTotalScore[s] = round(sum(self.tScores[s]), self.precision)
                self.IDtoTotalScore[s] = round(sum(self.tScores[s])/len(self.activities_data[s]), self.precision)
        return self.tScores

    def getXandY(self):
        if self.problem == 1:
            X = [round(x/10, self.precision) for x in range(-12, 27)]
            print(X)
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoTotalScore:
                curScore = self.IDtoTotalScore[someID]
                roundedScore = round(curScore, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 2:
            X = [round(x/10, self.precision) for x in range(-4, 9)]
            print(X)
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoTotalScore:
                curScore = self.IDtoTotalScore[someID]
                roundedScore = round(curScore, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 3:
            X = [round(x/10, self.precision) for x in range(-17, 27)]
            print(X)
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoTotalScore:
                curScore = self.IDtoTotalScore[someID]
                roundedScore = round(curScore, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 4:
            X = [round(x/10, self.precision) for x in range(-17, 30)]
            print(X)
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoTotalScore:
                curScore = self.IDtoTotalScore[someID]
                roundedScore = round(curScore, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y

    def getXandYOLD(self):
        if self.problem == 1:
            X = [round(x/2, self.precision) for x in range(-6, 28)]
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoOldTotalScore:
                curScore = self.IDtoOldTotalScore[someID]
                roundedScore = round(round(curScore*2)/2, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 2:
            X = [round(x/2, self.precision) for x in range(-4, 5)]
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoOldTotalScore:
                curScore = self.IDtoOldTotalScore[someID]
                roundedScore = round(round(curScore*2)/2, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 3:
            X = [round(x/2, self.precision) for x in range(-8, 35)]
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoOldTotalScore:
                curScore = self.IDtoOldTotalScore[someID]
                roundedScore = round(round(curScore*2)/2, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y
        elif self.problem == 4:
            X = [round(x/2, self.precision) for x in range(-9, 33)]
            Y = [0 for _ in range(len(X))]
            for someID in self.IDtoOldTotalScore:
                curScore = self.IDtoOldTotalScore[someID]
                roundedScore = round(round(curScore*2)/2, self.precision)
                Y[X.index(roundedScore)] += 1
            return X, Y

    def generateTotalScoreGraphs(self):
        x, y = self.getXandY()
        plt.bar(np.array(x), np.array(y), width=0.1)
        # print(x)
        # print(y)
        plt.xlabel('Total Learning Score')
        plt.ylabel('Number of Students')
        plt.title('p' + str(self.problem) + ' total learning score for each student')
        # plt.savefig('generated/totalScoresGraphP' + str(self.problem) + 'with0s.png')
        plt.savefig('generated/totalScoresGraphP' + str(self.problem) + '.png')
        plt.clf()

    def generateTotalScoreGraphsOLD(self):
        x, y = self.getXandYOLD()
        plt.bar(np.array(x), np.array(y), width=0.5)
        # print(x)
        # print(y)
        plt.xlabel('Total Learning Score')
        plt.ylabel('Number of Students')
        plt.title('p' + str(self.problem) + ' total learning score for each student (with old formula)')
        # plt.savefig('generated/totalScoresGraphP' + str(self.problem) + 'with0s.png')
        plt.savefig('generated/totalScoresGraphP' + str(self.problem) + '-old-formula.png')
        plt.clf()


    # def generateBreakthroughGraphs(self): # THIS IS BROKEN
    #     x, y = self.getXandYOLD()
    #     # # print(orderedMap)
    #     # for i in orderedMap:# range(-len(self.label_weights), 2*len(self.label_weights), 1):
    #     #     x.append(i[0])
    #     #     # print(i)
    #     #     y.append(len(i[1]))
    #     #     # x.append(round(i/2, self.precision))
    #     #     # y.append(len(self.maxScoreToID[round(i/2, self.precision)]))
    #     plt.bar(np.array(x), np.array(y))
    #     print(x)
    #     print(y)
    #     # plt.xticks(np.array(x))
    #     plt.xlabel('Max Transition Score')
    #     plt.ylabel('Number of Students')
    #     plt.title('p' + str(self.problem) + ' maximum transition score for each student')
    #     plt.savefig('generated/breakthroughBarGraph' + str(self.problem) + '.png')
    #     plt.clf()

    # def generateFinalLearning(self):
    #     counts = {}
    #     for i in self.tScores:
    #         if self.tScores[i] == None:
    #             if round(0, self.precision) not in counts:
    #                 counts[round(0, self.precision)] = 1
    #             else:
    #                 counts[round(0, self.precision)] += 1
    #         else:
    #             s = round(sum(self.tScores[i]), self.precision)
    #             if s not in counts:
    #                 counts[s] = 1
    #             else:
    #                 counts[s] += 1
    #     x = []
    #     y = []
    #     for a in counts:
    #         x.append(a)
    #         y.append(counts[a])
    #     plt.bar(np.array(x), np.array(y))
    #     plt.xlabel('Total Learning Score')
    #     plt.ylabel('Number of Students')
    #     plt.title('p' + str(self.problem) + ' total learning score for each student')
    #     # plt.xticks(np.array(x))
    #     plt.savefig('generated/total_learning_p' + str(self.problem) + '.png')
    #     plt.clf()

    # def generateLowPointsGraphs(self):
    #     x = []
    #     y = []
    #     for i in range(-len(self.label_weights), 2*len(self.label_weights), 1):
    #         x.append(round(i/2, self.precision))
    #         y.append(len(self.minScoreToID[round(i/2, self.precision)]))
    #     plt.bar(np.array(x), np.array(y))
    #     plt.xlabel('Min Transition Score')
    #     plt.ylabel('Number of Students')
    #     plt.title('p' + str(self.problem) + ' minimum transition score for each student')
    #     # plt.xticks(np.array(x))
    #     plt.savefig('generated/lowPointsBarGraph' + str(self.problem) + '.png')
    #     plt.clf()

    # def saveMinIDs(self):
    #     with open(f'generated/minIDs-{self.problem}.json', 'w') as dest_file:
    #         minIDs = []
    #         for i in range(-len(self.label_weights), 2*len(self.label_weights), 1):
    #             if round(i/2, self.precision) in minIDs:
    #                 minIDs += self.minScoreToID[round(i/2, self.precision)]
    #         json.dump(minIDs, dest_file, indent=2)

    # def saveMaxIDs(self):
    #     with open(f'generated/maxIDs-{self.problem}.json', 'w') as dest_file:
    #         maxIDs = []
    #         for i in range(2*len(self.label_weights), -len(self.label_weights), -1):
    #             if round(i/2, self.precision) in self.maxScoreToID:
    #                 maxIDs += self.maxScoreToID[round(i/2, self.precision)]
    #         json.dump(maxIDs, dest_file, indent=2)

    # def saveTotalIDs(self):
    #     with open(f'generated/totalScoreIDs-{self.problem}.json', 'w') as dest_file:
    #         totalScoreIDs = []
    #         for i in range(-10, 2*30, 1):
    #             if round(i/2, self.precision) in self.totalScoreToID:
    #                 totalScoreIDs += self.totalScoreToID[round(i/2, self.precision)]
    #         json.dump(totalScoreIDs, dest_file, indent=2)




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
            self.transitions[p].generateTotalScoreGraphs()
            self.transitions[p].generateTotalScoreGraphsOLD()
            # self.transitions[p].generateBreakthroughGraphs()
            # self.transitions[p].generateLowPointsGraphs()
            # self.transitions[p].saveMinIDs()
            # self.transitions[p].saveMaxIDs()
            # self.transitions[p].generateFinalLearning()
            # self.transitions[p].saveTotalIDs()
            print('Finished p' + str(p))

    def saveAllScores(self):
        
        with open(f'generated/totalScoresOLD.json', 'w') as dest_file:
            min_scores = [float('inf') for _ in range(len(self.problems))]
            max_scores = [float('-inf') for _ in range(len(self.problems))]
            allIDs = self.transitions[self.problems[0]].allIDs
            IDtoScores = {}
            for someID in allIDs:
                scores = []
                for i in range(len(self.problems)):
                    totalScoresMap = self.transitions[(i + 1)].IDtoOldTotalScore
                    if someID in totalScoresMap:
                        curScore = totalScoresMap[someID]
                        if min_scores[i] > curScore:
                            min_scores[i] = curScore
                        if max_scores[i] < curScore:
                            max_scores[i] = curScore
                        scores.append(curScore)
                    else:
                        scores.append('0')
                IDtoScores[someID] = scores
            # print('min orig/old scores', min_scores)
            # print('max orig/old scores', max_scores)
            json.dump(IDtoScores, dest_file, indent=2)

        with open(f'generated/totalScores.json', 'w') as dest_file:
            min_scores = [float('inf') for _ in range(len(self.problems))]
            max_scores = [float('-inf') for _ in range(len(self.problems))]
            allIDs = self.transitions[self.problems[0]].allIDs
            IDtoScores = {}
            for someID in allIDs:
                scores = []
                for i in range(len(self.problems)):
                    totalScoresMap = self.transitions[(i + 1)].IDtoTotalScore
                    if someID in totalScoresMap:
                        curScore = totalScoresMap[someID]
                        if min_scores[i] > curScore:
                            min_scores[i] = curScore
                        if max_scores[i] < curScore:
                            max_scores[i] = curScore
                        scores.append(curScore)
                    else:
                        scores.append('0')
                IDtoScores[someID] = scores
            # print('min scores', min_scores)
            # print('max scores', max_scores)
            json.dump(IDtoScores, dest_file, indent=2)

        # with open(f'generated/totalScores.json', 'w') as dest_file:
        #     allIDs = self.transitions[self.problems[0]].allIDs
        #     IDtoScores = {}
        #     for someID in allIDs:
        #         scores = []
        #         for i in range(len(self.problems)):
        #             if someID in self.transitions[(i + 1)].IDtoOldTotalScore:
        #                 scores.append(self.transitions[(i + 1)].IDtoOldTotalScore[someID])
        #             else:
        #                 scores.append(0)
        #         IDtoScores[someID] = scores
        #     json.dump(IDtoScores, dest_file, indent=2)


if __name__ == '__main__':

    everything = AllProbsTransitions((1, 2, 3, 4))
    everything.initialize()
    everything.doEverything()
    everything.saveAllScores()



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
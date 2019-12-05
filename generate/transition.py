from typing import Tuple
from predict import preprocess, make_prediction
from trainer.labels import get_labels
from gui import GUIState

class TScores:
    def __init__(self, state: GUIState, problems: Tuple[int]):
        self.state = state
        self.label_weights = {i: [1 for j in range(len(get_labels(i)))] for i in problems}
        self.scores = [[0, -0.5], [1, 0]] # scores[a][b] means score for transition from a to b

    def get_transition_scores(self, rubric_data):
        tScores = []
        curStudent = self.state.curr_student
        nn_data = preprocess(self.state.submissions)
        preds = make_prediction(self.state.curr_problem, nn_data)[0]
        if len(self.state.submissions) == 1:
            print('No Transition Scores (Only 1 Submission)')
        else:
            print('Transition Scores\n')
            totalScore = 0
            for i in range(len(self.state.submissions) - 1):
                rub1, rub2 = preds[i], preds[i + 1]
                tList = [self.scores[int(rub1[i])][int(rub2[i])] for i in range(len(rub1))]

                score = 0
                for j in range(len(tList)):
                    score += (self.label_weights[self.state.curr_problem][j] * tList[j])

                if score != 0:
                    print(f'Sub {i+1} to Sub {i+2} with transition learning score of {score}: ', tList)
                totalScore += score
            print(f'\nFinal Learning Score:   {totalScore}')
            print(f'(Ended with {int(sum(preds[len(self.state.submissions) - 1]))}',
                  f'out of {len(preds[len(self.state.submissions) - 1])} rubric items)')

    def update_weights(self, problem, weights):
        if problem in self.label_weights and len(weights) == len(self.label_weights[problem]):
            self.label_weights[problem] = weights

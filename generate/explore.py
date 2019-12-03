from typing import List, Dict, Tuple
import os
import sys
import json
import random
import pickle
import numpy as np
import torch
import torch.utils.data as data

import trainer
from trainer.labels import get_label_to_ix, get_labels
from trainer.datasets import ProductionDataset
from tree_encoder import TreeDecoder
from codeDotOrg import autoFormat, pseudoCodeToTree, remove_whitespace
from preprocess import flatten_ast
from lstmmodels import FeedbackNN
from gui import GUIState

CURR_PROBLEMS = (1, 2, 3, 4)
USE_FEEDBACK_NN = True
SPACE = " "

class TScores:
    def __init__(self, state):
        self.state = state
        self.label_weights = {i: [1 for j in range(len(get_labels(i)))] for i in range(1, 5)}
        self.scores = [[0, -1], [1, 0]] # scores[a][b] means score for transition from a to b

    def getCurTransitionScores(self, rubric_data):
        output = ''
        tScores = []
        curStudent = self.state.curr_student
        nn_data = preprocess(self.state.submissions)
        preds = make_prediction(self.state.curr_problem, nn_data)
        if len(self.state.submissions) == 1:
            print('No Transition Scores (Only 1 Submission)')
        else:
            print('Transition Scores\n')
            totalScore = 0
            for i in range(len(self.state.submissions) - 1):
                rub1 = preds[i]
                rub2 = preds[i + 1]
                tList = [self.scores[int(rub1[i])][int(rub2[i])] for i in range(len(rub1))]
                score = 0
                for j in range(len(tList)):
                    score += (self.label_weights[self.state.curr_problem][j] * tList[j])
                print(f'Sub {i+1} to Sub {i+2} with transition learning score of {score}: ', tList)
                totalScore += score
            print(f'\nFinal Learning Score: {totalScore}')
            print(f'\nEnded with {int(sum(preds[len(self.state.submissions) - 1]))}',
                  f'out of {len(preds[len(self.state.submissions) - 1])} rubric items')

    def updateWeights(self, problem, weights):
        if problem in self.label_weights and len(weights) == len(self.label_weights[problem]):
            self.label_weights[problem] = weights


def show_progress_bar(state, num_submissions):
    LENGTH = 100
    progress_bar = '|'
    for i in range(num_submissions):
        if i <= state.curr_index:
            progress_bar += ("=" * (LENGTH // num_submissions))
        else:
            progress_bar += ("-" * (LENGTH // num_submissions))
    progress_bar += "|"
    print(progress_bar)


def read_data(problem):
    print(f"Loading source file for Problem {problem}")
    with open(f'../data/p{problem}/sources-{problem}.json') as source_file:
        source_data = json.load(source_file, cls=TreeDecoder)

    print(f"Loading activities map for Problem {problem}")
    with open(f'../data/p{problem}/activities-{problem}.json') as activity_file:
        activity_data = json.load(activity_file, cls=TreeDecoder)

    if USE_FEEDBACK_NN:
        rubric_data = {}
    else:
        print(f"Loading sourceCode-to-rubric map for Problem {problem}")
        with open(f'generated/uniqueSubs-{problem}.json') as rubric_file:
            rubric_data = json.load(rubric_file)

    ids = list(activity_data.keys())
    return source_data, activity_data, ids, rubric_data


def preprocess(nn_data):
    programs = []
    for ast in nn_data:
        code_list = flatten_ast(ast)
        code_str = ' '.join(code_list)
        programs.append(code_str)
    return np.array(programs)


def make_prediction(problem, programs):
    checkpoint_path = os.path.join(os.path.dirname(__file__), 'checkpoints', f'cp{problem}')
    checkpoint_path = os.path.join(checkpoint_path, 'model_best.pth.tar')

    device = torch.device('cpu')  # no CUDA support for now

    checkpoint = torch.load(checkpoint_path)
    config = checkpoint['config']

    model = FeedbackNN(vocab_size=checkpoint['vocab_size'],
                       num_labels=checkpoint['num_labels'])
    model.load_state_dict(checkpoint['state_dict'])  # load trained model
    model = model.eval()

    # reproducibility
    torch.manual_seed(config['seed'])
    np.random.seed(config['seed'])

    real_dataset = ProductionDataset(programs,
                                     vocab=checkpoint['vocab'],
                                     max_seq_len=config['max_seq_len'],
                                     min_occ=config['min_occ'])
    real_loader = data.DataLoader(real_dataset,
                                  batch_size=config['batch_size'],
                                  shuffle=False)

    pred_arr = []
    with torch.no_grad():
        for (token_seq, token_len) in real_loader:
            token_seq = token_seq.to(device)
            token_len = token_len.to(device)
            label_out = model(token_seq, token_len)
            pred_npy = torch.round(label_out).detach().numpy()
            pred_arr.append(pred_npy)
    return pred_arr[0]


def run_gui():
    prob_data: Dict[int, Tuple] = {}
    for num in CURR_PROBLEMS:
        prob_data[num] = read_data(num)

    source_data, activity_data, ids, rubric_data = prob_data[CURR_PROBLEMS[0]]
    student_id = random.choice(ids)
    state = GUIState(prob_data,
                     student_id=student_id,
                     history=[student_id],
                     curr_problem=CURR_PROBLEMS[0])

    while state.action != SPACE:
        os.system('clear')

        source_data, activity_data, ids, rubric_data = state.get_problem_data()

        print("Student id:", state.student_id)
        if state.student_id not in activity_data:
            print(f"\nStudent had no submission for Problem {state.curr_problem}.\n")
        else:
            state.submissions = \
                [source_data[str(program_id)] for program_id, _ in activity_data[state.student_id]]

            num_submissions = len(state.submissions)
            problem = state.submissions[state.curr_index]
            program_id, timestamp = activity_data[state.student_id][state.curr_index]
            print("Submission:", state.curr_index+1, "out of", num_submissions)
            print("Timestamp:", timestamp)
            print("Program Rank:", program_id, '\n')

            program_tree = autoFormat(problem)
            if state.simple_mode:
                print(program_tree, '\n')
            else:
                print(problem, '\n')

            show_progress_bar(state, num_submissions)

            print("Rubric items: ")
            cleaned_program = remove_whitespace(program_tree)
            spaces = "   "
            if USE_FEEDBACK_NN:
                nn_data = preprocess(state.submissions)
                preds = make_prediction(state.curr_problem, nn_data)
                if not preds[state.curr_index].any():
                    print(spaces, "Submission looks good!")
                else:
                    for index in range(len(preds[state.curr_index])):
                        if preds[state.curr_index][index] == 1:
                            _, IX_TO_LABEL, _ = get_label_to_ix(state.curr_problem)
                            print(spaces, IX_TO_LABEL[index])

            else:
                if cleaned_program in rubric_data:
                    if len(rubric_data[cleaned_program]) == 0:
                        print(spaces, "Submission looks good!")
                    else:
                        for item in rubric_data[cleaned_program]:
                            print(spaces, item)
                else:
                    print("\nNo rubric items found.\n")

            print()
            # tScores = TScores(state)
            # tScores.getCurTransitionScores(rubric_data)

        print()
        with open('../data/student-rubric.json') as f:
            student_data = json.load(f)
            if state.student_id in student_data:
                for line in student_data[state.student_id]:
                    print(line)
        print()

        state.get_action()
        state.update_state(ids)


if __name__ == '__main__':
    run_gui()

    # Problem 1 interesting:
    # 1eb24f31bcd0c1be6b6f1f5a90aeec7b
    # d0cd3baccf1c7185d6674f4b2d041441
    # e1f895be584bde8e24b5965aeb9f9a85
    # fd4b849ec5f1202428194a6dfb81875d
    # f21c0f983d5690b97d8417f0a60fa3ff
    # 34af15319de837c25bea29fd5b1914fe

    # Problem 2 interesting:
    # e01d8b54fd8b2559a69f974cc0a85ff7
    # 70e90d1d1273b4940bb8d0af3faadf72
    # 919d02f28230e7f543880fdb22845874

# MY FAVORITE P1: dff01204325d3fdaa01f4b4f9d23d713
'''
print(f"Loading count map for Problem {problem}")
with open(f'data/p{problem}/countMap-{problem}.json') as count_file:
    count_data = json.load(count_file, cls=TreeDecoder)

print("Program Rank:", program_id, f"(similar programs:{count_data[str(program_id)]})")
'''

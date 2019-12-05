from typing import List, Dict, Tuple
import os
import sys
import json
import random
import pickle

import trainer
from trainer.labels import get_label_to_ix, get_learning_goals
from tree_encoder import TreeDecoder
from codeDotOrg import autoFormat, pseudoCodeToTree, remove_whitespace
from gui import GUIState
from predict import preprocess, make_prediction
from transition import TScores

CURR_PROBLEMS = (1, 2, 3, 4)
USE_FEEDBACK_NN = True
SPACE = " "


def show_progress_bar(state, num_submissions):
    LENGTH = 100
    progress_bar = '|'
    for i in range(num_submissions):
        if i <= state.curr_index:
            progress_bar += ("=" * (LENGTH // num_submissions))
        else:
            progress_bar += ("-" * (LENGTH // num_submissions))
    progress_bar += "|"
    print(progress_bar, "\n")


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

    with open(f'generated/reportcards.json') as report_file:
        report_cards = json.load(report_file)

    ids = list(activity_data.keys())
    return source_data, activity_data, ids, rubric_data, report_cards


def run_gui():
    prob_data: Dict[int, Tuple] = {}
    for num in CURR_PROBLEMS:
        prob_data[num] = read_data(num)

    _, _, ids, _, _ = prob_data[CURR_PROBLEMS[0]]
    student_id = random.choice(ids)
    state = GUIState(prob_data,
                     student_id=student_id,
                     history=[student_id],
                     curr_problem=CURR_PROBLEMS[0])

    while state.action != SPACE:
        os.system('clear')

        source_data, activity_data, ids, rubric_data, report_cards = state.get_problem_data()

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
                preds = make_prediction(state.curr_problem, nn_data)[0]
                if not preds[state.curr_index].any():
                    print(spaces, "Submission looks good!")
                else:
                    for index in range(len(preds[state.curr_index])):
                        if preds[state.curr_index][index] == 1:
                            _, IX_TO_LABEL, _ = get_label_to_ix(state.curr_problem)
                            print(spaces, IX_TO_LABEL[index])

                # print()
                # tScores = TScores(state, CURR_PROBLEMS)
                # tScores.get_transition_scores(rubric_data)
                if state.show_report_card:
                    print("\n\n\n")
                    print("-"*50, "")
                    print("Report Card - Student Summary\n")
                    print("Total Estimated Change in Ability: ", report_cards[state.student_id]['0'])
                    for num in CURR_PROBLEMS:
                        rubric_item_indexes = report_cards[state.student_id][str(num)]
                        _, IX_TO_LABEL, _ = get_label_to_ix(num)
                        for idx in rubric_item_indexes:
                            print(num, IX_TO_LABEL[idx])

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

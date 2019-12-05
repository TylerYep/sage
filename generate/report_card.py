from typing import Dict, Tuple, List
import json
import numpy as np
import sys

from gui import GUIState
from trainer.labels import get_learning_goals, get_labels
from tree_encoder import TreeDecoder

CURR_PROBLEMS = (1, 2, 3, 4)

def read_data(problem):
    print(f"Loading activities map for Problem {problem}")
    with open(f'../data/p{problem}/activities-{problem}.json') as activity_file:
        activity_data = json.load(activity_file, cls=TreeDecoder)

    with open(f'generated/rubric-{problem}.json') as score_file:
        rubric_scores = json.load(score_file)

    ids = list(activity_data.keys())
    return activity_data, ids, rubric_scores


def get_report_card():
    prob_data: Dict[int, Tuple] = {}
    for num in CURR_PROBLEMS:
        prob_data[num] = read_data(num)

    LABELS = {i: get_labels(i) for i in CURR_PROBLEMS}

    report_cards: Dict[str, List[int]] = {}
    _, student_ids, _ = prob_data[1]

    for student_id in student_ids:
        report_card = {}
        total_score = 0.0
        for problem in CURR_PROBLEMS:
            activity_data, _, rubric_scores = prob_data[problem]
            if student_id in activity_data:
                scores = [rubric_scores[str(program_id)] for program_id, _ in activity_data[student_id]]
                prob_score, learned_items = transitions(scores, problem, LABELS)
                total_score += prob_score
                report_card[problem] = learned_items
            else:
                report_card[problem] = []
        report_card[0] = total_score
        report_cards[student_id] = report_card

    with open(f'generated/reportcards.json', 'w') as dest_file:
        json.dump(report_cards, dest_file)


def transitions(scores, problem, LABELS):
    transition_matrix = [[0, -0.5], [1, 0]] # scores[a][b] means score for transition from a to b
    totalScore = 0
    final_list = np.zeros(len(scores[0]))
    for i in range(len(scores) - 1):
        sub1, sub2 = scores[i], scores[i + 1]
        t_list = np.array([transition_matrix[int(sub1[i])][int(sub2[i])] for i in range(len(sub1))])
        totalScore += sum(t_list)
        final_list += t_list

    learned_items = []
    for i, item in enumerate(list(final_list)):
        if item != 0:
            learned_items.append(i)
            # learned_items.append((i, item))

    return totalScore, learned_items




if __name__ == '__main__':
    get_report_card()
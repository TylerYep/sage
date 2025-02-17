from typing import Dict, Tuple, List
import json
import numpy as np
import sys
import math

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
                prob_score, learned_items = transitions(student_id, scores, problem, LABELS)
                total_score += prob_score
                report_card[problem] = learned_items
            else:
                report_card[problem] = []
        report_card[0] = total_score
        report_cards[student_id] = report_card

    with open(f'generated/reportcards.json', 'w') as dest_file:
        json.dump(report_cards, dest_file, indent=2)


def createTransList(student_id, scores, trans_matrix, sub1, sub2, discounts, discount_factor):
    t_list = []
    for j in range(len(sub1)):
        val = trans_matrix[int(sub1[j])][int(sub2[j])]
        if val == 1:
            t_list.append(val*discounts[j])
            if discounts[j] != 0.5:
                discounts[j] *= discount_factor
                if discounts[j] < 0.5:
                    discounts[j] = 0.5
        else:
            t_list.append(val)

    return t_list


def transitions(student_id, scores, problem, LABELS):
    transition_matrix = [[0, -0.5], [1, 0]] # scores[a][b] means score for transition from a to b
    discounts = [1 for _ in range(len(scores[0]))]
    discount_factor = 0.9
    totalScore = 0
    final_list = np.zeros(len(scores[0]))
    for i in range(len(scores) - 1):
        sub1, sub2 = scores[i], scores[i + 1]
        t_list = np.array(createTransList(student_id, scores, transition_matrix, sub1, sub2, discounts, discount_factor))
        totalScore += sum(t_list)
        final_list += t_list

    learned_items = []
    for i, item in enumerate(list(final_list)):
        if item != 0:
            learned_items.append(i)

    return totalScore / math.sqrt(len(scores)), learned_items


if __name__ == '__main__':
    get_report_card()

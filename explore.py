from typing import List, Dict, Tuple
import os
import sys
import json
import random
from tree_encoder import TreeDecoder
from copy import deepcopy

from codeDotOrg import autoFormat

clear = lambda: os.system('clear')

SUBMISSION_LEFT = "["
SUBMISSION_RIGHT = "]"
ENTER = "\r"
UNENTER = "\\"
CTRLC = "\x03"
SPACE = " "
NEXT = "n"
PREV = "p"
FIND_ID = "f"
SIMPLE_MODE_TOGGLE =  "s"
PROBLEM_1 = "1"
PROBLEM_2 = "2"
PROBLEM_4 = "4"
PROBLEM_9 = "9"

ALL_KEYS = ("", SUBMISSION_LEFT, SUBMISSION_RIGHT, SPACE, CTRLC, ENTER,
            UNENTER, NEXT, PREV, FIND_ID, SIMPLE_MODE_TOGGLE,
            PROBLEM_1, PROBLEM_2, PROBLEM_4, PROBLEM_9)

def getch():
    ''' Gets a single character from the user. '''
    import termios
    import tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

def get_action():
    ''' Prints out the prompt and then waits for the user to select an action. '''
    action = None
    prompt = (f"\nType {PREV} or {UNENTER} to see the previous student.\n"
              f"Type {NEXT} or RETURN to see the next student.\n\n"
              f"Type {SUBMISSION_LEFT} to see the previous submission.\n"
              f"Type {SUBMISSION_RIGHT} to see the next submission.\n\n"
              f"Type {FIND_ID} to enter a specific student id.\n\n"
              f"Type {SIMPLE_MODE_TOGGLE} to switch in/out of simple mode.\n\n"
              f"Press SPACE to exit!\n\n")
    print(prompt)

    while action not in ALL_KEYS:
        action = getch()
        if action == CTRLC:
            sys.exit()
    return action

class GUIState:
    def __init__(self,
                 action: str = None,
                 student_id: str = None,
                 history: List = [],
                 curr_index: int = 0,
                 curr_student: int = 0,
                 simple_mode: bool = True,
                 curr_problem: int = 1):
        self.action = action
        self.student_id = student_id
        self.history = history
        self.curr_index = curr_index
        self.curr_student = curr_student
        self.simple_mode = simple_mode
        self.curr_problem = 1

    def next_student(self, ids):
        self.curr_student += 1
        if self.curr_student == len(self.history):
            self.history.append(random.choice(ids))
        self.student_id = self.history[self.curr_student]
        self.curr_index = 0

    def prev_student(self):
        if self.curr_student > 0:
            self.curr_student -= 1
        self.student_id = self.history[self.curr_student]
        self.curr_index = 0

    def next_submission(self, num_submissions):
        if self.curr_index + 1 == num_submissions:
            print("This is the last submission!")
        else:
            self.curr_index += 1

    def prev_submission(self):
        if self.curr_index == 0:
            print("This is the first submission!")
        else:
            self.curr_index -= 1

    def toggle_simple_mode(self):
        self.simple_mode = not self.simple_mode

    def find_id(self, ids):
        student_id = input("Type in a student id (or Enter for random student): ")
        if len(student_id) != 32 or student_id not in ids:
            student_id = random.choice(ids)
        self.student_id = student_id

    def change_problem(self, prob_num):
        self.curr_problem = prob_num
        self.curr_index = 0


def show_progress_bar(state, num_submissions):
    LENGTH = 100
    print("|", end='')
    for i in range(num_submissions):
        if i <= state.curr_index:
            print("=" * (LENGTH // num_submissions), end='')
        else:
            print("-" * (LENGTH // num_submissions), end='')
    print("|")

def read_data(problem):
    print(f"Loading source file for Problem {problem}")
    with open(f'data/p{problem}/sources-{problem}.json') as source_file:
        source_data = json.load(source_file, cls=TreeDecoder)

    print(f"Loading activities map for Problem {problem}")
    with open(f'data/p{problem}/activities-{problem}.json') as activity_file:
        activity_data = json.load(activity_file, cls=TreeDecoder)

    ids = list(activity_data.keys())
    return source_data, activity_data, ids

def run_gui(problems=(1, 2, 4)):
    data: Dict[Tuple] = {}
    for num in problems:
        data[num] = read_data(num)

    _, _, ids = data[1]
    student_id = random.choice(ids)
    state = GUIState(student_id=student_id, history=[student_id])

    prev_problem = 1
    source_data, activity_data, ids = data[state.curr_problem]

    while state.action != SPACE:
        clear()

        if state.curr_problem != prev_problem:
            source_data, activity_data, ids = data[state.curr_problem]
            prev_problem = state.curr_problem

        if state.student_id in activity_data:
            student_submissions = [source_data[str(program_id)] for program_id, _ in activity_data[state.student_id]]
            num_submissions = len(student_submissions)
            problem = student_submissions[state.curr_index]
            program_id, timestamp = activity_data[state.student_id][state.curr_index]
            print("Student id:", state.student_id)
            print("Submission:", state.curr_index+1, "out of", num_submissions)
            print("Timestamp:", timestamp)
            print("Program Rank:", program_id)

            print()
            if state.simple_mode:
                program_tree = autoFormat(problem)
                print(program_tree)
            else:
                print(problem)
            print()

            show_progress_bar(state, num_submissions)
        else:
            print(f"Student had no submission for Problem {state.curr_problem}.")


        state.action = get_action()

        if state.action == ENTER or state.action == NEXT:
            state.next_student(ids)

        elif state.action == UNENTER or state.action == PREV:
            state.prev_student()

        elif state.action == SUBMISSION_RIGHT:
            state.next_submission(num_submissions)

        elif state.action == SUBMISSION_LEFT:
            state.prev_submission()

        elif state.action == FIND_ID:
            state.find_id(ids)

        elif state.action == SIMPLE_MODE_TOGGLE:
            state.toggle_simple_mode()

        elif state.action in (PROBLEM_1, PROBLEM_2, PROBLEM_4, PROBLEM_9):
            if int(state.action) in problems:
                state.change_problem(int(state.action))

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



'''
print(f"Loading count map for Problem {problem}")
with open(f'data/p{problem}/countMap-{problem}.json') as count_file:
    count_data = json.load(count_file, cls=TreeDecoder)

print("Program Rank:", program_id, f"(similar programs:{count_data[str(program_id)]})")


'''
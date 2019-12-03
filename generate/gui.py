from typing import List, Dict, Tuple
import json
import sys
import termios
import tty
import random

SUBMISSION_LEFT = "["
SUBMISSION_RIGHT = "]"
ENTER = "\r"
UNENTER = "\\"
CTRLC = "\x03"
SPACE = " "
NEXT = "n"
PREV = "p"
FIND_ID = "f"
SIMPLE_MODE_TOGGLE = "s"
ALL_POSSIBLE_PROBLEMS = [str(i) for i in range(1, 11)]
INSERT_RUBRIC_ITEM = "i"

ALL_KEYS = ("", SUBMISSION_LEFT, SUBMISSION_RIGHT, SPACE, CTRLC, ENTER,
            UNENTER, NEXT, PREV, FIND_ID, SIMPLE_MODE_TOGGLE,
            *ALL_POSSIBLE_PROBLEMS, INSERT_RUBRIC_ITEM)


class GUIState:
    def __init__(self,
                 problem_data: Dict[int, Tuple],
                 action: str = None,
                 student_id: str = None,
                 history: List = [],
                 curr_index: int = 0,
                 curr_student: int = 0,
                 simple_mode: bool = True,
                 curr_problem: int = -1,
                 submissions: List = []):
        self.problem_data = problem_data
        self.action = action
        self.student_id = student_id
        self.history = history
        self.curr_index = curr_index
        self.curr_student = curr_student
        self.simple_mode = simple_mode
        self.curr_problem = curr_problem
        self.submissions = submissions

    def get_action(self):
        ''' Prints out the prompt and then waits for the user to select an action. '''

        def getch():
            ''' Gets a single character from the user. '''
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        action = None
        prompt = (f"\nType {PREV} or {UNENTER} to see the previous student.\n"
                f"Type {NEXT} or RETURN to see the next student.\n\n"
                f"Type {SUBMISSION_LEFT} to see the previous submission.\n"
                f"Type {SUBMISSION_RIGHT} to see the next submission.\n\n"
                f"Type {FIND_ID} to enter a specific student id.\n\n"
                f"Type {SIMPLE_MODE_TOGGLE} to switch in/out of simple mode.\n\n"
                f"Type {INSERT_RUBRIC_ITEM} to switch in/out of edit mode.\n\n"
                f"Press SPACE to exit!\n\n")
        print(prompt)

        while action not in ALL_KEYS:
            action = getch()
            if action == CTRLC:
                sys.exit()

        self.action = action

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

    def next_submission(self):
        if self.curr_index + 1 == len(self.submissions):
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
        ID_LENGTH = 32
        student_id = input(
            "Type in a student id (or Enter for random student): ")
        if len(student_id) != ID_LENGTH or student_id not in ids:
            student_id = random.choice(ids)
        self.student_id = student_id

    def change_problem(self):
        problem = int(self.action)
        if problem in self.problem_data:
            self.curr_problem = problem
            self.curr_index = 0

    def get_rubric_input(self):
        rubric_numbers = []
        MAX_LINE_LENGTH = 36
        with open('../data/rubric-items.json') as f:
            rubric_items: Dict[List[str]] = json.load(f)
            i = 0
            for category in rubric_items:
                for rubric_item in rubric_items[category]:
                    i += 1
                    rubric_numbers.append(rubric_item)
                    rub = f"{i}. {rubric_item}"
                    print(rub, end=(' ' * (MAX_LINE_LENGTH-len(rub))))
                    if i % 5 == 0:
                        print()

        rubric_line = input("Type in some applicable rubric items: ")
        if rubric_line != '' and rubric_line.isdigit() and int(rubric_line) < len(rubric_numbers):
            student_data = {}
            with open('data/student-rubric.json') as f:
                student_data: Dict[List[str]] = json.load(f)
                if self.student_id not in student_data:
                    student_data[self.student_id] = []
                student_data[self.student_id].append(rubric_numbers[int(rubric_line)-1])

            with open('data/student-rubric.json', 'w') as f:
                json.dump(student_data, f, indent=2)

    def get_problem_data(self):
        return self.problem_data[self.curr_problem]

    def update_state(self, ids):

        if self.action in (ENTER, NEXT):
            self.next_student(ids)

        elif self.action in (UNENTER, PREV):
            self.prev_student()

        elif self.action == SUBMISSION_RIGHT:
            self.next_submission()

        elif self.action == SUBMISSION_LEFT:
            self.prev_submission()

        elif self.action == FIND_ID:
            self.find_id(ids)

        elif self.action == SIMPLE_MODE_TOGGLE:
            self.toggle_simple_mode()

        elif self.action in ALL_POSSIBLE_PROBLEMS:
            self.change_problem()

        elif self.action == INSERT_RUBRIC_ITEM:
            self.get_rubric_input()

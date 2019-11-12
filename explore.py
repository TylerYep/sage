import os
import sys
import json
import random
from tree_encoder import TreeDecoder

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
FIND_ID = "i"
SIMPLE_MODE_TOGGLE =  "s"

ALL_KEYS = ("", SUBMISSION_LEFT, SUBMISSION_RIGHT, SPACE, CTRLC, ENTER,
            UNENTER, NEXT, PREV, FIND_ID, SIMPLE_MODE_TOGGLE)

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
              f"Type {NEXT} or RETURN to see the next student.\n\n")
    prompt += (f"Type {SUBMISSION_LEFT} to see the previous submission.\n"
               f"Type {SUBMISSION_RIGHT} to see the next submission.\n\n")
    prompt += f"Type {FIND_ID} to enter a specific student id.\n\n"
    prompt += f"Type {SIMPLE_MODE_TOGGLE} to switch in/out of simple mode.\n\n"
    prompt += f"Press SPACE to exit!\n\n"
    print(prompt)

    while action not in ALL_KEYS:
        action = getch()
        if action == CTRLC:
            sys.exit()
    return action

def run_gui(problem=1):
    with open(f'data/p{problem}/sources-{problem}.json') as source_file:
        source_data = json.load(source_file, cls=TreeDecoder)

    with open(f'data/p{problem}/countMap-{problem}.json') as count_file:
        count_data = json.load(count_file, cls=TreeDecoder)

    students = {}
    with open(f'data/p{problem}/activities-{problem}.json') as activity_file:
        activity_data = json.load(activity_file, cls=TreeDecoder)
        for student_id in activity_data:
            student_submissions = []
            for program_id, timestamp in activity_data[student_id]:
                student_submissions.append(source_data[str(program_id)])
            students[student_id] = student_submissions


    student_id = input("Type in a student id (or Enter for random student): ")
    ids = list(activity_data.keys())
    if len(student_id) != 32 or student_id not in ids:
        student_id = random.choice(ids)

    action = None
    history = [student_id]
    curr_index, curr_student = 0, 0
    simple_mode = True

    while action != SPACE:
        clear()
        num_submissions = len(students[student_id])
        problem = students[student_id][curr_index]
        program_id, timestamp = activity_data[student_id][curr_index]
        print("Student id:", student_id)
        print("Submission:", curr_index+1, "out of", num_submissions)
        print("Timestamp:", timestamp)
        print("Program Rank:", program_id, f"(similar programs:{count_data[str(program_id)]})")

        print()
        if simple_mode:
            program_tree = autoFormat(problem)
            print(program_tree)
        else:
            print(problem)
        print()

        LENGTH = 100
        print("|", end='')
        for i in range(num_submissions):
            if i <= curr_index:
                print("=" * (LENGTH // num_submissions), end='')
            else:
                print("-" * (LENGTH // num_submissions), end='')
        print("|")

        action = get_action()

        if action == SPACE:
            break

        elif action == ENTER or action == NEXT:
            if curr_student == len(history) - 1:
                student_id = random.choice(ids)
                history.append(student_id)
            curr_student += 1
            student_id = history[curr_student]
            curr_index = 0

        elif action == UNENTER or action == PREV:
            if curr_student > 0:
                curr_student -= 1
            student_id = history[curr_student]
            curr_index = 0

        elif action == SUBMISSION_RIGHT:
            if curr_index + 1 == len(students[student_id]):
                print("This is the last submission!")
            else:
                curr_index += 1

        elif action == SUBMISSION_LEFT:
            if curr_index == 0:
                print("This is the first submission!")
            else:
                curr_index -= 1

        elif action == FIND_ID:
            student_id = input("Type in a student id (or Enter for random student): ")
            ids = list(activity_data.keys())
            if len(student_id) != 32 or student_id not in ids:
                student_id = random.choice(ids)

        elif action == SIMPLE_MODE_TOGGLE:
            simple_mode = not simple_mode

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

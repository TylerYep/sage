

CURR_PROBLEM = 3
LABELS = []

# map from integers to feedback labels
if CURR_PROBLEM == 1:
    LABELS = [
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

elif CURR_PROBLEM == 2:
    LABELS = [
        'noCode',
        'forLoop-wrongLoop',
        'triangle-wrongNumSides',
    ]

elif CURR_PROBLEM == 3:
    LABELS = [
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

elif CURR_PROBLEM == 4:
    LABELS = [
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

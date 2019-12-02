def get_label_to_ix(problem):
    LABELS = get_labels(problem)
    IX_TO_LABEL = {i: label for i, label in enumerate(LABELS)}
    LABEL_TO_IX = dict([[v,k] for k,v in IX_TO_LABEL.items()])
    NUM_LABELS = len(IX_TO_LABEL)
    return LABEL_TO_IX, IX_TO_LABEL, NUM_LABELS

def get_labels(problem):
    ''' map from integers to feedback labels '''
    labels = []
    if problem == 1:
        labels = [
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

    elif problem == 2:
        labels = [
            'noCode',
            'forLoop-wrongLoop',
            'triangle-wrongNumSides',
        ]

    elif problem == 3:
        labels = [
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

    elif problem == 4:
        labels = [
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
    return labels
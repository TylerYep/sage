from ideaToText import Decision

class CreateSquare(Decision):

    def registerChoices(self):
        self.addChoice('makesSquare', {
            'hasSquare': 40,
            'noSquare': 20
        })

        self.addChoice('squareUsesForLoop', {
            'usesLoopForSquare': 40,
            'noLoopForSquare': 20
        })

        self.addChoice('randomOrOneSide', {
            'oneSide': 70,
            'random': 40
        })

    def updateRubric(self):
        if self.getChoice('makesSquare') == 'noSquare':
            self.turnOnRubric('square-none')
        if self.getChoice('squareUsesForLoop') == 'noLoopForSquare':
            self.turnOnRubric('square-unrolled')

    def render(self):
        squareForLoop = self.getChoice('squareUsesForLoop')
        makesSquare = self.getChoice('makesSquare')
        randomOrOneSide = self.getChoice('randomOrOneSide')

        if makesSquare == 'hasSquare':
            if squareForLoop == 'noLoopForSquare':
                return '''
                {DrawSide}
                {DrawSide}
                {DrawSide}
                {DrawSide}
                '''
            else:
                return '''
                    Repeat({NumSides}) {{
                        {DrawSide}
                    }}
                '''
        if randomOrOneSide == 'oneSide':
            return '{DrawSide}'
        return '{ExtraCode}'

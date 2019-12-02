from ideaToText import Decision

class CreateTriangle(Decision):

    def registerChoices(self):
        self.addChoice('makesTriangle', {
            'hasTriangle': 40,
            'noTriangle': 20
        })

        self.addChoice('triangleUsesForLoop', {
            'usesLoopForTriangle': 80,
            'noLoopForTriangle': 1
        })

        self.addChoice('randomOrOneSide', {
            'oneSide': 70,
            'random': 40
        })

    def updateRubric(self):
        if self.getChoice('makesTriangle') == 'noTriangle':
            self.turnOnRubric('triangle-none')
        elif self.getChoice('triangleUsesForLoop') == 'noLoopForTriangle':
            self.turnOnRubric('triangle-unrolled')

    def render(self):
        triangleForLoop = self.getChoice('triangleUsesForLoop')
        makesTriangle = self.getChoice('makesTriangle')
        randomOrOneSide = self.getChoice('randomOrOneSide')

        if makesTriangle == 'hasTriangle':
            if triangleForLoop == 'noLoopForTriangle':
                return '''
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
        return ''

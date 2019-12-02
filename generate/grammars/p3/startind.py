from ideaToText import Decision

class StartInd(Decision):

    def registerChoices(self):
        self.addChoice('startInd', {
            '100': 5,
            '10': 10,
            '20': 80,
            '50': 15,
            '0': 5,
            '1': 2,
            '200': 15,
            '300': 5,
            '25': 1,
            '???': 1,
        })

    def updateRubric(self):
        if self.getChoice('startInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('startInd') != '20':
            self.turnOnRubric('shapeLoopHeader-wrongStart')

    def render(self):
        return self.getChoice('startInd')

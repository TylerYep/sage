from ideaToText import Decision

class StartInd(Decision):

    def registerChoices(self):
        self.addChoice('startInd', {
            '15': 40,
            '10': 15,
            '25': 10,
            '50': 10,
            '0': 10,
            '???': 5
        })

    def updateRubric(self):
        if self.getChoice('startInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('startInd') != '15':
            self.turnOnRubric('shapeLoopHeader-wrongStart')

    def render(self):
        return self.getChoice('startInd')

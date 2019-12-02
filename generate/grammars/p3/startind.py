from ideaToText import Decision

class StartInd(Decision):

    def registerChoices(self):
        self.addChoice('startInd', {
            '15': 20,
            '10': 15,
            '20': 50,
            '25': 10,
            '50': 30,
            '0': 10,
            '300': 20,
            '???': 5
        })

    def updateRubric(self):
        if self.getChoice('startInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('startInd') != '20':
            self.turnOnRubric('shapeLoopHeader-wrongStart')

    def render(self):
        return self.getChoice('startInd')

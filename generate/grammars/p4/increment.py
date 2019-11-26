from ideaToText import Decision

class Increment(Decision):

    def registerChoices(self):
        self.addChoice('increment', {
            '1': 20,
            '15': 60,
            '20': 30,
            '10': 40,
            '20': 10,
            '150': 10,
            '315': 10,
            '???': 5
        })

    def updateRubric(self):
        if self.getChoice('increment') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('increment') != '15':
            self.turnOnRubric('shapeLoopHeader-wrongDelta')


    def render(self):
        return self.getChoice('increment')

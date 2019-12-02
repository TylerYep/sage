from ideaToText import Decision

class Increment(Decision):

    def registerChoices(self):
        self.addChoice('increment', {
            '0': 5,
            '1': 10,
            '5': 1,
            '10': 20,
            '15': 10,
            '20': 80,
            '25': 5,
            '30': 5,
            '150': 5,
            '300': 5,
            '???': 1
        })

    def updateRubric(self):
        if self.getChoice('increment') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('increment') != '20':
            self.turnOnRubric('shapeLoopHeader-wrongDelta')


    def render(self):
        return self.getChoice('increment')

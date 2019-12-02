from ideaToText import Decision

class NumSides(Decision):

    def registerChoices(self):
        self.addChoice('numSides', {
            '0': 40,
            '1' : 10,
            '2' : 40,
            '3': 40,
            '4' : 70,
            '5': 40,
            '6': 1,
            '10': 5,
            '12': 2,
            '15': 5,
            '20': 10,
            'Counter': 1
        })

    def updateRubric(self):
        if self.getChoice('numSides') != '4':
            self.turnOnRubric('square-wrongNumSides')

    def render(self):
        return self.getChoice('numSides')

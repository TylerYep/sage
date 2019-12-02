from ideaToText import Decision

class NumSides(Decision):

    def registerChoices(self):
        self.addChoice('numSides', {
            '0': 10,
            '1' : 10,
            '2' : 10,
            '3': 120,
            '4' : 10,
            '5': 10,
            '6': 1,
            '10': 5,
            '12': 2,
            '15': 5,
            '20': 10,
            '100': 10,
            'Counter': 1
        })

    def updateRubric(self):
        if self.getChoice('numSides') != '3':
            self.turnOnRubric('triangle-wrongNumSides')

    def render(self):
        return self.getChoice('numSides')

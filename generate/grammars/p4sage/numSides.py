from ideaToText import Decision

class NumSides(Decision):

    def registerChoices(self):
        self.addChoice('numSides', {
            '0': 40,
            '1' : 5,
            '2' : 40,
            '3': 40,
            '4' : 70,
            '5': 40,
        })

    def updateRubric(self):
        if self.getChoice('numSides') != '4':
            self.turnOnRubric('square-wrongNumSides')

    def render(self):
        return self.getChoice('numSides')

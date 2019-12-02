from ideaToText import Decision

class NumSides(Decision):

    def registerChoices(self):
        numSides = {str(i): 1 for i in range(11)}
        numSides['3'] = 100
        for x in ('18', '99', '100'):
            numSides[x] = 1
        self.addChoice('numSides', numSides)

    def updateRubric(self):
        if self.getChoice('numSides') != '3':
            self.turnOnRubric('triangle-wrongNumSides')

    def render(self):
        return self.getChoice('numSides')

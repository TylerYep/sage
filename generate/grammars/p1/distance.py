from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        self.addChoice('distance', {
            '50': 40,
            '10' : 10,
            '1' : 10,
            '20': 10,
            '100': 10
        })

    def updateRubric(self):
        if self.getChoice('distance') != 'Counter':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')
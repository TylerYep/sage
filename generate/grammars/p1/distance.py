from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        self.addChoice('distance', {
            '50': 60,
            '10' : 10,
            '1' : 10,
            '15': 2,
            '20': 10,
            '25': 5,
            '100': 10,
            '17': 1,
            '30': 1,
            '40': 1,
        })

    def updateRubric(self):
        if self.getChoice('distance') != '50':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')

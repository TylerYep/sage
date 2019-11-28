from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        self.addChoice('distance', {
            '1': 10,
            '10': 10,
            '15': 2,
            '17': 1,
            '20': 10,
            '25': 5,
            '30': 1,
            '40': 1,
            '50': 60,
            '60': 10,
            '90': 10,
            '100': 10
        })

    def updateRubric(self):
        if self.getChoice('distance') != '50':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')

from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        self.addChoice('distance', {
            'Counter': 50,
            '1': 10,
            '5': 5,
            '10': 10,
            '15': 10,
            '17': 1,
            '20': 10,
            '25': 5,
            '30': 1,
            '40': 1,
            '50': 10,
            '60': 10,
            '90': 10,
            '100': 10,
            '300': 10
        })

    def updateRubric(self):
        if self.getChoice('distance') != 'Counter':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')

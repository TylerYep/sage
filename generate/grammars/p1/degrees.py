from ideaToText import Decision

class Degrees(Decision):

    def registerChoices(self):
        self.addChoice('degrees', {
            '10': 1,
            '15': 1,
            '20': 5,
            '25': 2,
            '30': 10,
            '40': 5,
            '45' : 20,
            '50': 5,
            '60': 20,
            '70': 1,
            '75': 2,
            '80': 2,
            '90': 60,
            '110': 2,
            '115': 2,
            '120': 30,
            '140': 1,
            '145': 1,
            '150': 5,
            '160': 1,
            '180' : 10,
            '240': 5,
            '270' : 50,
            '100': 10,
            '125': 5,
            '130': 5,
            '135': 5
        })

    def updateRubric(self):
        degrees = self.getChoice('degrees')
        if degrees != '90':
            self.turnOnRubric('turn-wrongAmount')

        if degrees == '270' and self.getChoice('turn') == 'TurnLeft':
            self.turnOnRubric('turn-rightLeftConfusion')
        elif degrees == '90' and self.getChoice('turn') == 'TurnRight':
            self.turnOnRubric('turn-rightLeftConfusion')

    def render(self):
        return self.getChoice('degrees')

from ideaToText import Decision

class Degrees(Decision):

    def registerChoices(self):
        self.addChoice('degrees', {
            '30': 10,
            '45' : 20,
            '60': 10,
            '90': 50,
            '120': 10,
            '180' : 10,
            '270' : 50,
            '100': 10
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

from ideaToText import Decision

class Degrees(Decision):

    def registerChoices(self):
        self.addChoice('degrees', {
            '45' : 20,
            '90': 20,
            '120': 80,
            '180' : 10,
            '270' : 10,
            '100': 10,
            'Counter': 10,
        })

    def updateRubric(self):
        degrees = self.getChoice('degrees')
        if degrees != '120':
            self.turnOnRubric('turn-wrongAmount')

        if degrees == '270' and self.getChoice('turn') == 'TurnLeft':
            self.turnOnRubric('turn-rightLeftConfusion')
        elif degrees == '90' and self.getChoice('turn') == 'TurnRight':
            self.turnOnRubric('turn-rightLeftConfusion')

    def render(self):
        return self.getChoice('degrees')

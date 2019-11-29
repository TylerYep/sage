from ideaToText import Decision

class Degrees(Decision):

    def registerChoices(self):
        base_probs = {str(i): (10 if i % 10 == 0 else 1) for i in range(0, 241, 5)}
        for s in ('45', '60', '90', '100', '180', '270'):
            base_probs[s] = 20

        base_probs['120'] = 80 # Correct answer
        self.addChoice('degrees', base_probs)

    def updateRubric(self):
        degrees = self.getChoice('degrees')
        if degrees == '240' and self.getChoice('turn') == 'TurnRight':
            return
            
        if degrees != '120':
            self.turnOnRubric('turn-wrongAmount')

        if self.getChoice('turn') == 'TurnRight':
            self.turnOnRubric('turn-rightLeftConfusion')

    def render(self):
        return self.getChoice('degrees')

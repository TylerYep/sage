from ideaToText import Decision

class RandomProgram(Decision):

    def registerChoices(self):
        self.addChoice('turn', {
            'TurnLeft' : 65,
            'TurnRight': 40
        })

    def updateRubric(self):
        pass

    def render(self):
        return self.getChoice('turn') + '({Degrees})'

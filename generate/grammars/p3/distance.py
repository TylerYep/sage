from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        distances = {str(i): 1 for i in range(0, 100, 10)}
        distances['Counter'] = 100
        distances['100'] = 20
        for s in ('1', '5', '15', '17', '25', '300'):
            distances[s] = 1
        self.addChoice('distance', distances)

    def updateRubric(self):
        if self.getChoice('distance') != 'Counter':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')

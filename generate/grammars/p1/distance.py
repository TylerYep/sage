from ideaToText import Decision

class Distance(Decision):

    def registerChoices(self):
        distances = {str(i): (10 if i % 25 == 0 else 1) for i in range(0, 150, 5)}
        distances['50'] = 60
        for s in ('1', '16', '17'):
            distances[s] = 1
        self.addChoice('distance', distances)

    def updateRubric(self):
        if self.getChoice('distance') != '50':
            self.turnOnRubric('move-wrongAmount')

    def render(self):
        return self.getChoice('distance')

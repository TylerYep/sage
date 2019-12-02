from ideaToText import Decision

class Loop(Decision):

    def registerChoices(self):
        numSides = {}
        numSides['50, 100, 10'] = 100
        for x in ('100, 100, 10',
                  '20, 200, 20',
                  '10, 100, 10',
                  '100, 50, 10',
                  '50, 100, 20',
                  '50, 100, 5',
                  '50, 100, 50',
                  '50, 100, 6',
                  '50, 1000, 10',
                  ):
            numSides[x] = 1
        self.addChoice('loop', numSides)

    def updateRubric(self):
        if self.getChoice('loop') != '50, 100, 10':
            self.turnOnRubric('forLoop-wrongLoop')

    def render(self):
        return self.getChoice('loop')

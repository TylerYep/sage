from ideaToText import Decision

class EndInd(Decision):

    def registerChoices(self):
        self.addChoice('endInd', {
            '300': 5,
            '100': 10,
            '20': 15,
            '10': 10,
            '200': 70,
            '???': 1,
            '500': 1,
            '400': 1,
            '1': 1,
            '40': 1,
            '120': 1,
            '150': 1,
        })

    def updateRubric(self):
        if self.getChoice('endInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('endInd') != '200':
            self.turnOnRubric('shapeLoopHeader-wrongEnd')

    def render(self):
        return self.getChoice('endInd')

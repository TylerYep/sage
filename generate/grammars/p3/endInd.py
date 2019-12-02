from ideaToText import Decision

class EndInd(Decision):

    def registerChoices(self):
        self.addChoice('endInd', {
            '300': 10,
            '100': 20,
            '315': 10,
            '15': 20,
            '200': 70,
            '???': 5,
            '500': 1,
            '400': 1
        })

    def updateRubric(self):
        if self.getChoice('endInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('endInd') != '200':
            self.turnOnRubric('shapeLoopHeader-wrongEnd')

    def render(self):
        return self.getChoice('endInd')

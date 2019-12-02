from ideaToText import Decision

class EndInd(Decision):

    def registerChoices(self):
        self.addChoice('endInd', {
            '300': 70,
            '150': 20,
            '315': 10,
            '15': 20,
            '200': 10,
            '???': 5,
            '500': 1,
            '400': 1
        })

    def updateRubric(self):
        if self.getChoice('endInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('endInd') != '300':
            self.turnOnRubric('shapeLoopHeader-wrongEnd')

    def render(self):
        return self.getChoice('endInd')

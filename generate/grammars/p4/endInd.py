from ideaToText import Decision

class EndInd(Decision):

    def registerChoices(self):
        self.addChoice('endInd', {
            '300': 50,
            '150': 20,
            '315': 10,
            '15': 5,
            '200': 5,
            '???': 5
        })

    def updateRubric(self):
        if self.getChoice('endInd') == '???':
            self.turnOnRubric('shapeLoopHeader-missingValue')
        elif self.getChoice('endInd') != '300':
            self.turnOnRubric('shapeLoopHeader-wrongEnd')

    def render(self):
        return self.getChoice('endInd')

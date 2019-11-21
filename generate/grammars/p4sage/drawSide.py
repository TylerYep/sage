from ideaToText import Decision

class DrawSide(Decision):

    def registerChoices(self):
        self.addChoice('hasCode', {
            'noCode': 40,
            'code' : 60
        })
        self.addChoice('moveVsTurnFirst', {
            'moveFirst': 40,
            'turnFirst': 20
        })

        self.addChoice('sideExtraCode', {
            'noExtraCode': 95,
            'extraCode': 5
        })

        self.addChoice('hasLeft', {
            'forgotLeft': 80,
            'hasLeft': 20
        })

        self.addChoice('hasMove', {
            'forgotMove': 80,
            'hasMove': 20
        })

    def updateRubric(self):
        if self.getChoice('hasCode') == 'noCode':
            self.turnOnRubric('side-none')
        else:
            if self.getChoice('moveVsTurnFirst') == 'turnFirst':
                self.turnOnRubric('side-wrongMoveLeftOrder')

            if self.getChoice('sideExtraCode') == 'extraCode':
                self.turnOnRubric('side-armsLength')

            if self.getChoice('hasLeft') == 'forgotLeft':
                self.turnOnRubric('side-forgotLeft')

            if self.getChoice('hasMove') == 'forgotMove':
                self.turnOnRubric('side-forgotMove')

    def render(self):
        moveVsTurnFirst = self.getChoice('moveVsTurnFirst')
        extra = '{ExtraCode}' if self.getChoice('sideExtraCode') else ''
        hasTurn = '{Turn}\n' if self.getChoice('hasLeft') else ''
        hasMove = 'Move({Distance})\n' if self.getChoice('hasMove') else ''

        if moveVsTurnFirst == 'moveFirst':
            return hasMove + hasTurn + extra
        else:
            return hasTurn + hasMove + extra


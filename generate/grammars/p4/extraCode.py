from ideaToText import Decision

class ExtraCode(Decision):

    def registerChoices(self):
        self.addChoice('extraCode', {
            '': 80,
            'move': 50,
            'turn' : 40
        })
        self.addChoice('extraCode2', {
            '': 60,
            'move': 50,
            'turn' : 40
        })
        self.addChoice('extraCode3', {
            '': 60,
            'move': 50,
            'turn' : 40
        })

    def updateRubric(self):
        if self.getChoice('extraCode') != '' \
            and self.getChoice('extraCode2') != '' \
            and self.getChoice('extraCode3') != '':
            self.turnOnRubric('square-armsLength')

    def render(self):
        def get_ans(extraCode):
            if extraCode == 'move':
                return 'Move({Distance}) '
            if extraCode == 'turn':
                return '{Turn} '
            return ''
        extraCode = self.getChoice('extraCode')
        extraCode2 = self.getChoice('extraCode2')
        extraCode3 = self.getChoice('extraCode3')
        if self.hasChoice('outerForLoop') and self.getChoice('outerForLoop') == 'noOuterForLoop':
            return get_ans(extraCode) + get_ans(extraCode2) + get_ans(extraCode3)
        else:
            return get_ans(extraCode)

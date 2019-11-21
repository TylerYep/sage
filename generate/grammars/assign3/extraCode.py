from ideaToText import Decision

class ExtraCode(Decision):

    def registerChoices(self):
        self.addChoice('extraCode', {
            '': 60,
            'move': 50,
            'turn' : 40,
            'moreCode': 5
        })

    def updateRubric(self):
        pass

    def render(self):
        extraCode = self.getChoice('extraCode')
        moreStuff = '' #'{ExtraCode}'
        if extraCode != '':
            if extraCode == 'move':
                return 'Move({Distance}) ' + moreStuff
            if extraCode == 'turn':
                return '{Turn} ' + moreStuff
        return ''
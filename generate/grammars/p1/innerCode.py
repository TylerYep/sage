from ideaToText import Decision
from ideaToText import generatorUtils as gu

# "Start" is a special decision which is invoked by the Sampler
# to generate a single sample.
class InnerCode(Decision):

    def registerChoices(self):
        self.addChoice('code', {
            '': 2,
            'move': 50,
            'turn' : 50
        })
        self.addChoice('code2', {
            '': 20,
            'move': 50,
            'turn' : 50
        })
        self.addChoice('code3', {
            '': 50,
            'move': 50,
            'turn' : 50
        })

        self.addChoice('mixedUpOrder', {
            'rightOrder': 80,
            'wrongOrder': 20
        })

        self.addChoice('sameChoice', {
            'same': 50,
            'different': 50
        })

    def updateRubric(self):
        if self.getChoice('code') != '' \
            and self.getChoice('code2') != '' \
            and self.getChoice('code3') != '':
            self.turnOnRubric('triangle-armsLength')

    def render(self):
        def get_ans(code):
            if code == 'move':
                return 'Move({Distance}) '
            if code == 'turn':
                return '{Turn} '
            return ''
        code = self.getChoice('code')
        code2 = self.getChoice('code2')
        code3 = self.getChoice('code3')
        if self.hasChoice('hasRepeat') and self.getChoice('hasRepeat') == 'noRepeat':
            if self.getChoice('sameChoice') == 'same':
                return get_ans(code) * 5

            return get_ans(code) + get_ans(code2) + get_ans(code) + get_ans(code2) + get_ans(code)
        else:
            return get_ans(code) + get_ans(code2) + get_ans(code3)

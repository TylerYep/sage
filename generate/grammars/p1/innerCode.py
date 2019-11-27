from ideaToText import Decision
from ideaToText import generatorUtils as gu

# "Start" is a special decision which is invoked by the Sampler
# to generate a single sample.
class InnerCode(Decision):

    def registerChoices(self):
        self.addChoice('code', {
            '': 2,
            'move': 70,
            'turn' : 50
        })
        self.addChoice('code2', {
            '': 20,
            'move': 50,
            'turn' : 70
        })
        self.addChoice('code3', {
            '': 70,
            'move': 50,
            'turn' : 50
        })

        self.addChoice('mixedUpOrder', {
            'rightOrder': 80,
            'wrongOrder': 20
        })

        self.addChoice('manyChoice', {
            'one': 50,
            'two': 50,
            'three': 30,
            'five': 20,
            'many': 30
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
        # if self.hasChoice('hasRepeat') and self.getChoice('hasRepeat') == 'noRepeat':
        if self.getChoice('manyChoice') == 'one':
            return get_ans(code)
        if self.getChoice('manyChoice') == 'two':
            return get_ans(code) + get_ans(code2)
        if self.getChoice('manyChoice') == 'three':
            return get_ans(code) + get_ans(code2) + get_ans(code)
        if self.getChoice('manyChoice') == 'five':
            return get_ans(code) + get_ans(code2) + get_ans(code) + get_ans(code2) + get_ans(code)
        else:
            return get_ans(code) + get_ans(code2) + get_ans(code3)

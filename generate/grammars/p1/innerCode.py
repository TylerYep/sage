import random

from ideaToText import Decision
from ideaToText import generatorUtils as gu

# "Start" is a special decision which is invoked by the Sampler
# to generate a single sample.
class InnerCode(Decision):

    def registerChoices(self):
        self.addChoice('turnOrMove', {
            'move': 50,
            'turn' : 50
        })
        self.addChoice('extra1', {
            'move': 50,
            'turn' : 50
        })
        self.addChoice('includesRandomExtra', {
            'hasExtraAction': 10,
            'reusesSameActions': 70
        })
        self.addChoice('mixedUpOrder', {
            'rightOrder': 80,
            'wrongOrder': 20
        })
        self.addChoice('pattern', {
            'oneLine': 50,
            'twoLines': 50,
            'threeLines': 30,
            'fourLines' : 10,
            'fiveLines': 20,
            'none': 20
        })

    def updateRubric(self):
        if self.getChoice('pattern') in ('threeLines', 'fourLines'):
            self.turnOnRubric('triangle-tooManyActions')

        elif self.getChoice('pattern') == 'fiveLines':
            if self.hasChoice('hasRepeat') and self.getChoice('hasRepeat') == 'noRepeat':
                self.turnOnRubric('triangle-tooManyActions')

        elif self.getChoice('mixedUpOrder') == 'wrongOrder':
            self.turnOnRubric('triangle-wrongMoveTurnOrder')

        elif self.getChoice('turnOrMove') == 'move' and self.getChoice('pattern') == 'oneLine':
            self.turnOnRubric('side-forgotTurn')

        elif self.getChoice('turnOrMove') == 'move' and self.getChoice('pattern') == 'oneLine':
            self.turnOnRubric('side-forgotMove')

    def render(self):
        def get_action(code):
            if code == 'move':
                return 'Move({Distance}) '
            if code == 'turn':
                return '{Turn} '
            return ''

        move = get_action('move')
        turn = get_action('turn')

        if self.getChoice('pattern') == 'oneLine':
            return turn if self.getChoice('turnOrMove') == 'turn' else move

        if self.getChoice('pattern') == 'twoLines':
            if self.getChoice('mixedUpOrder') == 'rightOrder':
                return move + turn
            else:
                return turn + move

        order = [move, turn]
        random.shuffle(order)
        a, b = order

        if self.getChoice('pattern') == 'threeLines':
            if self.getChoice('includesRandomExtra') == 'reusesSameActions':
                return a + b + a
                
            extra1 = get_action(self.getChoice('extra1'))
            return a + b + extra1

        if self.getChoice('pattern') == 'fourLines':
            return a + b + a + b

        if self.getChoice('pattern') == 'fiveLines':
            return a + b + a + b + a

        return ''

from ideaToText import Decision
from ideaToText import generatorUtils as gu

# "Start" is a special decision which is invoked by the Sampler
# to generate a single sample.
class Repeat(Decision):

    def registerChoices(self):
        self.addChoice('times', {
            '0' : 30,
            '1': 40,
            '2' : 10,
            '3' : 40,
            '4': 10,
            '5': 10,
            '???': 5,
            '50': 1
        })

    def updateRubric(self):
        if self.getChoice('times') != '3':
            self.turnOnRubric('triangle-wrongNumSides')

    def render(self):
        times = self.getChoice('times')
        return '''
            Repeat(''' + times + ''') {{
                {InnerCode}
            }}'''

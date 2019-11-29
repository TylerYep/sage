from ideaToText import Decision
from ideaToText import generatorUtils as gu

# "Start" is a special decision which is invoked by the Sampler
# to generate a single sample.
class Start(Decision):

    def registerChoices(self):
        self.addChoice('codeOrNo', {
            'code': 100,
            'noCode': 5
        })
        self.addChoice('completeProblemFirstTry', {
            'firstTry': 50,
            'notFirstTry': 50
        })
        self.addChoice('hasRepeat', {
            'yesRepeat': 50,
            'noRepeat': 50
        })

    def updateRubric(self):
        if self.getChoice('codeOrNo') == 'code':
            if self.getChoice('hasRepeat') == 'noRepeat':
                self.turnOnRubric('missingRepeat')
        else:
            self.turnOnRubric('noCode')

    def render(self):
        if self.getChoice('codeOrNo') == 'code':
            if self.getChoice('hasRepeat') == 'yesRepeat':
                return '{Repeat}'
            else:
                return '{InnerCode}'
        else:
            return ''

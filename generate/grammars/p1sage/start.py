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
            'firstTry': 100,
            'notFirstTry': 5
        })

    def updateRubric(self):
        if self.getChoice('codeOrNo') == 'code':
            self.turnOnRubric('triesBlocks')


    def render(self):
        # 

        return '{CreateSquare}'

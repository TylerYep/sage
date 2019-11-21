from ideaToText import Decision
from ideaToText import generatorUtils as gu
import json
from .tree_encoder import TreeDecoder
from  codeDotOrg.treeToString import autoFormat

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
            self.turnOnRubric('hasCode')

    def render(self):
        with open('p1/sources-1.json') as f:
            source_data = json.load(f, cls=TreeDecoder)
            random_program = source_data["0"]
            print(random_program)

        if self.getChoice('codeOrNo') == 'noCode':
            return ''
        # if self.getChoice('completeProblemFirstTry') == 'firstTry':
        #     return '{Solution}'
        return random_program

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
        self.addChoice('outerForLoop', {
            'hasOuterForLoop': 80,
            'noOuterForLoop': 20
        })
        self.addChoice('mixedUpOrder', {
            'rightOrder': 80,
            'wrongOrder': 20
        })
        self.addChoice('sideOrTriangle', {
            'side': 80,
            'triangle': 20
        })
        self.addChoice('forLoopVars', {
            'none': 20,
            'some': 95
        })

    def updateRubric(self):
        if self.getChoice('codeOrNo') == 'noCode':
            self.turnOnRubric('no-code')
        else:
            if self.getChoice('outerForLoop') == 'noOuterForLoop':
                self.turnOnRubric('shapeLoop-none')
                if self.getChoice('mixedUpOrder') == 'wrongOrder':
                    self.turnOnRubric('shapeLoopHeader-wrongOrder')

    def render(self):
        if self.getChoice('codeOrNo') == 'noCode':
            return ''

        if self.getChoice('outerForLoop') == 'hasOuterForLoop':
            if self.getChoice('mixedUpOrder') == 'rightOrder':
                return '''
                For({StartInd}, {EndInd}, {Increment}) {{
                   {CreateTriangle}
                }}
                '''
            if self.getChoice('forLoopVars') == 'none':
                if self.getChoice('sideOrTriangle') == 'side':
                    return '''
                    For(???, ???, ???) {{
                        {DrawSide}
                    }}
                    '''
                return '''
                For(???, ???, ???) {{
                   {CreateTriangle}
                }}
                '''
            return '''
            For({StartInd}, {Increment}, {EndInd}) {{
               {CreateTriangle}
            }}
            '''

        if self.getChoice('sideOrTriangle') == 'side':
            return '{DrawSide}'
        return '{CreateTriangle}'

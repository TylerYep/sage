from .autoIndent import autoIndent

def flatten_tree(tree):
    flat = ['(', tree.rootName]
    for child in tree.children:
        if child:
            flat += flatten_tree(child)
    flat.append(')')

    return flat


def removeColors(tree):
    for child in tree.children:
        removeColors(child)

    newChildren = []
    for child in tree.children:
        if child.rootName != 'SetColor':
            newChildren.append(child)

    tree.children = newChildren


def autoFormat(tree):
    assert tree.rootName == 'Program'
    newline = "\n"

    def recurseOnChildren(tree, separator="", startChild=0):
        return separator.join([_autoFormat(next) for next in tree.children[startChild:]])

    def _autoFormat(tree):
        name = tree.rootName
        if name in ('Program', 'WhenRun', 'Value', 'Color', 'Number', 'Variable'):
            if tree.children:
                return recurseOnChildren(tree)
            return ''

        if name in ('Move', 'Turn', 'SetColor'):
            return f'{name}({recurseOnChildren(tree, separator=", ")})'

        if name == 'Repeat':
            times = ''
            if tree.children:
                times = _autoFormat(tree.children[0])
            return (f'Repeat({times}) {{\n'
                    f'{recurseOnChildren(tree, startChild=1)}\n}}')

        if name == 'Body':
            return (f'{recurseOnChildren(tree, separator=newline)}')

        if name == 'For':
            if len(tree.children) < 3:
                return (f'For() {{\n'
                        f'{recurseOnChildren(tree)}\n}}')
            return (f'For({_autoFormat(tree.children[0])}, '
                    f'{_autoFormat(tree.children[1])}, '
                    f'{_autoFormat(tree.children[2])}) {{\n'
                    f'{recurseOnChildren(tree, startChild=3)}\n}}')

        if name == 'Arithmetic':
            op = tree.children[0].rootName
            sign = '_'
            if op == 'Add':
                sign = '+'
            elif op == 'Subtract':
                sign = '+'
            elif op == 'Multiply':
                sign = 'x'
            elif op == 'Divide':
                sign = '/'
            if len(tree.children) > 2:
                return (f'({_autoFormat(tree.children[1])} {sign} {_autoFormat(tree.children[2])})')
            return (f'(_ {sign} _)')

        return name # 6fbf9cf0406cc709e93a037a894d6e62

    result = recurseOnChildren(tree, '\n')
    return autoIndent(result)

    # assert name in ('Left', 'Right', 'Forward', 'Backward', 'RandomColor', '???') \
    #     or name.isnumeric() \
    #     or name.ishex()

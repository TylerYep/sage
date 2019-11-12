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
        if name in ('Program', 'WhenRun', 'Value', 'Color', 'Number'):
            return _autoFormat(tree.children[0])

        if name in ('Move', 'Turn', 'SetColor'):
            return f'{name}({recurseOnChildren(tree, separator=", ")})'

        if name == 'Repeat':
            return (f'Repeat({_autoFormat(tree.children[0])}) {{\n'
                    f'{recurseOnChildren(tree, startChild=1)}\n}}')

        if name == 'Body':
            return (f'{recurseOnChildren(tree, separator=newline)}')

        # print(f"{tree.rootName}\n")
        # assert name in ('Left', 'Right', 'Forward', 'Backward', 'RandomColor', '???') \
        #     or name.isnumeric() \
        #     or name.ishex()
        return name

    result = recurseOnChildren(tree, '\n', 1)
    return autoIndent(result)

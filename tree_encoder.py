import json
from models import Tree

class TreeEncoder(json.JSONEncoder):
    def default(self, o):
        ''' Overrides encoding method. '''
        if isinstance(o, Tree):
            return {'type': 'Tree',
					'data': {'rootName': o.rootName, 'children': o.children}
					}
        return json.JSONEncoder.default(self, o)


class TreeDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.json_to_objects)

    @staticmethod
    def json_to_objects(obj):
        ''' Implements decoding method. '''
        if 'type' not in obj:
            return obj
        obj_type = obj['type']
        del obj['type']

        if obj_type == 'Tree':
        	return get_object_initializer(obj_type)(**obj)

        return obj


def get_object_initializer(obj_name: str):
    ''' Retrieves class initializer from its string name. '''
    return getattr(sys.modules[__name__], obj_name)
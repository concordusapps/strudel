from .Parser import Parse


class Vobj(object):

    def __init__(self, vobj):
        self.parse(vobj)

    def parse(self, vobj):
        # Check if a string was provided, and assume its a path
        if isinstance(vobj, str):
            vobj = open(vobj)

        y = Parse(vobj)
        objects = y.parse()

        for k, v in objects.items():
            setattr(self, k, v)


    def vformat(self, version=2.1):

        for attr in self.__dict__:
            
            if callable(attr):
                continue

            if isinstance(attr, list):
                for subattr in attr:
                    yield subattr.vformat() + '\n'

            yield attr.vformat() + '\n'



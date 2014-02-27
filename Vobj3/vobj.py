from .Parser import Parse


class Vobj(object):

    def __init__(self, vobj):
        self.parse(vobj)

    def parse(self, vobj):
        if isinstance(vobj, str):
            vobj = open(vobj)

        y = Parse(vobj)
        objects = y.parse()

        for k, v in objects.items():
            setattr(self, k, v)

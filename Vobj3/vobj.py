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

    def export(self):
        """Write the Vobj back to a file
        Warning! Current version will overwrite vcards for
        people with the same 'Fn' field"""

        # Sets filename to The formatted name string associated with the vCard
        filename = str(self.fn[0]) + '.vcf'

        # if p.isfile('./' + filename):
        #     filename + 'copy'

        target = open(filename, 'w+')

        target.write('BEGIN:VCARD\n')

        # Get list of vobj fields
        members = [attr for attr in dir(self) if not callable(attr) and not (
            attr.startswith("__"))]

        # blah = [attr for attr in members if attr[0] != defaultdict(list)]

        members.remove('Items')
        members.remove('parse')
        members.remove('export')

        for attr in members:
            # if hasattr(self, attr):
            target.write(getattr(self, attr)[0].vformat())

        # for attr in vobj.__dict__.items():
        #     if hasattr(vobj, str(attr)):
        #         target.write(getattr(vobj, str(attr))[0].vformat() + '\n')

        target.write('END:VCARD\n')
        target.close()

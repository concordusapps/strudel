
class VcardExporter():
    """Write the Vobj back to a file"""

    def export_to_file(vobj):
        """Warning! Current version will overwrite vcards for
        people with the same 'Fn' field"""

        # Sets filename to The formatted name string associated with the vCard
        filename = str(vobj.fn[0]) + '.vcf'

        # if p.isfile('./' + filename):
        #     filename + 'copy'

        target = open(filename, 'w+')

        target.write('BEGIN:VCARD\n')

        # Get list of vobj fields
        members = [attr for attr in dir(vobj) if not callable(attr) and not (
            attr.startswith("__"))]

        # blah = [attr for attr in members if attr[0] != defaultdict(list)]

        members.remove('Items')
        members.remove('parse')

        for attr in members:
            target.write(getattr(vobj, attr)[0].vformat() + '\n')

        # for attr in vobj.__dict__.items():
        #     if hasattr(vobj, str(attr)):
        #         target.write(getattr(vobj, str(attr))[0].vformat() + '\n')

        target.write('END:VCARD\n')

        target.close()

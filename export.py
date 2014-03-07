class VcardExporter():
    """Write the Vobj back to a file"""

    def export_to_file(vobj):

        filename = str(vobj.fn[0])

        target = open(filename, 'w+')

        target.write('BEGIN:VCARD\n')

        target.write(vobj.version[0].vformat() + '\n')
        target.write(vobj.n[0].vformat() + '\n')
        target.write(vobj.fn[0].vformat() + '\n')
        target.write(vobj.org[0].vformat() + '\n')
        target.write(vobj.tel[0].vformat() + '\n')
        target.write(vobj.bday[0].vformat() + '\n')
        target.write(vobj.tel[0].vformat() + '\n')
        target.write(vobj.photo[0].vformat() + '\n')
        # target.write(vobj.impp[0].vformat() + '\n')

        target.close()

from io import StringIO
import Fields


class Parse():
    """Parse the Vcard, the idea is that the parser returns something like this

        [
            {
                "BEGIN": {
                    "attributes": [],
                    "kvattr": {},
                    "value": ["VCARD"]
                }
            }
            {
                "VERSION": {
                    "attributes": [],
                    "kvattr": {},
                    "value": ["2.1"]
                }
            }
            {
                "N": {
                    "attributes": [],
                    "kvattr": {
                        "language": "en-us"
                    },
                    "value": ["Doge", "Snoop", "C", "Rapper", "Jr"]
                }
            }
            {
                "FN": {
                    "attributes": [],
                    "kvattr": {},
                    "value": ["Rapper Snoop C Doge Jr"]
                }
            }

        ]

        etc etc

    """

    def __init__(self, vobj):
        self.vcard = vobj
        self.data = []
        self.buff = []
        self

    def parse(self):
        objects = {}
        for key, attributes, dictofattrs, value in self.parse_attr(self.vcard):
            self.data.append({key: {"kvattr": dictofattrs,
                                    "attributes": [a for a in attributes],
                                    "value": value.split(";")}})

            # Dynamic creation of Field objects
            if key.title() not in ("Begin", "Rev", "End"):
                field_type = getattr(Fields, key.title())

                objects[key.lower()] = field_type([a for a in attributes],
                                                  dictofattrs, value, key)

        return objects

    def parse_attr(self, vcard):
        buf = StringIO()
        for line in self.vcard:
            key, sattrs, kwatters, value = self.splitattrs(line.strip())

            # When the encoding type is quoted-printable, this means
            # That there will be a line cont. sequence in the line
            # So here, we check for the encoding type, and merge any
            # Line that ends in "=0D=0A=", with the next one, until
            # The sequence is not found
            if kwatters.get('encoding') == 'quoted-printable':
                buf.write(value)
                while True:

                    next_line = self.vcard.readline().strip()
                    buf.write(next_line)
                    if not next_line.endswith("=0D=0A="):
                        value = buf.getvalue().replace("=0D=0A=", "")
                        buf.seek(0)
                        buf.truncate()
                        break
            yield key, sattrs, kwatters, value

    def splitattrs(self, line):
        names, value = line.split(':', 1)
        source_attrs = names.split(';')

        # Attributes are split into 2 types: declared and key/value
        key = source_attrs.pop(0)
        attrs = set()
        kwattrs = {}
        for attr in source_attrs:
            if "=" in attr:
                kwkey, kwvalue = attr.split("=", 1)
                kwattrs[kwkey.lower()] = kwvalue.lower()
            else:
                attrs.add(attr.lower())

        return key, attrs, kwattrs, value

    def serialize(self, key, attributes, value):
        self.data.append({key: {"Values": value, "attributes": attributes}})

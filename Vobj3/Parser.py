from io import StringIO
from . import Fields
from collections import defaultdict


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
        self.buff = defaultdict(list)

    def parse(self):
        objects = defaultdict(list)
        for key, attributes, dictofattrs, value in self.parse_attr(self.vcard):
            # Dynamic creation of Field objects
            # Make sure we don't get begin, rev, or end, since they are not
            # fields that contain important data
            if key.title() not in ("Begin", "Rev", "End", "Prodid"):

                # Go through the fields module, and use the name of the key to
                # find our class, and create a link to it.
                field_type = getattr(Fields, key.title())

                # Here we actually instantiate the field, and throw it in to
                # a dictionary, in order for the Vobj class to iterate and
                # use setattr() to itself.
                values = objects[key.lower()]

                values.append(field_type(list(attributes),
                                         dictofattrs,
                                         value.split(";"),
                                         key))
        objects['Items'] = self.buff

        return objects

    def parse_attr(self, vcard):
        buf = StringIO()
        for line in self.vcard:
            key, sattrs, kwattrs, value = self.splitattrs(line.strip())

            # There is probably a better place to put this, but w/e
            # Basically, if we come across an "item", we will catch it
            # and store it
            # for later parsing, after the file is fully parsed
            if key.startswith('item'):
                item, key = key.split('.')
                self.buff[item].append({key: value})
                # Continue on to the next line
                continue

            # When the encoding type is quoted-printable, this means
            # That there will be a line cont. sequence in the line
            # So here, we check for the encoding type, and merge any
            # Line that ends in "=0D=0A=", with the next one, until
            # The sequence is not found. "OD" and "OA" are the carriage return
            # and line feed character in hexadecimal.

            if kwattrs.get('encoding') == 'quoted-printable':
                buf.write(value)
                while True:

                    next_line = self.vcard.readline().strip()
                    buf.write(next_line)
                    if not next_line.endswith("=0D=0A="):
                        value = buf.getvalue().replace("=0D=0A=", "")
                        buf.seek(0)
                        buf.truncate()
                        break
            # yield key, sattrs, kwattrs, value

            # Check if its a b64 encoded value, "b" in vcard 3
            if kwattrs.get('encoding') in ('base64', 'b'):
                # Yes? write the line to a buffer,
                # since its probably more than one line
                buf.write(value)
                # Keep iterating through each line until we get what we want
                while True:
                    next_line = self.vcard.readline().replace("\n", "")
                    # import ipdb; ipdb.set_trace()
                    buf.write(next_line)
                    # In this case, we want to check if the line does not start
                    # With a space, or an indention.
                    if not next_line.startswith(" "):
                        # set the value of the field to the b64
                        value = buf.getvalue()
                        # Return the file to its original state before we
                        # Started fucking around with it
                        buf.seek(0)
                        buf.truncate()
                        break

            yield key, sattrs, kwattrs, value

    ###
    # A function that splits key value attributes, from single attributes,
    # i.e, "PREF"(Single) vs "ENCODING=PRINTABLE"(Key-Value)
    # And returns they key(string), attributes(string), kwattributes(dict), and
    # The value of the field (string)
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

    # A function that does absolutely nothing (yet)
    def serialize(self, key, attributes, value):
        self.data.append({key: {"Values": value, "attributes": attributes}})

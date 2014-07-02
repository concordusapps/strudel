from . import Fields
from collections import defaultdict
from io import StringIO


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
        vcards = []
        for key, attributes, dictofattrs, value in self.parse_attr(self.vcard):
            # Dynamic creation of Field objects

            if key.title() == "Begin":
                objects = defaultdict(list)
            # Make sure we don't get begin, rev, or end, since they are not
            # fields that contain important data
            if key.title() not in ("Begin", "Rev", "End", "Prodid"):

                try:
                    # Go through the fields module, and use the name of the key to
                    # find our class, and create a link to it.
                    field_type = getattr(Fields, key.title())

                except AttributeError:
                    continue

                # Here we actually instantiate the field, and throw it in to
                # a dictionary, in order for the Vobj class to iterate and
                # use setattr() to itself.
                values = objects[key.lower()]

                values.append(field_type(list(attributes),
                                         dictofattrs,
                                         value.split(";"),
                                         key))

            if key.title() == "End":
                vcards.append(objects)

        #Check if items is an empty default dict, if so, we dont need it
        if not isinstance(self.buff, defaultdict):
            objects['Items'] = self.buff

        return vcards

    def parse_attr(self, vcard):
        buf = StringIO()
        last_line = None
        vcf_iter = iter(self.vcard)
        while True:
            if last_line is not None:
                line = last_line
                last_line = None
            else:
                line = next(vcf_iter)
                if not line:
                    break

            # Remove the trailing newline and whitespace.
            line = line.strip("\n").strip()

            # Ignore blank lines.
            if not line:
                continue

            # We need to pull the next lines into us if they start with
            # a space, because that apparently is the spec.
            while True:
                try:
                    last_line = next(vcf_iter)
                    if last_line[0] == " ":
                        line += last_line.strip()
                    else:
                        break

                except StopIteration:
                    break

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
                if kwkey.lower() == 'type':
                    if 'type' not in kwattrs:
                        kwattrs['type'] = [kwvalue.lower()]
                    else:
                        kwattrs['type'] += [kwvalue.lower()]
                else:
                    kwattrs[kwkey.lower()] = kwvalue.lower()
            else:
                attrs.add(attr.lower())

        return key, attrs, kwattrs, value

    # A function that does absolutely nothing (yet)
    def serialize(self, key, attributes, value):
        self.data.append({key: {"Values": value, "attributes": attributes}})

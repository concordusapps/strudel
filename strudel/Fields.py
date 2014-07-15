class FieldTypes:

    def __init__(self, attr=None, kvattr=None, val=None, key=None):
        self.attributes = attr or []
        self.kvattributes = kvattr or {}
        self.values = val
        self.is_preferred = False
        self.key = key or type(self).__name__.upper()
        if self.attributes is not None:
            self.parse_attributes()

    def parse_attributes(self):
        self.is_preferred = False
        if "pref" in self.attributes:
            self.is_preferred = True
            del self.attributes[self.attributes.index("pref")]
            self.types = self.values

    # Vcard spec says to fold lines after 75 characters, this checks and does
    # just that.
    def fold(self, line):
        if len(line) <= 75:
            return line

        lines = "\r\n ".join([line[i:i + 75] for i in range(0, len(line), 75)])

        return lines

    def vformat(self, version="2.1"):
        kvattr = ''

        for key, value in self.kvattributes.items():
            if key == 'type':
                for x in value:
                    kvattr += ";%s=%s" % (key.upper(), x.upper())
            else:
                kvattr += ";%s=%s" % (key.upper(), value.upper())

        attr = ";".join([x.upper() for x in self.attributes])
        values = ";".join(self.values)
        if attr or kvattr:
            if attr:
                attr = ";" + attr
            return self.fold("%s%s%s:%s\r\n" % (self.key, attr, kvattr,
                                                values))
        else:
            return self.fold("%s:%s\r\n" % (self.key, values))

    def __str__(self):
        # Return the value on str(object)
        return ", ".join([x for x in self.values if x])

    def __repr__(self):
        return "<Vcard %s Field Object>" % self.__class__.__name__

    # A type for Apple style Vcards (3.0), which allows unique naming of
    # fields, This is simply a class for figuring out, as well as parsing the
    # field under normal means of sanitation, and having a storage place for
    # it, while waiting for more items class Item:

    # In this case, key will be "item.x"
    # def parse_all_attributes(self):
        # for attribute, value in self.__dict__.items():


class Impp(FieldTypes):

    """Instant Messaging and Presence Protocol"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.photo = self.values[0]


class Bday(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.photo = self.values[0]


class Photo(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.photo = self.values[0]

    def __str__(self):
        return self.values[0]

    def __repr__(self):
        return self.values[0]


class Version(FieldTypes):

    """The version of the vCard specification."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.version = self.values[0]


class N(FieldTypes):

    """A structured representation of the name of the person, place or thing
    associated with the vCard """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.n = " ".join(self.values)


class Fn(FieldTypes):

    """The formatted name string associated with the vCard"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.full_name = self.values[0]


class Org(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.name = self.values[-1]
        # self.unit = [self.values[1:]]


class Title(FieldTypes):

    """Specifies the job title, functional position or function of the
    individual associated with the vCard """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tel(FieldTypes):

    """Telephone field object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def append(self, phone_number='', name=''):
        self.attributes.append(name)
        self.attributes.append(phone_number)


class Adr(FieldTypes):

    """ The address field, the value will always follow
        the following:
             the post office box;
             the extended address (e.g., apartment or suite number);
             the street address;
             the locality (e.g., city);
             the region (e.g., state or province);
             the postal code;
             the country name (full name in the language specified in
             Section 5.1).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     self.parse_address()

    # def parse_address(self):
    #     params = ['post_office', 'extended', 'address', 'locality', 'region',
    #               'zipcode', 'country']
    #     for attribute, value in zip(params, self.values):
    #         setattr(self, attribute, value)


class Label(FieldTypes):

    """Represents the actual text that should be put on the mailing label
    when delivering a physical package to the person/object associated with
    the vCard (related to the ADR property)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Url(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.url = self.values[-1]


class Email(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.email = self.values[-1]

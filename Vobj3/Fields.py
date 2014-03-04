class FieldTypes():

    def __init__(self, attr=None, kvattr=None, val=None, key=None):
        self.attributes = attr
        self.kvattributes = kvattr
        self.values = val
        self.is_preferred = False
        self.key = key
        self.parse_attributes()

    def parse_attributes(self):
        self.is_preferred = False
        if "pref" in self.attributes:
            self.is_preferred = True
            del self.attributes[self.attributes.index("PREF")]
            self.types = self.values

    def vformat(self):
        kvattr = ";".join(["%s=%s" % (key.upper(), value.upper())
                           for key, value in self.kvattributes.items()])

        if kvattr:
            kvattr = ";" + kvattr

        attr = ";".join([x.upper() for x in self.attributes])
        values = ";".join(self.values)
        return "%s;%s%s:%s" % (self.key, attr, kvattr, values)

    def __str__(self):
        # Return the value on str(object)
        return ", ".join([x for x in self.values if x])

    def __repr__(self):
        return "<Vcard %s Field Object>" % self.__class__.__name__


class Version(FieldTypes):
    """The version of the vCard specification."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = self.values[0]


class Prodid(FieldTypes):
    """The identifier for the product that created the vCard object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prodid = self.values[0]


class N(FieldTypes):
    """A structured representation of the name of the person, place or thing
    associated with the vCard """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = " ".join(self.values)


class Fn(FieldTypes):
    """The formatted name string associated with the vCard"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_name = self.values[0]


class Org(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.values[-1]
        self.unit = [self.values[1:]]


class Title(FieldTypes):
    """Specifies the job title, functional position or function of the
    individual associated with the vCard """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = self.values[0]


class Tel(FieldTypes):
    """Telephone field object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
        self.parse_address()

    def parse_address(self):
        params = ['post_office', 'extended', 'address', 'locality', 'region',
                  'zipcode', 'country']
        for attribute, value in zip(params, self.values):
            setattr(self, attribute, value)


class Label(FieldTypes):
    """Represents the actual text that should be put on the mailing label
    when delivering a physical package to the person/object associated with
    the vCard (related to the ADR property)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Url(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.values[-1]


class Email(FieldTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = self.values[-1]

from .Parser import Parse
from . import Fields
from collections.abc import Sequence
from io import StringIO


class NamedMutator:

    def __init__(self, data, class_, indicies):
        self._data = data
        self._class_ = class_
        self._indicies = indicies

    def __str__(self):
        return str(self._data)

    def __dir__(self):
        return super().__dir__() + list(self._indicies.keys())

    def __getattr__(self, name):
        try:
            return self._data[0].values[self._indicies[name]]

        except (IndexError, KeyError):
            raise AttributeError

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
            return

        try:
            if not self._data:
                self._data[0:0] = [self._class_()]
                self._data[0].values = [''] * len(self._indicies)

            self._data[0].values[self._indicies[name]] = value

        except KeyError:
            raise AttributeError()


class VCard:

    # Create a simple map.
    _simple_map = {
        "full_name": {
            "key": "fn",
            "scalar": True,
            "class": Fields.Fn
        },
        "title": {
            "key": "title",
            "scalar": True,
            "class": Fields.Title
        },
        "organization": {
            "key": "org",
            "scalar": True,
            "class": Fields.Org
        },
    }

    def __init__(self, data=None, version="2.1"):
        #! The data contained in the vcard object.
        self._data = data or {}

        #! The version of the vcard.
        self.version = version

    @staticmethod
    def parse(source):
        # Handle being passed a filename.
        managed = False
        if isinstance(source, str):
            managed = True
            source = open(source, "r")

        try:
            # Parse the source to yield vcards.
            m = Parse(source)
            data = m.parse()

        except:
            # Just re-raise the exception, we don't give three fucks.
            raise

        finally:
            # Destroy the file handle if we managed the creation of it.
            if managed:
                source.close()

        # Turns the list of data and into a list of VCards
        vcards = []
        for card in data:
            vcards.append(VCard(card))

        # Store the data in a new vcard and return it.
        return vcards

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = value

    def __dir__(self):
        return super().__dir__() + list(self._simple_map.keys())

    def __getattr__(self, name):
        try:
            item = self._simple_map[name]
            if item['scalar']:
                return str(self._data[item['key']][0])

        except (KeyError, IndexError):
            return None

    def __setattr__(self, name, value):
        # Short-circuit if we're a thing.
        if name in self.__dict__ or name not in self._simple_map:
            self.__dict__[name] = value
            return

        try:
            item = self._simple_map[name]
            if item['scalar']:

                if item['key'] not in self._data:
                    self._data[item['key']] = data = item['class']()

                else:
                    data = self._data[item['key']]
                    if isinstance(data, Sequence):
                        data = data[0]

                data.values = [value]

        except KeyError:
            raise AttributeError

    @property
    def photo(self):
        if 'PHOTO' not in self._data:
            self._data['PHOTO'] = []

        return self._data['PHOTO'][0]

    @property
    def name(self):
        if 'N' not in self._data:
            self._data['N'] = []

        return NamedMutator(self._data['N'], Fields.N, {
            "last": 0,
            "first": 1,
            "middle": 2,
            "prefix": 3,
            "suffix": 4})

    def __iter__(self):
        # Yield prologue
        yield "BEGIN:VCARD\n"

        # Yield version initially.
        # yield self._data['version'][0].vformat()

        for name, value in self._data.items():

            # Version was already provided; skip.
            if name == 'version':
                continue

            if isinstance(value, Sequence):
                for sub in value:
                    yield sub.vformat(self.version)
                    # yield "\n"

            else:
                yield value.vformat(self.version)
                # yield "\n"

        # Yield epilogue
        yield "END:VCARD\n"

    def __str__(self):
        io = StringIO()
        for chunk in self:
            io.write(chunk)
        io.seek(0)
        return io.read()

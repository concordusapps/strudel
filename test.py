# -*- coding: utf-8 -*-
from Vobj3 import vobj


class TestVobj:

    def __init__(self):
        self.setup()

    def setup(self):

        with open('Vobj3/vcard_v3', 'r') as file:
            data = file.read()

        return data

    def testParse(self, data):
        x = vobj.Vobj(data)
        # import ipdb; ipdb.set_trace()

testobj = TestVobj()
dump = testobj.setup()
testobj.testParse(dump)

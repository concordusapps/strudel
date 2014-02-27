# -*- coding: utf-8 -*-
from Vobj3 import vobj


class TestVobj:

    def __init__(self):
        self.setup()

    def setup(self):
        fixture = 'Vobj3/vcard_v3'
        return open(fixture)

    def testParse(self, data):
        testobj = TestVobj()
        vobj.Vobj(testobj.setup())

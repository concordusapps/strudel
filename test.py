# -*- coding: utf-8 -*-
from export import VcardExporter
from Vobj3.vobj import Vobj

vcard2_1 = 'Vobj3/fixtures/vcard_v2.1'
vcard3_0 = 'Vobj3/fixtures/vcard_v3.0'

# x = Vobj(vcard3_0)
x = Vobj(vcard2_1)

VcardExporter.export_to_file(x)

import ipdb
ipdb.set_trace()

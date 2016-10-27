from unittest import TestCase
from ESXiHost import *
from ESXiHost import *

import logging
from pySimpleVmCtrl import ESXiHost

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class TestESXiHostClass(TestCase):
    def test_esxihost(self):
        h = ESXiHostClass('192.168.1.2','root','password')
        assert len(h.get_datastores() ) > 0
        assert len(h.get_networks() ) > 0
        assert len(h.get_guests() ) > 0

    def test_esxiclass(self):
        h = ESXiHostClass('192.168.1.2','root','password')


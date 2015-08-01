import os
import unittest
import libcnml
import datetime


DATA = {
    54284: {
        'zones': 1,
        'nodes': 27,
        'devices': 48,
        'services': 5,
        'radios': 42,
        'interfaces': (
            82382, 82389, 82390, 82391, 82392, 82393, 82443, 82444, 82445,
            82450, 82496, 86317, 86326, 86327, 87464, 87465, 87466, 87467,
            88596, 88598, 88602, 93284, 96778, 97141, 101085, 101159, 101160,
            102429, 102430, 102431, 102436, 102437, 102442, 102448, 102716,
            102718, 102890, 102891, 108647, 126097, 127016, 127925, 132688,
            134455, 134456, 134457, 134778, 135000, 135633, 136954, 137582,
            139291, 139295, 139297, 139302, 140559, 141248, 141385, 141389,
            141390, 142165, 142603, 142898, 143505,

        ),
        'links': (
            121882, 122468, 122570, 122663, 122909, 123391, 123628, 124201,
            124205, 124624, 124894, 124949, 124950, 125214, 125364, 125468,
            125700, 54362, 54363, 54364, 54365, 54408, 54449, 57313, 57320,
            58265, 58271, 59133, 59137, 65511, 65799, 69092, 70212, 70213,
            70214, 70216, 70220, 70226, 70400, 70402, 70551, 70552, 74307,
            79959, 80238, 80531,
        ),
        'ip': {
            'address': '10.69.12.1',
            'title': 'ANDGkPlzUdala',
        },
    },
    55284: {
        'zones': 1,
        'nodes': 6,
        'devices': 18,
        'services': 4,
        'radios': 12,
        'interfaces': (
            104955, 104957, 84178, 84179, 84185, 84228, 84246, 84248, 84273,
            84274, 84275, 84276, 84319, 84328, 84459, 84460, 84462, 84463,
            84464, 84469, 84470, 96341, 96342, 96343, 96347, 96348, 96349,
            96727, 96728, 97283, 97284,
        ),
        'links': (
            55732, 55735, 55767, 55784, 55785, 55789, 55797, 55817, 55818,
            55897, 55898, 55899, 55902, 55904, 65136, 65138, 65140, 65141,
            65469, 65471, 65919, 65920, 72156, 72158,
        ),
        'ip': {
            'address': '10.69.28.1',
            'title': 'TOLOOiaun',
        },
    },
    2525: {
        'zones': 1,
        'nodes': 14,
        'devices': 14,
        'services': 9,
        'radios': 10,
        'interfaces': (
            77127, 81573, 82624, 82626, 82630, 82631, 82641, 82664, 83515, 83516, 84998, 86420, 86955, 102790, 120315, 123115,
        ),
        'links': (
            54559, 54560, 54568, 54589, 55264, 55265, 55341, 56317, 57394,
            57846, 70459, 78121, 78999,
        ),
        'ip': {
            'address': '10.138.53.101',
            'title': 'CanetCuba',
        },
    }
}


class EmptyFileTestCase(unittest.TestCase):
    def test_invalid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/empty.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertFalse(parser.loaded)


class ValidationTestCase(unittest.TestCase):
    def test_valid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/54284.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertTrue(parser.loaded)

    def test_invalid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/54284_invalid.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertFalse(parser.loaded)


class LibcnmlTestCase(unittest.TestCase):
    cnml_file = 'data/54284.cnml'
    data = DATA[54284]

    def setUp(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.cnml_file
        )
        self.parser = libcnml.CNMLParser(filename)

    def test_findNodefromIPv4(self):
        node = self.parser.findNodefromIPv4(self.data['ip']['address'])
        self.assertTrue(node is not None)
        self.assertEqual(node.title, self.data['ip']['title'])

    def test_getNodes(self):
        nodes = self.parser.getNodes()
        self.assertEqual(len(nodes), self.data['nodes'])

    def test_getZones(self):
        zones = self.parser.getZones()
        self.assertEqual(len(zones), self.data['zones'])

    def test_getDevices(self):
        devices = self.parser.getDevices()
        self.assertEqual(len(devices), self.data['devices'])

    def test_getServices(self):
        services = self.parser.getServices()
        self.assertEqual(len(services), self.data['services'])

    def test_getRadios(self):
        radios = self.parser.getRadios()
        self.assertEqual(len(radios), self.data['radios'])

    def test_getInterfaces(self):
        interfaces = self.parser.getInterfaces()
        for iface in interfaces:
            self.assertIn(iface.id, self.data['interfaces'])

        self.assertEqual(len(interfaces), len(self.data['interfaces']))

    def test_getLinks(self):
        links = self.parser.getLinks()
        for link in links:
            self.assertIn(link.id, self.data['links'])
        self.assertEqual(len(links), len(self.data['links']))


class LibcnmlUrlTestCase(LibcnmlTestCase):
    """
    Same as LibcnmlTestCase but get CNML from URL
    instead of from local file
    """
    cnml_url = 'https://raw.githubusercontent.com/PabloCastellano/libcnml/master/libcnml/tests/data/54284.cnml'

    def setUp(self):
        self.parser = libcnml.CNMLParser(self.cnml_url)
        if not self.parser.loaded:
            raise ValueError('could not load CNMLParser')


class LibcnmlNodeAttributesTestCase(LibcnmlTestCase):
    cnml_file = 'data/54284.cnml'

    def setUp(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.cnml_file
        )
        self.parser = libcnml.CNMLParser(filename)

    def test_node_title(self):
        node = self.parser.getNode(48441)
        self.assertEqual(node.title, 'ANDBerria38')

    def test_node_antenna_elevation(self):
        node = self.parser.getNode(48441)
        self.assertEqual(node.antenna_elevation, 12)

    def test_node_created(self):
        node = self.parser.getNode(48441)
        self.assertIsInstance(node.created, datetime.datetime)
        self.assertEqual(node.created.strftime('%Y-%m-%d %H:%M'), '2012-05-23 06:47')

    def test_node_updated(self):
        node = self.parser.getNode(48441)
        self.assertIsInstance(node.updated, datetime.datetime)
        self.assertEqual(node.updated.strftime('%Y-%m-%d %H:%M'), '2014-11-20 11:35')


class Zone55284TestCase(LibcnmlTestCase):
    cnml_file = 'data/55284.cnml'
    data = DATA[55284]


class Zone2525TestCase(LibcnmlTestCase):
    cnml_file = 'data/2525.cnml'
    data = DATA[2525]

if __name__ == '__main__':
    unittest.main()

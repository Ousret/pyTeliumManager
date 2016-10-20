import unittest
from TeliumManager.telium import Telium

class TestTPE(unittest.TestCase):
    def test_demande_paiement(self):
        kTeliumClient = Telium(1, True, False, '/dev/tty.usbmodem1411')
        self.assertEqual(kTeliumClient.demandePaiement(0.5), True)


if __name__ == '__main__':
    unittest.main()

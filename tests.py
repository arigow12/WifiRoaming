import unittest
from io import StringIO
import sys
from unittest.mock import patch, mock_open
from AccessPoint import AccessPoint
from Client import Client
from ParseInput import ParseInput
from AC import AC_controller


class TestAccessPoint(unittest.TestCase):

    def setUp(self):
        self.ap = AccessPoint(
            name="AP1", x=0, y=0, channel=6, power=20, freq=2.4, standard="WiFi6",
            y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
        )

    def test_rssi_calculation_within_coverage(self):
        rssi = self.ap.get_rssi(10, 10)
        self.assertNotEqual(rssi, float('-inf'))

    def test_rssi_calculation_out_of_coverage(self):
        rssi = self.ap.get_rssi(100, 100)
        self.assertEqual(rssi, float('-inf'))

    def test_connect_client_success(self):
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, -70)
        connected = self.ap.connect_client(client)
        self.assertTrue(connected)
        self.assertIn(client, self.ap.all_clients)

    def test_connect_client_failure_due_to_limit(self):
        for i in range(5):
            client = Client(f"Client{i}", 10, 10, "WiFi6", 1, True, True, True, -70)
            self.ap.connect_client(client)
        extra_client = Client("Client6", 10, 10, "WiFi6", 1, True, True, True, -70)
        connected = self.ap.connect_client(extra_client)
        self.assertFalse(connected)

    def test_disconnect_client(self):
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, -70)
        self.ap.connect_client(client)
        self.ap.remove_client(client)
        self.assertNotIn(client, self.ap.all_clients)

    def test_process_roaming(self):
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, -70)
        self.ap.process_roaming(client)
        self.assertIn(client, self.ap.all_clients)

    def test_give_channel_indicator(self):
        self.ap.give_channel_indicator(11)
        self.assertEqual(self.ap.channel, 11)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, -70)
        self.ap = AccessPoint(
            name="AP1", x=0, y=0, channel=6, power=20, freq=2.4, standard="WiFi6",
            y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
        )

    def test_move_client(self):
        self.client.move(20, 20)
        self.assertEqual(self.client.client_x, 20)
        self.assertEqual(self.client.client_y, 20)

    def test_associate_with_ap(self):
        self.client.associate_with_ap(self.ap)
        self.assertEqual(self.client.connected_ap, self.ap)

    def test_disassociate_from_ap(self):
        self.client.associate_with_ap(self.ap)
        self.client.disassociate_from_ap()
        self.assertIsNone(self.client.connected_ap)

    def test_assess_roaming_options(self):
        another_ap = AccessPoint(
            name="AP2", x=20, y=20, channel=11, power=25, freq=2.4, standard="WiFi6",
            y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
        )
        self.client.associate_with_ap(self.ap)
        self.client.assess_roaming_options([self.ap, another_ap])
        self.assertEqual(self.client.connected_ap, another_ap)


class TestACController(unittest.TestCase):

    def setUp(self):
        self.ap1 = AccessPoint(
            name="AP1", x=0, y=0, channel=6, power=20, freq=2.4, standard="WiFi6",
            y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
        )
        self.ap2 = AccessPoint(
            name="AP2", x=20, y=20, channel=6, power=20, freq=2.4, standard="WiFi6",
            y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
        )
        self.ac = AC_controller([self.ap1, self.ap2])

    def test_change_channel_due_to_conflict(self):
        self.ac.change_channel()
        self.assertNotEqual(self.ap1.channel, self.ap2.channel)

    def test_change_memory(self):
        self.ap1.give_channel_indicator(11)
        self.ap2.give_channel_indicator(1)
        logs = self.ac.change_memory()
        self.assertIn("Step: AC REQUIRES AP1 TO CHANGE CHANNEL TO 11", logs)
        self.assertIn("Step: AC REQUIRES AP2 TO CHANGE CHANNEL TO 1", logs)


class TestParseInput(unittest.TestCase):

    def setUp(self):
        self.parser = ParseInput()

    @patch('builtins.open', new_callable=mock_open, read_data="AP AP1 0 0 6 20 2.4 WiFi6 true true true 50 5\nCLIENT Client1 10 10 WiFi6 1 true true true -70\nMOVE Client1 15 15\n")
    def test_parse_input_file(self, mock_open):
        self.parser.input_parse("dummy_filename")
        self.assertEqual(len(self.parser.access_points), 1)
        self.assertEqual(len(self.parser.clients), 1)
        self.assertEqual(len(self.parser.occurs), 1)

    def tearDown(self):
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()

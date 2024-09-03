import unittest
from io import StringIO
import sys
from AccessPoint import AccessPoint
from Client import Client
from ParseInput import ParseInput
from AC import AC_controller
import tempfile


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
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, 10)
        connected = self.ap.connect_client(client)
        self.assertTrue(connected)
        self.assertIn(client, self.ap.all_clients)

    def test_connect_client_failure_due_to_limit(self):
        for i in range(5):
            client = Client(f"Client{i}", 10, 10, "WiFi6", 1, True, True, True, 10)
            self.ap.connect_client(client)

        extra_client = Client("Client6", 10, 10, "WiFi6", 1, True, True, True, 10)
        connected = self.ap.connect_client(extra_client)
        self.assertFalse(connected)

    def test_disconnect_client(self):
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, 10)
        self.ap.connect_client(client)
        self.ap.remove_client(client)
        self.assertNotIn(client, self.ap.all_clients)

    def test_process_roaming(self):
        client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, 10)
        self.ap.process_roaming(client)
        self.assertIn(client, self.ap.all_clients)

    def test_give_channel_indicator(self):
        self.ap.give_channel_indicator(11)
        self.assertEqual(self.ap.channel, 11)


# class TestClient(unittest.TestCase):
#
#     def setUp(self):
#         self.client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, 10)
#         self.ap = AccessPoint(
#             name="AP1", x=0, y=0, channel=6, power=20, freq=2.4, standard="WiFi6",
#             y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
#         )
#
#     def test_move_client(self):
#         self.client.move(20, 20)
#         self.assertEqual(self.client.client_x, 20)
#         self.assertEqual(self.client.client_y, 20)
#
#     def test_associate_with_ap(self):
#         self.client.associate_with_ap(self.ap)
#         self.assertIsNotNone(self.client.connected_ap, "Client should be connected to AP")
#
#     def test_disassociate_from_ap(self):
#         self.client.associate_with_ap(self.ap)
#         self.client.disassociate_from_ap()
#         self.assertIsNone(self.client.connected_ap)
#
#     def test_assess_roaming_options(self):
#         another_ap = AccessPoint(
#             name="AP2", x=20, y=20, channel=11, power=25, freq=2.4, standard="WiFi6",
#             y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
#         )
#         self.client.associate_with_ap(self.ap)
#         self.client.assess_roaming_options([self.ap, another_ap])
#         self.assertIsNotNone(self.client.connected_ap, "Client should have roamed to another AP")
#         self.assertEqual(self.client.connected_ap, another_ap, "Client should have roamed to the optimal AP")

class TestClient(unittest.TestCase):
    class TestClient(unittest.TestCase):

        def setUp(self):
            self.client = Client("Client1", 10, 10, "WiFi6", 1, True, True, True, -70)
            self.ap = AccessPoint(
                name="AP1", x=0, y=0, channel=6, power=20, freq=2.4, standard="WiFi6",
                y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
            )
            # Capturing print output
            self.held_stdout = StringIO()
            sys.stdout = self.held_stdout

        def tearDown(self):
            # Reset stdout
            sys.stdout = sys.__stdout__

        def test_associate_with_ap(self):
            self.client.associate_with_ap(self.ap)
            self.assertIsNotNone(self.client.connected_ap, "Client should be connected to AP")

        def test_assess_roaming_options(self):
            another_ap = AccessPoint(
                name="AP2", x=20, y=20, channel=11, power=25, freq=2.4, standard="WiFi6",
                y_11k=True, y_11v=True, y_11r=True, radius=50, device_limit=5
            )
            self.client.associate_with_ap(self.ap)
            self.client.assess_roaming_options([self.ap, another_ap])
            self.assertIsNotNone(self.client.connected_ap, "Client should have roamed to another AP")


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

    def test_parse_input_file(self):
        test_input = (
            "AP AP1 0 0 6 20 2.4 WiFi6 true true true 50 5\n"
            "CLIENT Client1 10 10 WiFi6 1 true true true 10\n"
            "MOVE Client1 15 15\n"
        )
        with tempfile.NamedTemporaryFile('w+', delete=False) as temp_file:
            temp_file.write(test_input)
            temp_file.seek(0)
            self.parser.input_parse(temp_file.name)

        self.assertEqual(len(self.parser.access_points), 1)
        self.assertEqual(len(self.parser.clients), 1)
        self.assertEqual(len(self.parser.occurs), 1)

    def test_simulation_execution(self):
        test_input = (
            "AP AP1 0 0 6 20 2.4 WiFi6 true true true 50 5\n"
            "CLIENT Client1 10 10 WiFi6 1 true true true 10\n"
            "MOVE Client1 15 15\n"
        )
        with tempfile.NamedTemporaryFile('w+', delete=False) as temp_file:
            temp_file.write(test_input)
            temp_file.seek(0)
            self.parser.input_parse(temp_file.name)

        output = StringIO()
        sys.stdout = output
        self.parser.execute_simulation()
        sys.stdout = sys.__stdout__  # Reset stdout after the test

        expected_output = [
            "Step 1: Client1 CONNECT TO AP1 WITH SIGNAL STRENGTH",
            "Step 1: Client1 DISCONNECT FROM AP1 WITH SIGNAL STRENGTH",
            "Step 1: Client1 ROAM TO AP1"
        ]
        for line in expected_output:
            self.assertIn(line, output.getvalue())

    def tearDown(self):
        # Reset stdin and stdout
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()

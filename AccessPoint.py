import math

class AccessPoint:
    def __init__(self, name, x, y, channel, power, freq, standard, y_11k, y_11v, y_11r,
                 radius, device_limit, rssi=0):
        self.name = name
        self.x = x
        self.y = y
        self.channel = channel
        self.power = power
        self.freq = freq
        self.standard = standard
        self.y_11k = y_11k
        self.y_11v = y_11v
        self.y_11r = y_11r
        self.radius = radius
        self.device_limit = device_limit
        self.rssi = rssi
        self.all_clients = []
        self.memory = []


    def get_rssi(self, x_client, y_client):
        distance = self._calculate_distance(x_client, y_client)
        if self._is_out_of_coverage(distance):
            return float('-inf')
        return self._calculate_rssi(distance)

    def _calculate_distance(self, x_client, y_client):
        """Calculates the Euclidean distance between the AP and the client."""
        return math.sqrt((self.x - x_client) ** 2 + (self.y - y_client) ** 2)

    def _is_out_of_coverage(self, distance):
        """Checks if the client is out of the AP's coverage radius."""
        return distance > self.radius

    def _calculate_rssi(self, distance):
        """Calculates the RSSI based on the distance and frequency."""
        return self.power - 20 * math.log10(distance) - 20 * math.log10(self.freq) - 32.44


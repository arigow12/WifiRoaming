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
        return math.sqrt((self.x - x_client) ** 2 + (self.y - y_client) ** 2)

    def _is_out_of_coverage(self, distance):
        return distance > self.radius

    def _calculate_rssi(self, distance):
        return self.power - 20 * math.log10(distance) - 20 * math.log10(self.freq) - 32.44

    def connect_client(self, client):
        if self._can_connect_client(client):
            self._add_client(client)
            self._log_connection(client)
            return True
        else:
            self._log_denial(client)
            return False

    def _can_connect_client(self, client):
        return len(self.all_clients) < self.device_limit and client not in self.all_clients

    def _add_client(self, client):
        self.all_clients.append(client)

    def _log_connection(self, client):
        self.memory.append(
            f"Step {client.step}: {client.name} CONNECT TO {self.name} WITH SIGNAL STRENGTH {client.current_rssi}")

    def _log_denial(self, client):
        self.memory.append(f"Step {client.step}: {client.name} TRIED {self.name} BUT WAS DENIED")

    def remove_client(self, client):
        if self.is_client_connected(client):
            self.remove_client_from_list(client)
            self.log_removal(client)

    def is_client_connected(self, client):
        return client in self.all_clients

    def remove_client_from_list(self, client):
        self.all_clients.remove(client)

    def log_removal(self, client):
        self.memory.append(f"Step {client.step}: {client.name} DISCONNECT FROM {self.name} WITH SIGNAL STRENGTH {client.current_rssi}")


    def process_roaming(self, client):
        can_connect = len(self.all_clients) < self.device_limit
        if can_connect:
            roaming_type = "FAST ROAM TO" if self.y_11r else "ROAM TO"
            self.memory.append(f"Step {client.step}: {client.name} {roaming_type} {self.name}")
            return self.connect_client(client)

        self.memory.append(f"Step {client.step}: {client.name} TRIED {self.name} BUT WAS DENIED")
        return False

    def give_channel_indicator(self, new_channel):
        self.channel = new_channel
        self.memory.append(f"Step: AC REQUIRES {self.name} TO CHANGE CHANNEL TO {new_channel}")

    def get_mem(self):
        return self.memory
class Client:
    def __init__(self, client_name, client_x, client_y, standard, speed, y_11k, y_11v, y_11r,
                 rssi):
        self.y_11k = y_11k
        self.y_11v = y_11v
        self.y_11r = y_11r
        self.name = client_name
        self.wifi = standard
        self.speed = speed
        self.rssi = rssi
        self.aps = None
        self.curr_rssi = float('-inf')
        self.count = 0
        self.client_x = client_x
        self.client_y = client_y

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.step += 1

    def associate_with_ap(self, access_point):
        self.current_rssi = self._get_rssi_from_ap(access_point)
        if self._meets_minimal_rssi():
            self._update_connected_ap(access_point)
            access_point.connect_client(self)

    def _get_rssi_from_ap(self, access_point):
        """Calculates the RSSI from the given access point based on current client location."""
        return access_point.calculate_rssi(self.client_x, self.client_y)

    def _meets_minimal_rssi(self):
        """Checks if the current RSSI meets the minimal required RSSI for connection."""
        return self.current_rssi >= self.min_rssi

    def _update_connected_ap(self, access_point):
        """Updates the current connected access point."""
        self.connected_ap = access_point


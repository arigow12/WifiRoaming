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
        self.connected_ap = None
        self.curr_rssi = float('-inf')
        self.count = 0
        self.client_x = client_x
        self.client_y = client_y

    def move(self, new_x, new_y):
        self.client_x = new_x
        self.client_y = new_y
        self.count += 1

    def associate_with_ap(self, access_point):
        self.curr_rssi = self._get_rssi_from_ap(access_point)
        if self._meets_minimal_rssi():
            self._update_connected_ap(access_point)
            access_point.connect_client(self)


    def _get_rssi_from_ap(self, access_point):
        return access_point.calculate_rssi(self.client_x, self.client_y)

    def _meets_minimal_rssi(self):
        return self.curr_rssi >= self.rssi

    def _update_connected_ap(self, access_point):
        self.connected_ap = access_point

    def disassociate_from_ap(self):
        if self._is_connected_to_ap():
            self._remove_client_from_current_ap()
            self._reset_connected_ap()

    def _is_connected_to_ap(self):
        return self.connected_ap is not None

    def _remove_client_from_current_ap(self):
        self.connected_ap.remove_client(self)

    def _reset_connected_ap(self):
        self.connected_ap = None

    def assess_roaming_options(self, available_aps):
        optimal_ap = self._find_optimal_ap(available_aps)
        if self._should_roam(optimal_ap):
            self._roam_to(optimal_ap)

    def _find_optimal_ap(self, aps):
        best_ap = None
        best_rssi = float('-inf')

        for ap in aps:
            rssi = ap.get_rssi(self.client_x, self.client_y)
            if self._is_ap_eligible(ap, rssi, best_rssi):
                best_rssi = rssi
                best_ap = ap

        return best_ap

    def _is_ap_eligible(self, ap, rssi, best_rssi):
        return rssi > best_rssi and rssi >= self.rssi and self._is_ap_compatible(ap)

    def _should_roam(self, ap):
        return ap and ap != self.connected_ap

    def _roam_to(self, new_ap):
        self.disassociate_from_ap()
        self.associate_with_ap(new_ap)

    def _is_ap_compatible(self, ap):
        return self.wifi in ap.standard

    def fetch_connection_logs(self):
        return self.connected_ap.get_mem() if self._is_connected_to_ap() else []

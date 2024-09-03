class ParseInput:

    def __init__(self):
        self.access_points = []
        self.clients = []
        self.occurs = []

    def input_parse(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                inputs = line.split()
                input_type = inputs[0]
                if input_type == "AP":
                    self.execute_ap(inputs)
                elif input_type == "CLIENT":
                    self.execute_client(inputs)
                elif input_type == "MOVE":
                    self.execute_move(inputs)

    def execute_ap(self, inputs):
        e_ap = AccessPoint(
            ap_name = inputs[1],
            x = int(inputs[2]),
            y = int(inputs[3]),
            channel = int(inputs[4]),
            power = int(inputs[5]),
            freq = float(inputs[6]),
            standard = inputs[7],
            y_11k = inputs[8].lower() == 'true',
            y_11v = inputs[9].lower() == 'true',
            y_11r = inputs[10].lower() == 'true',
            radius = int(inputs[11]),
            device_limit = int(inputs[12]),
            rssi = int(inputs[13]) if len(inputs) > 13 else 0
        )
        self.access_points.append(e_ap)



    def execute_client(self, inputs):
        client = Client(
            name=inputs[1],
            x=int(inputs[2]),
            y=int(inputs[3]),
            standard=inputs[4],
            speed=int(inputs[5]),
            y_11k=inputs[6].lower() == 'true',
            y_11v=inputs[7].lower() == 'true',
            y_11r=inputs[8].lower() == 'true',
            rssi=int(inputs[9])
        )
        self.clients.append(client)

    def execute_move(self, inputs):
        move_type, client_name, new_x, new_y = inputs[0], inputs[1], int(inputs[2]), int(inputs[3])
        self.occurs.append((move_type, client_name, new_x, new_y))

    def execute_simulation(self):
        """Executes the simulation by processing events, moving clients, evaluating roaming, and managing AP channels."""
        for event in self.occurs:
            self._process_event(event)

        self.ac.manage_ap_channels()  # Manages channel assignments for APs
        self._record_simulation_results()  # Logs the simulation results

    def _process_event(self, event):
        """Processes a single event by moving the client and evaluating roaming options."""
        action, client_name, new_x, new_y = event
        client = self._get_client_by_name(client_name)
        client.move(new_x, new_y)
        client.assess_roaming_options(self.aps)

    def _get_client_by_name(self, client_name):
        """Retrieves a client object by its name."""
        return next(c for c in self.clients if c.name == client_name)

    def _record_simulation_results(self):
        """Logs the results of the simulation."""
        self._log_results()

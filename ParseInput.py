class ParseInput:

    def __init__(self):
        self.access_points = []
        self.clients = []
        self.occurs = []
        self.ac = None

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

        self.ac = AC_controller(self.access_points)

    def execute_ap(self, inputs):
        e_ap = AccessPoint(
            name=inputs[1],
            x=int(inputs[2]),
            y=int(inputs[3]),
            channel=int(inputs[4]),
            power=int(inputs[5]),
            freq=float(inputs[6]),
            standard=inputs[7],
            y_11k=inputs[8].lower() == 'true',
            y_11v=inputs[9].lower() == 'true',
            y_11r=inputs[10].lower() == 'true',
            radius=int(inputs[11]),
            device_limit=int(inputs[12]),
            rssi=int(inputs[13]) if len(inputs) > 13 else 0
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
        for event in self.occurs:
            self._process_event(event)
        self.ac.change_channels()
        self._record_simulation_results()

    def _process_event(self, event):
        action, client_name, new_x, new_y = event
        client = self._get_client_by_name(client_name)
        client.move(new_x, new_y)
        client.assess_roaming_options(self.access_points)

    def _get_client_by_name(self, client_name):
        return next(c for c in self.clients if c.name == client_name)

    def _record_simulation_results(self):
        logs = []
        for client in self.clients:
            logs.extend(client.fetch_connection_logs())
        logs.extend(self.ac.change_memory())
        for log in logs:
            print(log)

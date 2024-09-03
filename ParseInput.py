class ParseInput:

    def __init__(self):
        self.access_points = []

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

    def execute_move(self, inputs):

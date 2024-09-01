class ParseInput:

    def __init__(self):

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

    def execute_client(self, inputs):

    def execute_move(self, inputs):

class AC_controller:
    def __init__(self, access_points):
        self.access_points = access_points
        self.memory = []

    def change_channel(self):
        for a_point in self.access_points:
            conflicting_aps = [other_ap for other_ap in self.access_points if
                               other_ap.channel == a_point.channel and other_ap != a_point]
            if conflicting_aps:
                preferred_channels = [11, 6, 1]
                for channel in preferred_channels:
                    if not any(ap.channel == channel for ap in self.access_points):
                        a_point.give_channel_indicator(channel)
                        break
                else:
                    a_point.give_channel_indicator(a_point.channel - 1 if a_point.channel > 1 else 2)

    def change_memory(self):
        for a_point in self.access_points:
            self.memory.extend(a_point.get_mem())
        return self.memory


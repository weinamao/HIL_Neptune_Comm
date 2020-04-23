from niveristand import nivs_rt_sequence


class Test():

    def __init__(self):
        self.error = False

    @nivs_rt_sequence
    def set_val(self, channel, value):
        channel.value = value

class SignalManager:

    def __init__(self):

        self.left_signal = "RED"
        self.right_signal = "RED"

    def set_left_green(self):

        self.left_signal = "GREEN"
        self.right_signal = "RED"

    def set_right_green(self):

        self.left_signal = "RED"
        self.right_signal = "GREEN"

    def set_left_orange(self):

        self.left_signal = "ORANGE"

    def set_right_orange(self):

        self.right_signal = "ORANGE"

    def reset_signals(self):

        self.left_signal = "RED"
        self.right_signal = "RED"
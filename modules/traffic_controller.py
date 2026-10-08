class TrafficController:

    def __init__(self):

        self.current_lane = "LEFT"

    def calculate_timer(
        self,
        left_count,
        right_count
    ):

        if self.current_lane == "LEFT":

            timer = left_count

        else:

            timer = right_count

        # Minimum timer

        if timer < 5:
            timer = 5

        # Maximum timer

        if timer > 30:
            timer = 30

        return timer

    def switch_lane(self):

        if self.current_lane == "LEFT":

            self.current_lane = "RIGHT"

        else:

            self.current_lane = "LEFT"

    def get_current_lane(self):

        return self.current_lane
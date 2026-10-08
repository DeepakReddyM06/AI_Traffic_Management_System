class VehicleCounter:

    def __init__(
        self,
        roi_x1,
        roi_y1,
        roi_x2,
        roi_y2
    ):

        self.roi_x1 = roi_x1
        self.roi_y1 = roi_y1

        self.roi_x2 = roi_x2
        self.roi_y2 = roi_y2

    def inside_roi(
        self,
        center_x,
        center_y
    ):

        return (
            self.roi_x1 <= center_x <= self.roi_x2
            and
            self.roi_y1 <= center_y <= self.roi_y2
        )
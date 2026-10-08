import time

from modules.signal_manager import SignalManager
from modules.traffic_controller import TrafficController

signal = SignalManager()
controller = TrafficController()

left_count = 8
right_count = 7

timer = controller.calculate_timer(
    left_count,
    right_count
)

print("Current Lane:", controller.current_lane)
print("Timer:", timer)

while timer > 0:

    print(
        signal.left_signal,
        signal.right_signal,
        timer
    )

    if timer == 6:

        signal.set_orange()

    time.sleep(1)

    timer -= 1

signal.switch_signals()
controller.switch_lane()

print()
print("Switched")
print()

print(
    signal.left_signal,
    signal.right_signal
)
# sensor.py

import numpy as np


class RangeSensor:
    def __init__(self, max_range):
        self.max_range = max_range

    def sense(self, state, obstacles):
        readings = []

        for obs in obstacles:
            dx = obs.x - state.x
            dy = obs.y - state.y
            dist = np.hypot(dx, dy) - obs.radius

            if dist <= self.max_range:
                angle = np.arctan2(dy, dx) - state.theta
                readings.append({
                    "distance": dist,
                    "angle": angle
                })

        return readings


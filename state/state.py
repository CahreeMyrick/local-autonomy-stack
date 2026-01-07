# state.py
import numpy as np

class VehicleState:
    def __init__(self, x, y, theta=0.0, v=0.0, v_max=3.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.v = float(v)
        self.v_max = v_max

    def step(self, omega, a, dt):
        # Update heading and speed
        self.theta += omega * dt
        self.v += a * dt
        self.v = np.clip(self.v, 0.0, self.v_max)

        # Update position
        self.x += self.v * np.cos(self.theta) * dt
        self.y += self.v * np.sin(self.theta) * dt

    def position(self):
        return self.x, self.y


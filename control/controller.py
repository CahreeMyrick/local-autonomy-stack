# controller.py
import numpy as np

class WaypointController:
    def __init__(self, k_turn=2.0, k_speed=1.0):
        self.k_turn = k_turn
        self.k_speed = k_speed

    def control(self, state, waypoint):
        wx, wy = waypoint

        dx = wx - state.x
        dy = wy - state.y

        desired_theta = np.arctan2(dy, dx)
        heading_error = desired_theta - state.theta
        heading_error = (heading_error + np.pi) % (2*np.pi) - np.pi

        omega = self.k_turn * heading_error
        a = self.k_speed * np.hypot(dx, dy)

        return omega, a

class AvoidanceController:
    def __init__(self, goal, k_goal=2.0, k_avoid=1.5, safe_dist=10.0):
        self.goal = goal
        self.k_goal = k_goal
        self.k_avoid = k_avoid
        self.safe_dist = safe_dist

    def control(self, state, sensor_data):
        gx, gy = self.goal
        dx = gx - state.x
        dy = gy - state.y

        # --- Goal attraction ---
        goal_theta = np.arctan2(dy, dx)
        heading_error = goal_theta - state.theta
        heading_error = (heading_error + np.pi) % (2*np.pi) - np.pi

        omega_goal = self.k_goal * heading_error
        a = min(np.hypot(dx, dy), 3.0)

        # --- Obstacle repulsion ---
        omega_avoid = 0.0
        for obs in sensor_data:
            if obs["distance"] < self.safe_dist:
                omega_avoid += -self.k_avoid * np.sign(obs["angle"]) \
                               * (self.safe_dist - obs["distance"])

        omega = omega_goal + omega_avoid
        return omega, a


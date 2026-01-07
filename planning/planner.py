# planner.py
import numpy as np


def segment_collides(x0, y0, x1, y1, obs, steps=15):
    """
    Check whether the straight-line segment from (x0, y0) to (x1, y1)
    intersects an obstacle (with inflation handled externally).
    """
    for i in range(steps + 1):
        t = i / steps
        px = x0 + t * (x1 - x0)
        py = y0 + t * (y1 - y0)

        if np.hypot(px - obs.x, py - obs.y) < obs.radius:
            return True

    return False


class LocalPlanner:
    def __init__(
        self,
        goal,
        lookahead=10.0,
        num_samples=21,
        clearance=4.0
    ):
        """
        goal        : (x_goal, y_goal)
        lookahead   : distance of local waypoint
        num_samples : number of steering directions sampled
        clearance   : safety margin added to obstacle radius
        """
        self.goal = goal
        self.lookahead = lookahead
        self.num_samples = num_samples
        self.clearance = clearance

    def plan(self, state, obstacles):
        gx, gy = self.goal

        # Sample steering angles relative to current heading
        angles = np.linspace(-np.pi / 2, np.pi / 2, self.num_samples)

        best_cost = float("inf")
        best_waypoint = None

        for a in angles:
            theta = state.theta + a

            # Candidate waypoint
            wx = state.x + self.lookahead * np.cos(theta)
            wy = state.y + self.lookahead * np.sin(theta)

            # -----------------------------
            # Collision checking
            # -----------------------------
            collision = False
            for obs in obstacles:
                # Inflate obstacle
                inflated_obs = type(obs)(
                    obs.x, obs.y, obs.radius + self.clearance
                )

                # Check entire path segment
                if segment_collides(
                    state.x, state.y, wx, wy, inflated_obs
                ):
                    collision = True
                    break

            if collision:
                continue  # reject this candidate completely

            # -----------------------------
            # Cost function
            # -----------------------------
            # Primary term: distance to goal
            cost = np.hypot(gx - wx, gy - wy)

            # Secondary term: prefer smaller steering
            cost += 0.2 * abs(a)

            if cost < best_cost:
                best_cost = cost
                best_waypoint = (wx, wy)

        # -----------------------------
        # Fallback behavior
        # -----------------------------
        # If no safe waypoint found, go straight (slowly)
        if best_waypoint is None:
            best_waypoint = (
                state.x + 0.5 * self.lookahead * np.cos(state.theta),
                state.y + 0.5 * self.lookahead * np.sin(state.theta),
            )

        return best_waypoint


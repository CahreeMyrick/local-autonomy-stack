# experiments/evaluate.py
import numpy as np
from state.state import VehicleState
from simulation.simulator import Simulator
from sensor.sensor import RangeSensor
from planning.planner import LocalPlanner
from control.controller import WaypointController, AvoidanceController

MAX_STEPS = 1000
GOAL_TOL = 2.0

def compute_min_clearance(history, obstacles):
    """
    Minimum signed distance from trajectory to any obstacle.
    < 0  => collision
    = 0  => grazing
    > 0  => safe clearance
    """
    min_clearance = np.inf

    for (x, y) in history:
        for obs in obstacles:
            ox = obs.x
            oy = obs.y
            r  = obs.radius

            d = np.hypot(x - ox, y - oy) - r
            min_clearance = min(min_clearance, d)

    return min_clearance


def run_trial(planner_type, scenario, seed=None):
    rng = np.random.default_rng(seed)

    start = scenario["start"]
    goal = scenario["goal"]
    obstacles = scenario["obstacles"]

    state = VehicleState(*start, theta=0.0, v=0.0)
    sensor = RangeSensor(max_range=20.0)

    if planner_type == "reactive":
        planner = None
        controller = AvoidanceController(goal)
    elif planner_type == "planner":
        planner = LocalPlanner(goal)
        controller = WaypointController()
    else:
        raise ValueError("Unknown planner type")

    sim = Simulator(
        state=state,
        planner=planner,
        controller=controller,
        sensor=sensor,
        obstacles=obstacles,
        dt=0.1
    )

    history = []

    for step in range(MAX_STEPS):
        sim.step()
        history.append((state.x, state.y))

        if np.hypot(state.x - goal[0], state.y - goal[1]) < GOAL_TOL:
            min_clearance = compute_min_clearance(history, obstacles)
            return {
                "planner": planner_type,
                "success": True,
                "steps": step,
                "path_length": len(history),
                "min_clearance": min_clearance,
                "history": history,
                "obstacles": obstacles,
            }

    min_clearance = compute_min_clearance(history, obstacles)
    return {
        "planner": planner_type,
        "success": False,
        "steps": MAX_STEPS,
        "path_length": len(history),
        "min_clearance": min_clearance,
        "history": history,
        "obstacles": obstacles,
    }


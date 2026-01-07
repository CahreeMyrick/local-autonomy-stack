# main.py

from world.world import Obstacle
from state.state import VehicleState
from sensor.sensor import RangeSensor
from planning.planner import LocalPlanner
from control.controller import WaypointController
from simulation.simulator import Simulator
from visualize.visualization import animate


def main():
    goal = (150, 150)

    obstacles = [
    # Core diagonal blockers (break straight-line path)
    Obstacle(60, 60, 7),
    Obstacle(80, 80, 7),
    Obstacle(100, 100, 7),

    # Offset blockers (force detours)
    Obstacle(90, 65, 6),
    Obstacle(65, 90, 6),
    Obstacle(115, 85, 6),
    Obstacle(85, 115, 6),

    # Peripheral clutter (but not trapping)
    Obstacle(45, 95, 5),
    Obstacle(95, 45, 5),
    Obstacle(120, 120, 6),

    # Late-stage decision near goal
    Obstacle(135, 125, 6),
    Obstacle(125, 135, 6),
    ]

    # Vehicle state
    state = VehicleState(10, 10, theta=0.0, v=0.0)

    # Perception
    sensor = RangeSensor(max_range=20.0)

    # Planning (goal + obstacles live here)
    planner = LocalPlanner(goal, lookahead=10.0)

    # Control (tracks planner waypoint)
    controller = WaypointController()

    # Simulator (glue)
    sim = Simulator(
        state=state,
        planner=planner,
        controller=controller,
        sensor=sensor,
        obstacles=obstacles,
        dt=0.1
    )

    animate(sim, goal)


if __name__ == "__main__":
    main()


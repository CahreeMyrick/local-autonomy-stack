import numpy as np
from world.world import Obstacle

def generate_scenario(
    num_obstacles,
    world_size=(100, 100),
    min_dist=10.0,
    seed=None
):
    rng = np.random.default_rng(seed)

    obstacles = []
    width, height = world_size

    for _ in range(num_obstacles):
        x = rng.uniform(10, width - 10)
        y = rng.uniform(10, height - 10)
        r = rng.uniform(3, 6)

        obstacles.append(Obstacle(x, y, r))

    start = (10, 10)
    goal = (80, 80)

    return {
        "start": start,
        "goal": goal,
        "obstacles": obstacles
    }


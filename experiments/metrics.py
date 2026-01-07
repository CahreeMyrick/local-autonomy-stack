
import numpy as np

def compute_metrics(result):
    path = result["history"]
    obstacles = result["obstacles"]

    # Path length
    path_len = sum(
        np.hypot(
            path[i+1][0] - path[i][0],
            path[i+1][1] - path[i][1]
        )
        for i in range(len(path) - 1)
    )

    # Minimum clearance
    min_clearance = float("inf")
    for x, y in path:
        for obs in obstacles:
            d = np.hypot(x - obs.x, y - obs.y) - obs.radius
            min_clearance = min(min_clearance, d)

    return {
        "success": result["success"],
        "steps": result["steps"],
        "path_length": path_len,
        "min_clearance": min_clearance
    }


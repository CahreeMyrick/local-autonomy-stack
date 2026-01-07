# visualization.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(sim, goal):
    fig, ax = plt.subplots()

    # Camera settings
    view_radius = 50.0  # how much world to show around vehicle

    # Vehicle
    vehicle_dot, = ax.plot([], [], "bo", label="Vehicle")

    # Goal
    gx, gy = goal
    ax.plot(gx, gy, "rx", markersize=10, label="Goal")

    # Waypoint (planner output)
    waypoint_dot, = ax.plot([], [], "gx", markersize=8, label="Waypoint")

    # Obstacles
    for obs in sim.obstacles:
        circle = plt.Circle(
            (obs.x, obs.y),
            obs.radius,
            color="red",
            alpha=0.5
        )
        ax.add_patch(circle)

    ax.set_aspect("equal", adjustable="box")
    ax.legend()

    def update(frame):
        sim.step()

        # Vehicle position
        x, y = sim.state.position()
        vehicle_dot.set_data([x], [y])

        # Follow the vehicle
        ax.set_xlim(x - view_radius, x + view_radius)
        ax.set_ylim(y - view_radius, y + view_radius)

        # Planner waypoint
        if sim.current_waypoint is not None:
            wx, wy = sim.current_waypoint
            waypoint_dot.set_data([wx], [wy])
        else:
            waypoint_dot.set_data([], [])

        return vehicle_dot, waypoint_dot

    ani = FuncAnimation(
        fig,
        update,
        interval=50,
        blit=False,          # blit off since axes are moving
        cache_frame_data=False
    )

    plt.show()


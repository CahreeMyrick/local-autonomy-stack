# simulator.py
class Simulator:
    def __init__(self, state, planner, controller, sensor, obstacles, dt):
        self.state = state
        self.planner = planner          # may be None
        self.controller = controller
        self.sensor = sensor
        self.obstacles = obstacles
        self.dt = dt

        self.current_waypoint = None

    def step(self):
        # Always sense first
        sensor_data = self.sensor.sense(self.state, self.obstacles)

        if self.planner is not None:
            # Planner-based autonomy
            self.current_waypoint = self.planner.plan(
                self.state, self.obstacles
            )
            omega, a = self.controller.control(
                self.state, self.current_waypoint
            )
        else:
            # Reactive baseline
            omega, a = self.controller.control(
                self.state, sensor_data
            )

        self.state.step(omega, a, self.dt)


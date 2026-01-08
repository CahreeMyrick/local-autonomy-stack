# Local Autonomy Stack
A modular 2D autonomous navigation system implementing sensing, local planning, control, and evaluation, with quantitative comparison between reactive obstacle avoidance and planner-based navigation.

This project explores core autonomy concepts—how forward-looking planning improves reliability and efficiency compared to purely reactive control—using a lightweight but extensible simulation framework.

## Key Features
Modular autonomy stack with clear sepration of:
- State representation
- Sensing (range-based obstacle perception)
- Local planning
- Simulation and evaluation

**Reactive baseline controller** using goal attraction + obstacle repulsion

**Local Planner** using steering-angle sampling, collision checking, and cost-based waypoint selection

**Automated experiment framework** for large scale evaluation

**Quantitative performance metrics** (success rate, collision rate, path length, clearance)

Reproducible experiments with randomized obstacle scenarios

## System Architecture
This system follows a classic autonomy pipeline:
```sql
State → Sense → Plan → Control → Execute → State
```
### Core Components
State
- Represents vehicle pose and headind in 2d

Range Sensor
- Simulates limited-range perception of nearby obstacles

Controllers
- Reactive controller: combines goal attraction and obstacle repulsion
- Waypoint controller: tracks planner-generated waypoints

Local Planner
- Samples candidate steering directions
- Performs collision checking against obstacles
- Selects the safest, goal-directed waypoint via a cost function

Simulation Loop
- Advances the system step-by-step and records metrics

Experiments Module
- Runs large batches of trials and aggregates results

## Algorithms
### Reactice Obstacle Avoidance
A purely local strategy that steers toward te goal and applies repulsive forces when near obsatcles.

### Local-Planning (Waypoint-Based)
A forward looking strategy that samples multiple candidate steering angles, projects a short-horizon waypoint, 
rejects trajectories that collide with obstacles, and chooses the waypoint minimizing distance-to-goal plus steering cost.

## Experimental Evaluation
Evaluated reactive control vs planner based navigation over 100 randomized trials with 7 obstacles per scenario.

### Results Summary
| Planner    | Trials | Success Rate | Collision Rate | Mean Steps | Std Steps | Mean Path Length | Std Path Length | Mean Clearance |
|------------|--------|--------------|----------------|------------|-----------|------------------|-----------------|----------------|
| Reactive   | 100    | 0.61         | 0.17           | 432.70     | 136.82    | 433.70           | 136.82          | 6.40           |
| Planner    | 100    | 0.81         | 0.06           | 350.10     | 36.47     | 351.10           | 36.47           | 4.07           |

**These results demonstrate the limitations of purely reactive autonomy and the benefits of even simple forward-looking planning.**

## Running Expirements
```bash

python -m experiments.run \
  --planner reactive planner \
  --num-trials 100 \
  --num-obstacles 7
```

## Run Demo
```bash 
python main.py
```

## Demo
![ED02B4C7-7972-44EF-9FAD-6EBB42B70A90_1_102_o](https://github.com/user-attachments/assets/ae8ac35c-585c-4b9d-877c-5bb029f196df)

from Drone import Drone
from simulation import simulation   # make sure filename matches

# Create drones
d1 = Drone("D1", 10)
d2 = Drone("D2", 5)

drones = [d1, d2]

# Define routes (each route = list of points)
routes = [
    [(5, 5), (10, 5)],     # drone 1 path
    [(-5, 3), (-8, 6)]     # drone 2 path
]

# No-fly zones
obstacles = [(2,2), (3,3), (-2,4)]

# Run simulation
simulation(routes, drones, obstacles)
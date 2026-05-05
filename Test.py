from Fleet import Fleet
from Drone import Drone
from Package import Package

fleet = Fleet()


d1 = Drone("D1", 10)
d2 = Drone("D2", 5)

fleet.add_drone(d1)
fleet.add_drone(d2)

p1 = Package("P1", 3, (4, 5))
p2 = Package("P2", 6, (2, 8))

fleet.add_package(p1)
fleet.add_package(p2)


fleet.add_no_fly_zone([(1, 1), (2, 2)])


fleet.assign_packages()


fleet.show_status()


fleet.save_to_file()
print("\nFleet saved to file.")


fleet2 = Fleet()
fleet2.load_from_file()

print("\nLoaded Fleet:")
fleet2.show_status()


print("\nTop drones by battery:")
for d in fleet2.top_drones():
    print(d)
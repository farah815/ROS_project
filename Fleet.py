import json
from Drone import Drone
from Package import Package


class Fleet:
    def __init__(self):
        self.drones = []
        self.packages = []
        self.no_fly_zones = []  

  
    def add_drone(self, drone):
        self.drones.append(drone)

   
    def add_package(self, package):
        self.packages.append(package)


    def add_no_fly_zone(self, zone_points):
        self.no_fly_zones.extend(zone_points)

  
    def assign_packages(self):
        for drone in self.drones:
            if drone.package_id is None and drone.status=="idle":
                for package in self.packages:
                    if package.status == "waiting" and package.weight <= drone.max_payload:
                        drone.assign_package(package)
                        package.mark_in_transit()
                        break

 
    def show_status(self):
        print("\n===== FLEET STATUS =====")

        print("\nDrones:")
        for d in self.drones:
            print(d)

        print("\nPackages:")
        for p in self.packages:
            print(p)

 
    def save_to_file(self, filename="fleet.json"):
        data = {
            "drones": [d.to_dict() for d in self.drones],
            "packages": [p.to_dict() for p in self.packages],
            "no_fly_zones": self.no_fly_zones
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

  
    def load_from_file(self, filename="fleet.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            self.drones = [Drone.from_dict(d) for d in data["drones"]]
            self.packages = [Package.from_dict(p) for p in data["packages"]]
            self.no_fly_zones = data.get("no_fly_zones", [])

        except FileNotFoundError:
            print("No saved data found. Starting fresh.")

   
    def top_drones(self):
        return sorted(self.drones, key=lambda d: d.missions_completed, reverse=True)
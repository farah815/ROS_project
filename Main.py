from Fleet import Fleet
from Drone import Drone
from Package import Package
from grid import Grid
from Orchestrator import orchestrate_missions
from Weather_System import WeatherSystem
from simulation import simulation

def main():
    fleet = Fleet()
    fleet.load_from_file()  # auto-loads on startup
    print("📂 Fleet state loaded.")

    while True:
        print("\n===== AEROPATH SYSTEM =====")
        print("1. Add Drone")
        print("2. Add Package")
        print("3. Add No-Fly Zone")
        print("4. Assign Packages")
        print("5. Show Status")
        print("6. Save System")
        print("7. Load System")
        print("8. Top Drones")
        print("9. Start Flight Simulation")
        print("10. Champions of Efficiency")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            drone_id = input("Drone ID: ")
            max_payload = int(input("Max Payload: "))
            battery = int(input("Battery (default 100): ") or 100)
            drone = Drone(drone_id, max_payload, battery)
            fleet.add_drone(drone)
            print("✅ Drone added")

        elif choice == "2":
            package_id = input("Package ID: ")
            weight = int(input("Weight: "))
            x = int(input("Destination X: "))
            y = int(input("Destination Y: "))
            package = Package(package_id, weight, (x, y))
            fleet.add_package(package)
            print("✅ Package added")

        elif choice == "3":
            x = int(input("X: "))
            y = int(input("Y: "))
            fleet.add_no_fly_zone([(x, y)])
            print("✅ No-fly zone added")

        elif choice == "4":
            fleet.assign_packages()
            print("✅ Packages assigned")

        elif choice == "5":
            fleet.show_status()

        elif choice == "6":
            fleet.save_to_file()
            print("💾 Saved successfully")

        elif choice == "7":
            fleet.load_from_file()
            print("📂 Loaded successfully")

        elif choice == "8":
            print("\n🏆 Top Drones:")
            for d in fleet.top_drones():
                print(d)

        elif choice == "9":
           

            # Build the grid
            grid = Grid(20, 20)
            grid.register_no_fly_zones([tuple(z) for z in fleet.no_fly_zones])
            weather = WeatherSystem()

            # Pair drones with their packages
            fleet_dict = {}
            for drone in fleet.drones:
                if drone.package_id:
                    pkg = next((p for p in fleet.packages
                               if p.package_id == drone.package_id), None)
                    if pkg:
                        fleet_dict[drone.drone_id] = {
                            "target": pkg.destination,
                            "battery": drone.battery,
                            "max_battery": 100,
                            "payload": pkg.weight
                        }

            if not fleet_dict:
                print("⚠️  No drones have packages assigned. Use option 4 first.")
            else:
                # Plan all missions
                planned = orchestrate_missions(grid, fleet_dict)

                # Build routes for simulation
                routes = []
                drones_to_simulate = []

                for d_id, result in planned.items():
                    if result["status"] == "Success":
                        path_coords = [node for node, t in result["path"]]
                        routes.append(path_coords)
                        drone_obj = next(d for d in fleet.drones
                                        if d.drone_id == d_id)
                        drones_to_simulate.append(drone_obj)
                        print(f"✅ {d_id}: planned ({len(path_coords)} steps)")
                    else:
                        print(f"❌ {d_id}: {result['reason']}")

                if routes:
                    simulation(
                        routes,
                        drones_to_simulate,
                        obstacles=fleet.no_fly_zones,
                        pre_planned=True
                    )

        elif choice == "10":
            from logger import get_champions
            champs = get_champions()
            if not champs:
                print("⚠️  No logs yet. Run a simulation first.")
            else:
                print("\n🏆 CHAMPIONS OF EFFICIENCY")
                print(f"{'Rank':<6}{'Drone ID':<12}{'Missions':<10}{'Battery Left'}")
                print("-" * 40)
                for i, c in enumerate(champs, 1):
                    print(f"{i:<6}{c['drone_id']:<12}{c['missions_completed']:<10}{c['battery_remaining']:.1f}%")

        elif choice == "0":
            fleet.save_to_file()  # auto-save on exit
            print("💾 Fleet saved.")
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
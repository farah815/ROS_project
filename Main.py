from Fleet import Fleet
from Drone import Drone
from Package import Package
from grid import Grid
from Orchestrator import orchestrate_missions
from Weather_System import WeatherSystem
from simulation import simulation
from Execution import execute_flight
import os
from time import time
cur_os = os.name
def clear():
    if cur_os=='nt':
        os.system("cls")
    else:
        os.system("clear")
        
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
            drone_id = input("Enter Drone ID: ").strip().upper()
            while 1:
                try:
                    drone_mass = float(input("Drone mass: "))
                    if drone_mass:
                        break
                    else: print("drone_mass can't be zero")
                except ValueError:
                    print("❌ Invalid input, try again.")
            while 1:
                try:
                    max_payload = float(input("Max Payload: "))
                    if max_payload:
                        break
                    else: print("Payload can't be zero")
                except ValueError:
                    print("❌ Invalid input, try again.")
            while 1:
                try:
                    battery = float(input("Battery (default 100): ") or 100)
                    break
                except ValueError:
                    print("❌ Invalid input, try again.")
            drone = Drone(drone_id,drone_mass ,max_payload, battery)
            fleet.add_drone(drone)
            clear()
            print("✅ Drone added")

        elif choice == "2":
            package_id = input("Package ID: ")
            while 1:
                try:
                    weight = float(input("Weight: "))
                    if weight:
                        break
                    else: print("battery can't be zero")
                except ValueError:
                    print("❌ Invalid input, try again.")
            while 1:
                try:
                    x = float(input("Destination X: "))
                    y = float(input("Destination Y: "))
                    break
                except ValueError:
                    print("❌ Invalid input, try again.")
            package = Package(package_id, weight, (x, y))
            fleet.add_package(package)
            clear()
            print("✅ Package added")

        elif choice == "3":
            while 1:
                try:
                    x = float(input("X: "))
                    y = float(input("Y: "))
                    break
                except ValueError:
                    print("❌ Invalid input, try again.") 
            fleet.add_no_fly_zone([(x, y)])
            clear()
            print("✅ No-fly zone added")

        elif choice == "4":
            fleet.assign_packages()
            clear()
            print("✅ Packages assigned")

        elif choice == "5":
            clear()
            fleet.show_status()

        elif choice == "6":
            fleet.save_to_file()
            clear()
            print("💾 Saved successfully")

        elif choice == "7":
            fleet.load_from_file()
            clear()
            print("📂 Loaded successfully")

        elif choice == "8":
            clear()
            print("\n🏆 Top Drones:")
            for d in fleet.top_drones():
                print(d)

        elif choice == "9":
            t=time()
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
                         "payload": pkg.weight,
                         "drone_mass": drone.mass   
                        }

            if not fleet_dict:
                print("⚠️ No drones have packages assigned. Use option 4 first.")
            else:
                # Plan all missions
                print("\n[Phase 1] Planning & Scheduling Missions...")
                planned = orchestrate_missions(grid, fleet_dict)

                # Execute flights with real-time monitoring
                print("\n[Phase 2] Executing Flights with Dynamic Monitoring...")
                routes = []
                drones_to_simulate = []

                for d_id, result in planned.items():
                    if result["status"] == "Success":
                        
                        # --- FIX: FIND THE DRONE OBJECT ---
                        # This line prevents the UnboundLocalError
                        drone_obj = next((d for d in fleet.drones if d.drone_id == d_id), None)

                        if drone_obj is not None:
                            status, actual_path = execute_flight(
                                grid, 
                                d_id, 
                                result["path"],
                                fleet_dict[d_id], 
                                weather,
                                drone_obj  # Now correctly associated with a value[cite: 3]
                            )
                            
                            print(f"  {'✅' if 'Success' in status else '⚠️ '} {d_id}: {status} "
                                  f"| delay={result['delay']}s | steps={len(actual_path)}")

                            path_coords = [node for node, t in actual_path]
                            routes.append(path_coords)
                            drones_to_simulate.append(drone_obj)
                    else:
                        print(f"  ❌ {d_id}: {result['reason']}")

                if routes:
                    print(time()-t)
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
                clear()
                print("⚠️  No logs yet. Run a simulation first.")
            else:
                clear()
                print("\n🏆 CHAMPIONS OF EFFICIENCY")
                print(f"{'Rank':<6}{'Drone ID':<12}{'Missions':<10}{'Battery Left'}")
                print("-" * 40)
                for i, c in enumerate(champs, 1):
                    print(f"{i:<6}{c['drone_id']:<12}{c['missions_completed']:<10}{c['battery_remaining']:.1f}%")

        elif choice == "0":
            fleet.save_to_file()  # auto-save on exit
            clear()
            print("💾 Fleet saved.")
            print("👋 Exiting...")
            break

        else:
            clear()
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()

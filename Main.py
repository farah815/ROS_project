from Fleet import Fleet
from Drone import Drone
from Package import Package


def main():
    fleet = Fleet()

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
        print("0. Exit")

        choice = input("Enter choice: ")


        if choice == "1":
            drone_id = input("Drone ID: ")
            max_payload = int(input("Max Payload: "))
            battery = int(input("Battery (default 100): ") or 100)

            drone = Drone(drone_id, max_payload, battery)
            fleet.add_drone(drone)

            print("Drone added")

        elif choice == "2":
            package_id = input("Package ID: ")
            weight = int(input("Weight: "))
            x = int(input("Destination X: "))
            y = int(input("Destination Y: "))

            package = Package(package_id, weight, (x, y))
            fleet.add_package(package)

            print("Package added")

     
        elif choice == "3":
            x = int(input("X: "))
            y = int(input("Y: "))

            fleet.add_no_fly_zone([(x, y)])
            print("No-fly zone added")

       
        elif choice == "4":
            fleet.assign_packages()
            print("Packages assigned")

        # -------------------------
        # 5. Show Status
        # -------------------------
        elif choice == "5":
            fleet.show_status()

        # -------------------------
        # 6. Save
        # -------------------------
        elif choice == "6":
            fleet.save_to_file()
            print("💾 Saved successfully")

        # -------------------------
        # 7. Load
        # -------------------------
        elif choice == "7":
            fleet.load_from_file()
            print("📂 Loaded successfully")

        # -------------------------
        # 8. Top Drones
        # -------------------------
        elif choice == "8":
            print("\n🏆 Top Drones:")
            for d in fleet.top_drones():
                print(d)

      
        elif choice == "0":
            print("👋 Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
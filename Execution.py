from logger import log_mission


def execute_flight(grid_obj, drone_id, plan, info, weather_system, drone_obj):
    safety = info['max_battery'] * 0.10
    actual_path = []
    reached_target = False

    for i, (node, t) in enumerate(plan):
        actual_path.append((node, t))

        # 1. Check for arrival at target
        if not reached_target and node == info['target']:
            reached_target = True
            drone_obj.deliver_package()          # increments missions_completed

        # 2. Arrived back at base -> full mission complete
        if reached_target and node == (0, 0):
            drone_obj.return_to_base()
            log_mission(drone_id, drone_obj.missions_completed, drone_obj.battery)
            return "Mission Success", actual_path

        # 3. Low-battery check: must we turn back NOW?
        if drone_obj.should_return_home(node, safety_margin=safety):
            if node != (0, 0):
                print(f"Low Battery at {node}. Aborting mission.")
                grid_obj.cancel_reservation(plan, t)

                rtl_path, _ = grid_obj.find_path_time_aware(node, (0, 0), start_time=t)
                if rtl_path:
                    grid_obj.reserve_path(rtl_path)
                    # Walk the RTL path so battery drains correctly
                    for rtl_node, rtl_t in rtl_path[1:]:
                        wind = weather_system.get_wind(drone_id)
                        drain = drone_obj.mass * 9.81 * 0.005 * wind
                        drone_obj.drain_battery(drain)
                        actual_path.append((rtl_node, rtl_t))
                    drone_obj.return_to_base()
                    log_mission(drone_id, drone_obj.missions_completed, drone_obj.battery)
                    return "Emergency RTL", actual_path

                # No path home found - forced landing wherever it is
                log_mission(drone_id, drone_obj.missions_completed, drone_obj.battery)
                return "Critical: Forced Landing", actual_path

        # 4. Drain battery for this step
        wind = weather_system.get_wind(drone_id)
        mass = (info['drone_mass'] + info['payload']) if not reached_target else info['drone_mass']
        drain = mass * 9.81 * 0.005 * wind
        drone_obj.drain_battery(drain)

    # Plan exhausted without completing the loop back to base
    log_mission(drone_id, drone_obj.missions_completed, drone_obj.battery)
    return "Mission Ended", actual_path
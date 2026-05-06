from ability_test import check_preflight_feasibility 

def orchestrate_missions(grid_obj, fleet_dict):
    schedule = {}
    # ترتيب الأولوية: الأثقل حملاً والأقل بطارية أولاً
    sorted_fleet = sorted(fleet_dict.items(), key=lambda x: ((x[1]['payload']+x[1]['drone_mass'])*9.81)/x[1]['battery'], reverse=True)

    for d_id, info in sorted_fleet:
        can_fly, msg = check_preflight_feasibility(info['drone_mass'], info['payload'], info['battery'], (0,0), info['target'], info['max_battery'])
        if not can_fly:
            schedule[d_id] = {"status": "Failed", "reason": msg}; continue

        found = False
        for delay in range(40): 
            out, _ = grid_obj.find_path_time_aware((0,0), info['target'], start_time=delay)
            if out:
                back, _ = grid_obj.find_path_time_aware(info['target'], (0,0), start_time=out[-1][1])
                if back:
                    full = out + back[1:]; grid_obj.reserve_path(full)
                    schedule[d_id] = {"status": "Success", "path": full, "delay": delay}
                    found = True; break
                    
        if not found: schedule[d_id] = {"status": "Failed", "reason": "Congestion"}
    return schedule
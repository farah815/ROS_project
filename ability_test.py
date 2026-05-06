def check_preflight_feasibility(drone_mass, payload_mass, current_battery, start, target, max_battery=100):

    g = 9.81
    efficiency = 0.005
    dist = abs(target[0] - start[0]) + abs(target[1] - start[1])

    energy_out = dist * ((drone_mass + payload_mass) * g * efficiency)
    safety_limit = max_battery * 0.10

    if current_battery < energy_out + safety_limit:
        # ⚠️ WARNING ONLY — don't block
        return True, "Warning: may not complete mission"

    return True, "Flight Approved"
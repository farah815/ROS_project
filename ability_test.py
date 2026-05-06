def check_preflight_feasibility(drone_mass, payload_mass, current_battery, start, target, max_battery=100):
    """التأكد المبدئي """
    g = 9.81
    efficiency = 0.005 
    dist = abs(target[0] - start[0]) + abs(target[1] - start[1])
    
    energy_out = dist * ((drone_mass + payload_mass) * g * efficiency)
    energy_back = dist * (drone_mass * g * efficiency)
    
    total_needed = energy_out + energy_back
    safety_limit = max_battery * 0.10 
    
    if current_battery < energy_out + safety_limit:
        return False, "Battery too low for outbound"
    if current_battery < total_needed + safety_limit:
        return False, "Insufficient battery for RTL"
    
    return True, "Flight Approved"
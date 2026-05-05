from grid import Grid
from Weather_System import WeatherSystem

def execute_flight(grid_obj, drone_id, plan, info, weather_system):
    current_batt = info['battery']
    safety = info['max_battery'] * 0.10
    actual_path = []
    reached_target = False 

    for i, (node, t) in enumerate(plan):
        actual_path.append((node, t))
        
        # عند العودة للقاعدة
        if i > 0 and node == (0,0):
            # سلم ولا؟
            status = "Mission Success" if reached_target else "RTL Completed (Abort)"
            return status, actual_path
            
        if not reached_target and node == info['target']:
            reached_target = True

        wind = weather_system.get_wind(drone_id)
        mass = 2.0 if reached_target else (2.0 + info['payload'])
        
        # مبدئيا مراقبة للرياح
        dist_back = node[0] + node[1]
        energy_to_return = dist_back * (2.0 * 9.81 * 0.005 * wind)
        
        if current_batt < energy_to_return + safety:
            grid_obj.cancel_reservation(plan, t)
            rtl, _ = grid_obj.find_path_time_aware(node, (0,0), start_time=t)
            if rtl:
                grid_obj.reserve_path(rtl)
                return f"Emergency RTL (Wind Risk: {wind}x)", actual_path + rtl[1:]
            return "Critical: Forced Landing", actual_path
        
        current_batt -= (mass * 9.81 * 0.005 * wind)
    return "Mission Ended", actual_path
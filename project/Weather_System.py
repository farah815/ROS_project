class WeatherSystem:
    def __init__(self):
        self.drones_wind = {} # id الدرون -> قوة الرياح

    def set_drone_wind(self, drone_id, power):
        self.drones_wind[drone_id] = power

    def get_wind(self, drone_id):
        return self.drones_wind.get(drone_id, 1.0)
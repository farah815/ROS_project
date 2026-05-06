class Drone:
    def __init__(self, drone_id, max_payload, battery=100) :
        self.drone_id=drone_id
        self.max_payload=max_payload
        self.battery=battery
        self.position = (0, 0)            
        self.status = "idle" 
        self.missions_completed = 0             
        self.package_id = None

    def __repr__(self):
      return f"Drone(id={self.drone_id}, battery={self.battery}%, status={self.status}, pos={self.position})"  

    def assign_package(self,package) :
        if package.weight>self.max_payload:
            raise ValueError(" Package exceeds drone capacity")
        self.package_id = package.package_id
        self.status = "delivering"
    

    
    def move_drone (self, new_position) :
        if not isinstance(new_position, tuple) or len(new_position) != 2:
            raise ValueError("Invalid position format")
        self.position = new_position
 
    def drain_battery(self, amount):
        self.battery -= amount

        if self.battery < 0:
            self.battery = 0

    def is_low_battery(self):
        return self.battery <= 10  

    def deliver_package(self):
     self.missions_completed += 1  
     self.package_id = None
     self.status = "returning"  

    def return_to_base(self):
        self.position = (0, 0)
        self.status = "idle"
        self.package_id = None    
    
    def should_return_home(self, steps_to_home):
   
      battery_needed = steps_to_home * 2  
      safety_margin = 5                   
    
      return self.battery <= battery_needed + safety_margin

    def to_dict(self):
     return {
        "drone_id": self.drone_id,
        "max_payload": self.max_payload,
        "battery": self.battery,
        "position": list(self.position),
        "status": self.status,
        "package_id": self.package_id,
        "missions_completed": self.missions_completed  # ← add this
    }

  
    @staticmethod
    def from_dict(data):
     drone = Drone(
        data["drone_id"],
        data["max_payload"],
        data["battery"]
    )
     drone.position = tuple(data["position"])
     drone.status = data["status"]
     drone.package_id = data["package_id"]
     drone.missions_completed = data.get("missions_completed", 0)  # ← add this
     return drone   
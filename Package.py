class Package:
    
     def __init__(self, package_id, weight, destination):
        self.package_id = package_id
        self.weight = weight
        self.destination = destination  
        self.status = "waiting" 

   
     def mark_in_transit(self):
        self.status = "in_transit"

   
     def mark_delivered(self):
        self.status = "delivered"

    
     def to_dict(self):
        return {
            "package_id": self.package_id,
            "weight": self.weight,
            "destination": self.destination,
            "status": self.status
        }

 
     @staticmethod
     def from_dict(data):
        package = Package(
            data["package_id"],
            data["weight"],
            tuple(data["destination"])
        )
        package.status = data["status"]
        return package

  
     def __repr__(self):
      return f"Package(id={self.package_id}, weight={self.weight}, dest={self.destination}, status={self.status})"
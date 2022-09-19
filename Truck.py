# Truck class

class Truck:
    def __init__(self, load, packages, maximum, start_address, truck_speed, truck_mileage, departure_time):
        self.load = load
        self.packages = packages
        self.maximum = maximum
        self.start_address = start_address
        self.truck_speed = truck_speed
        self.truck_mileage = truck_mileage
        self.departure_time = departure_time

        self.time = departure_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.load, self.packages, self.maximum, self.start_address,
                                               self.truck_speed, self.truck_mileage, self.departure_time)

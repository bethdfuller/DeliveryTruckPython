# Package class

class Package:
    def __init__(self, package_id, package_weight, delivery_address, delivery_city, delivery_zip,
                 delivery_deadline, delivery_status):
        self.package_id = package_id
        self.package_weight = package_weight
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.delivery_status = delivery_status

        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.package_weight, self.delivery_address,
                                               self.delivery_city, self.delivery_zip, self.delivery_deadline,
                                               self.delivery_status)

    # Formula used to update delivery_status (Options: Delivered, En Route or At Hub)
    def status_update(self, time_convert):
        if self.delivery_time < time_convert:
            self.delivery_status = "Package has been delivered."
        elif self.departure_time > time_convert:
            self.delivery_status = "Package is en route."
        else:
            self.delivery_status = "Package is at hub."

# Beth Fuller
# Student ID: 001409039
# WGU C950: WGUPS Routing Program

# Imports
import csv
import datetime

import Truck
import Package

from HashMap import HashMap
from Package import Package

# Read CSV Address File
with open("CSV /Address.csv") as csvAddressFile:
    CSV_Address = csv.reader(csvAddressFile)
    CSV_Address = list(CSV_Address)

# Read CSV Distance File
with open("CSV /Distance.csv") as csvDistanceFile:
    CSV_Distance = csv.reader(csvDistanceFile)
    CSV_Distance = list(CSV_Distance)

# Read CSV Package File
with open("CSV /Package.csv") as csvPackageFile:
    CSV_Package = csv.reader(csvPackageFile)
    CSV_Package = list(CSV_Package)


# Create package objects from the Package.csv file & load packages into hash table
# Space-time complexity: O(N)
def load_packages(filename, package_hash):
    with open(filename) as package_content:
        package_data = csv.reader(package_content)
        for package in package_data:
            p_package_id = int(package[0])
            p_package_weight = package[6]
            p_delivery_address = package[1]
            p_delivery_city = package[2]
            p_delivery_zip = package[4]
            p_delivery_deadline = package[5]
            p_delivery_status = "Package is at hub."

            # Package object
            p = Package(p_package_id, p_package_weight, p_delivery_address, p_delivery_city, p_delivery_zip,
                        p_delivery_deadline, p_delivery_status)

            # Insert package data into hash table
            package_hash.insert(p_package_id, p)


# Create hash table and then load packages into hash table
package_hash = HashMap()
load_packages("CSV /Package.csv", package_hash)

# Create truck 1 object - Start 8 - Specials: 14 (w/15,19), 16 (w/13,19), 20 (2/13,15)
# truck 1 - 15 packages
truck_1 = Truck.Truck(None, [1, 7, 13, 14, 15, 16, 19, 20, 21, 24, 27, 29, 34, 35, 39], 16, "4001 South 700 East",
                      18, 0.0, datetime.timedelta(hours=8))

# Create truck 2 object - Start 8, Packages - 3, 18, 36, 38 must be on truck 2
# truck 2 - 10 packages
# V2 - move packages 6, 30, 31, 40 from truck 3 to truck 2 and depart truck 2 at 9:05 for package deadlines
truck_2 = Truck.Truck(None, [3, 5, 11, 12, 17, 18, 23, 36, 37, 38, 6, 30, 31, 40], 16, "4001 South 700 East",
                      18, 0.0, datetime.timedelta(hours=9, minutes=5))

# Create truck 3 object - Start at 10:20 when address corrected for package 9
# Packages - 6, 25, 28, 32 delayed until 9:05 AM
# truck 3 - 15 packages
truck_3 = Truck.Truck(None, [2, 4, 8, 9, 10, 22, 25, 26, 28, 32, 33], 16, "4001 South 700 East",
                      18, 0.0, datetime.timedelta(hours=10, minutes=20))


# Method used to get the address
# Space-time complexity: O(N)
def get_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Method used to find distance between two addresses
# Space-time complexity: O(1)
def get_distance_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    return float(distance)


# Method for ordering the packages onto the truck using the nearest neighbor algorithm
# Space-time complexity: O(N^2)
def deliver_packages(truck):
    # Create array of undelivered packages
    needs_delivered = []
    for package_package_id in truck.packages:
        package = package_hash.hash_lookup(package_package_id)
        needs_delivered.append(package)

    # Clear the list of packages so that the algorithm can add them in order of nearest neighbor
    truck.packages.clear()

    # Runs through the list of packages in needs_delivered until the list is empty
    # Adds the packages in order of nearest neighbor 
    while len(needs_delivered) > 0:
        next_delivery = 4000
        next_package = None
        for package in needs_delivered:
            if get_distance_between(get_address(truck.start_address),
                                    get_address(package.delivery_address)) <= next_delivery:
                next_delivery = get_distance_between(get_address(truck.start_address),
                                                     get_address(package.delivery_address))
                next_package = package

        # Adds next package to the truck's package list & then removes it from the needs_delivered list
        truck.packages.append(next_package.package_id)
        needs_delivered.remove(next_package)
        # Adds mileage to the truck_mileage
        truck.truck_mileage += next_delivery
        # Changes truck address to package it just delivered
        truck.start_address = next_package.delivery_address
        # Updates total driving time
        truck.time += datetime.timedelta(hours=next_delivery / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.departure_time


# Load trucks. Truck 3 needs a driver so must wait for Truck 1 or 2 to complete deliveries before departing.
deliver_packages(truck_1)
deliver_packages(truck_2)
truck_3.departure_time = min(truck_1.time, truck_2.time)
deliver_packages(truck_3)


class Main:
    # User Interface - user input to answer
    print("Western Governors University Parcel Service")
    # Print total mileage for 3 trucks
    print("Truck 1: " + str(truck_1.truck_mileage))
    print("Truck 2: " + str(truck_2.truck_mileage))
    print("Truck 3: " + str(truck_3.truck_mileage))
    # Print total
    print("The total mileage for the 3 delivery trucks is: " + str(truck_1.truck_mileage + truck_2.truck_mileage + truck_3.truck_mileage))
    # Start input with user
    text = input("To check WGUPS route, time and package details type 'start'. All other entries with quit program.")
    if text == 'start':
        try:
            time_check = input("Enter a time (using format HH:MM:SS) to check status of package(s).")
            (h, m, s) = time_check.split(":")
            time_convert = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            package_check = input("To view status of a single package type '1' "
                                  "to view status of all packages type '2'.")
            if package_check == "1":
                try:
                    # Looks up package by package ID, exits program if invalid entry
                    single_package = input("Enter the package ID")
                    package = package_hash.hash_lookup(int(single_package))
                    package.status_update(time_convert)
                    print(str(package))
                except ValueError:
                    print("Invalid entry. Program exit.")
                    exit()
            elif package_check == "2":
                try:
                    for package_package_id in range(1, 41):
                        package = package_hash.hash_lookup(package_package_id)
                        package.status_update(time_convert)
                        print(str(package))

                except ValueError:
                    print("Invalid entry. Program exit.")
                    exit()

            else:
                exit()
        except ValueError:
            print("Invalid entry. Program exit.")
            exit()
    elif input != "start":
        print("Invalid entry. Program exit.")
        exit()

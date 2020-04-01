# Jacob Alo, SID: 000929515
# Thank you for reviewing my code!



import csv
from operator import attrgetter


# Hub class represents delivery hubs as individuals with relevant delivery information. In all cases, a hub will
# be referred to by its index, provided as an argument to the get_hub method.
class Hub:
    def __init__(self, hub_id, name, address, zip_code, neighbors):
        self.hub_id = hub_id  # 0-26
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.neighbors = neighbors  # List of distance to hubs stored in direct hash by index ID from 0-26.
        self.distance = float('inf')
        self.predecessor_hub = ''

    # Return the distance to a given neighbor, specified by hub index.
    def get_neighbor(self, index):
        return self.neighbors[index]


# Hubs class represent the delivery hubs as a group, with methods to describe relationships, and a graph, mostly
# for use with master_hubs variable. Hubs in hub_list are stored in a direct hash as a hub ID index, and are used by
# the get_hub method. This index value is pulled directly from the csv as the row the hub information is displayed in,
# starting at 0 for the first row (WGU).
class Hubs(Hub):
    def __init__(self):
        self.hub_list = []
        self.adjacency_list = {}
        self.edge_weights = {}

    # Add hub to the list of hubs, for use by master_hubs.
    def add_hub(self, hub):
        self.hub_list.append(hub)
        self.adjacency_list[hub] = []

    def add_directed_edge(self, hub, neighboring_hub, weight=1.0):
        self.edge_weights[(hub, neighboring_hub)] = weight
        self.adjacency_list[hub].append(neighboring_hub)

    def add_undirected_edge(self, hub_a, hub_b, weight=1.0):
        self.add_directed_edge(hub_a, hub_b, weight)
        self.add_directed_edge(hub_b, hub_a, weight)

    # Get distance between two hubs. Includes check to make sure an out of index error does not occur,
    # by making sure that row and column in list are being referenced in proper order.
    def get_distance(self, hub_a, hub_b):
        if hub_a < hub_b:
            temp = hub_b
            hub_b = hub_a
            hub_a = temp
        return self.get_hub(hub_a).get_neighbor(hub_b)

    # Return hub specified by direct hash index ID. This method will be necessary to reference the hub object throughout
    # the program.
    def get_hub(self, index):
        return self.hub_list[index]

    # Return direct hash index ID of hub specified by delivery address.
    def get_hub_id(self, hub_address):
        for row in range(len(self.hub_list)):
            if self.hub_list[row].address == hub_address:
                return row
            else:
                return None

    # Return hub address specified by hub ID number
    def get_hub_address_by_id(self, hub_id):
        for row in range(len(self.hub_list)):
            if self.hub_list[row].hub_id == hub_id:
                return self.hub_list[row].address


# Truck class represents trucks owned by WGU. Tracks relevant information like how many
# packages can be carried and remain to be delivered, and the mileage on the vehicle. Can be
# updated later to include information like make and model, insurance status, fuel, and
# maintenance. Also has a method to add packages to the truck based on their priority and zip code, deliver them,
# and return to base, adding mileage where appropriate and keeping track of time spent on deliveries.
# Uses Dijkstra's algorithm to find shortest path between hubs for delivery.
class Truck(Hubs):
    def __init__(self, truck_name, max_packages, mileage, location, hours, minutes, seconds):
        self.regular_current_packages = []
        self.priority_current_packages = []
        self.priority_current_route = []
        self.regular_current_route = []
        self.name = truck_name
        self.max_packages = max_packages
        self.mileage = mileage
        self.location = location
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    # Load specified package from its delivery list onto the truck, and remove it from the list of packages in the
    # depot waiting for delivery.
    def load_regular_individual_package(self, package, delivery_list):
        if (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
            self.regular_current_packages.append(str(package))
            delivery_list.remove(str(package))
        else:
            print('This truck is already full, please remove a package before adding another.')

    def load_priority_individual_package(self, package, delivery_list):
        if (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
            self.priority_current_packages.append(str(package))
            delivery_list.remove(str(package))
        else:
            print('This truck is already full, please remove a package before adding another.')

    # Remove specified package on truck and put it in the special_instructions_list as an individual case to be
    # handled separately.
    def remove_individual_package(self, package):
        special_instructions_list.append(package)
        if package in self.regular_current_packages:
            self.regular_current_packages.remove(package)
        if package in self.priority_current_packages:
            self.priority_awaiting_delivery_list.remove(package)

    # Checks if there are regular packages awaiting delivery. If there are packages waiting, checks if there is room
    # in the truck. If there is, loads from the back end of the list until the truck is full or the list is empty.
    def load_truck_regular(self):
        if len(default_awaiting_delivery_list) > 0:
            while (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
                try:
                    self.regular_current_packages.append(default_awaiting_delivery_list.pop())
                except IndexError:
                    break

    # Checks if there are priority packages awaiting delivery. If there are packages waiting, checks if there is room
    # in the truck. If there is, loads from the back end of the list until the truck is full or the list is empty.
    def load_truck_priority(self):
        if len(priority_awaiting_delivery_list) > 0:
            while (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
                try:
                    self.priority_current_packages.append(priority_awaiting_delivery_list.pop())
                except IndexError:
                    break

    # For each package in truck, checks each package delivery address for matching hub address and adds that hub
    # to a list of hubs that will be delivered to. Called every time a truck is loaded, and when a delivery to a hub
    # is made.
    def build_current_route(self):
        for delivery_package in self.priority_current_packages:
            for hub in master_hubs.hub_list:
                if master_packages.get_package_address_by_id(str(delivery_package)) == \
                        master_hubs.get_hub_address_by_id(hub.hub_id):
                    if hub not in self.priority_current_route:
                        self.priority_current_route.append(hub)
        for delivery_package in self.regular_current_packages:
            for hub in master_hubs.hub_list:
                if master_packages.get_package_address_by_id(str(delivery_package)) == \
                        master_hubs.get_hub_address_by_id(hub.hub_id):
                    if hub not in self.regular_current_route:
                        self.regular_current_route.append(hub)

    # Check to see if current hub is in route. If it is, it has been visited and is removed from the route.
    def remove_hub_from_route(self):
        for hub in self.priority_current_route:
            if hub == self.location:
                self.priority_current_route.remove(hub)
        for hub in self.regular_current_route:
            if hub == self.location:
                self.regular_current_route.remove(hub)

    # Calculates the amount of time it takes for a delivery in seconds, given a speed of 18 mph, and breaks it into
    # hours, minutes, and seconds added to the time attributes of the truck for keeping military time. For use in
    # get_shortest_path method.
    def travel_time(self, miles):
        time_in_transit = (miles * 3600) / 18  # Total number of seconds
        self.seconds = (self.seconds + time_in_transit) % 60  # Computes seconds on clock
        time_in_transit = time_in_transit / 60  # Variable is now remaining minutes
        self.minutes = (self.minutes + time_in_transit) % 60  # Computes minutes on clock
        time_in_transit = time_in_transit / 60  # Variable is now remaining hours
        self.hours = (self.hours + time_in_transit)

    # Provide master_hubs.get_hub(index) for start_hub. Calculates shortest path.
    def dijkstras_shortest_path(self, master_hubs, start_hub):
        self.clean_dijkstra_distances()  # Clean distance variables before use
        unvisited_queue = []  # All hubs in unvisited queue
        for current_hub in master_hubs.adjacency_list:
            unvisited_queue.append(current_hub)
        start_hub.distance = 0  # Starting hub has 0 distance from self
        while len(unvisited_queue) > 0:  # One hub removed each iteration until base case of 0 hubs remaining ends loop
            smallest_index = 0  # Visit hub with min distance from start_hub
            for i in range(1, len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_hub = unvisited_queue.pop(smallest_index)
            # Check path lengths from current hub to all neighbors
            for adj_hub in master_hubs.adjacency_list[current_hub]:
                edge_weight = float(master_hubs.edge_weights[(current_hub, adj_hub)])
                alternate_path_distance = current_hub.distance + edge_weight
                # If shorter path from start_hub to adj_hub is found, update adj_hub distance and predecessor
                if alternate_path_distance < adj_hub.distance:
                    adj_hub.distance = alternate_path_distance
                    adj_hub.predecessor_hub = current_hub

    # For use with dijkstras. Will reset the distances so dijkstras can be called repeatedly on the same graph without
    # inaccurately importing outdated distance values.
    def clean_dijkstra_distances(self):
        for hub in master_hubs.hub_list:
            hub.distance = float('inf')

    # While there are packages to be delivered in the truck, recursively build routes from each hub visited to each
    # other hub truck has packages for. Deliver packages to each location, printing out details about time and mileage
    # at each hub. Once all packages are delivered, return to WGU delivery center and print out details about time
    # and mileage.
    def deliver_route(self):
        while (len(self.regular_current_packages) or len(self.priority_current_packages)) != 0:  # Check for packages
            self.build_current_route()  # Build list of hubs to be visited based on packages
            self.dijkstras_shortest_path(master_hubs, self.location)  # Build routes from current location
            print('\nCurrent Location of Truck ' + str(self.name) + ': ' + str(self.location.name))
            self.remove_hub_from_route()  # Remove current location from list of hubs to be visited
            if len(self.priority_current_route) > 0:  # Check if list of priority hubs is empty
                next_delivery = min(self.priority_current_route, key=attrgetter('distance'))  # Find next closest hub
            elif len(self.regular_current_route) > 0:  # Check if list of regular hubs is empty
                next_delivery = min(self.regular_current_route, key=attrgetter('distance'))  # Find next closest hub
            print('Driving to ' + str(next_delivery.name))
            self.travel_time(next_delivery.distance)  # Add time to travel to next delivery
            self.mileage += next_delivery.distance  # Add mileage to travel to next delivery
            print('Miles Traveled: ' + str(next_delivery.distance))  # Print updates on travel details
            print('Time of Delivery: ' + str(int(self.hours)) + ': ' + str(int(self.minutes)) + ': '
                  + str(int(self.seconds)))
            print('Current Mileage of This Truck: ' + str(self.mileage))
            print('Packages Delivered Today: ' + str(delivered_list))
            self.location = next_delivery  # Update to new location
            priority_new_package_list = []  # List of priority packages to be retained in truck
            regular_new_package_list = []
            priority_packages_delivered_at_hub = []  # Priority packages delivered this location
            regular_packages_delivered_at_hub = []  # Regular packages delivered this location
            for package in self.priority_current_packages:  # Deliver priority packages addressed to location
                #   If package is not address to current location, keep in truck
                if master_packages.get_package_address_by_id(str(package)) != self.location.address:
                    priority_new_package_list.append(package)  # Add non-delivered package to list
                # If package is addressed to current location, deliver
                elif master_packages.get_package_address_by_id(str(package)) == self.location.address:
                    delivered_list.append(package)  # Add to list of delivered packages
                    priority_packages_delivered_at_hub.append(package)  # Report for packages delivered this location
            for package in self.regular_current_packages:  # Deliver regular packages addressed to location
                #   If package is not address to current location, keep in truck
                if master_packages.get_package_address_by_id(str(package)) != self.location.address:
                    regular_new_package_list.append(package)  # Add non-delivered package to list
                # If package is addressed to current location, deliver
                elif master_packages.get_package_address_by_id(str(package)) == self.location.address:
                    delivered_list.append(package)  # Add to list of delivered packages
                    regular_packages_delivered_at_hub.append(package)  # Report for packages delivered this location
            self.priority_current_packages = priority_new_package_list  # Update truck inventory
            self.regular_current_packages = regular_new_package_list  # Update truck inventory
            print('Priority Packages Delivered This Location: ', priority_packages_delivered_at_hub)
            print('Regular Packages Delivered This Location: ', regular_packages_delivered_at_hub)
            print('Regular Packages Remaining This Route: ' + str(self.regular_current_packages))
            print('Priority Packages Remaining This Route: ' + str(self.priority_current_packages))
        self.return_to_wgu()  # Return to WGU when packages have been delivered.

    # Employs dijkstras to calculate efficient route back to WGU package center from current location then moves there.
    # Once at center, updates global mileage variable with mileage on vehicle.
    def return_to_wgu(self):
        self.dijkstras_shortest_path(master_hubs, self.location)  # Build route
        print('\nAll Packages delivered by Truck ' + str(self.name) + '. Returning to WGU from ' +
              str(self.location.name))
        print('Distance from WGU = ' + str(master_hubs.get_hub(0).distance))
        print('Driving from : ' + str(self.location.name))
        print('Driving to : ' + str(master_hubs.get_hub(0).name))
        self.travel_time(master_hubs.get_hub(0).distance)  # Time to drive back to WGU
        self.mileage += master_hubs.get_hub(0).distance  # Miles to get back to WGU
        print('Miles Traveled: ' + str(master_hubs.get_hub(0).distance))  # Print updates on travel details
        print('Time of Arrival: ' + str(int(self.hours)) + ': ' + str(int(self.minutes)) + ': '
              + str(int(self.seconds)))
        print('Total Mileage of this truck: ' + str(self.mileage))
        print('Packages Delivered Today: ' + str(delivered_list))
        self.location = master_hubs.get_hub(0)
        print('Arrived at ' + str(self.location.name))


# Package class represents packages to be delivered as individuals. Contains delivery relevant information
# about the package: package ID, delivery address, deadline for delivery, and package weight.
class Package:
    def __init__(self, package_id, package_address, city, state, package_zip_code, deadline, mass, note):
        self.package_id = package_id
        self.address = package_address
        self.city = city
        self.state = state
        self.zip_code = package_zip_code
        self.deadline = deadline
        self.mass = mass
        self.note = note


# Packages class represents packages to be delivered as a group. Contains a list of all packages, and methods
# to pull them up from that list. Packages are stored as a direct hash using package ID as the index.
class Packages:
    def __init__(self):
        self.package_list = []
        pass

    # Add a note to a package. Index position in list is 1 less than the package ID number.
    def add_note(self, package, input):
        master_packages.get_package(package - 1).note = str(input)

    # Add package to list of packages, for use by master_package.
    def add_package(self, package_to_add):
        self.package_list.append(package_to_add)

    # Return package specified by direct hash package ID.
    def get_package(self, index):
        return self.package_list[index]

    # Return list of package IDs specified by zip code.
    def get_packages_by_zip(self, zip_code):
        packages_by_zip = []
        for row in range(len(self.package_list)):
            if self.package_list[row].zip_code == zip_code:
                packages_by_zip.append(self.package_list[row].package_id)
        if len(packages_by_zip) > 0:
            return packages_by_zip
        else:
            return None

    # Return a nested dictionary of packages grouped by zip code, using zip and ID as key : value pairs.
    def group_packages_by_zip(self):
        packages_grouped_by_zip = {}
        for row in range(len(self.package_list)):
            packages_grouped_by_zip.setdefault(self.package_list[row].zip_code,
                                               []).append(self.package_list[row].package_id)
        if len(packages_grouped_by_zip) > 0:
            return packages_grouped_by_zip
        else:
            return None

    # Return list of package IDs specified by delivery address.
    def get_packages_by_address(self, address):
        packages_by_address = []
        for row in range(len(self.package_list)):
            if self.package_list[row].address == address:
                packages_by_address.append(self.package_list[row].package_id)
        if len(packages_by_address) > 0:
            return packages_by_address
        else:
            return None

    # Return list of packages with a delivery deadline.
    def get_packages_by_deadline(self):
        packages_by_deadline = []
        for row in range(len(self.package_list)):
            if self.package_list[row].deadline != 'EOD':
                packages_by_deadline.append(self.package_list[row].package_id)
        if len(packages_by_deadline) > 0:
            return packages_by_deadline
        else:
            return None

    # Return list of packages with a note for special instructions.
    def get_packages_by_note(self):
        packages_by_note = []
        for package in master_packages.package_list:
            if len(package.note) > 0:
                packages_by_note.append(package.package_id)
        if len(packages_by_note) > 0:
            return packages_by_note
        else:
            return None

    # Return direct hash index ID of package specified by delivery address.
    def get_package_id(self, address):
        for row in range(len(self.package_list)):
            if self.package_list[row].address == address:
                return row
            else:
                return None

    # Return package address specified by package ID number
    def get_package_address_by_id(self, package_id):
        for row in range(len(self.package_list)):
            if self.package_list[row].package_id == package_id:
                return self.package_list[row].address


# Main program

# Build Master reference lists to keep track of variables representing objects being delivered, and their relationships
# with other objects.
master_hubs = Hubs()
master_packages = Packages()

# Read in formatted CSV file (no header, hidden characters stripped, zip code as separate comma separated value),
# iterate through each line, and create instance of Hub class for each location. In addition to instantiating Hub
# variables, also instantiate a Hubs variable to create a master reference. This reference uses the index automatically
# assigned by the csv reader when it populates the list as a direct hash for storing and referencing individual hubs.
# This hash value will be used in all cases as a consistent hub ID.
with open('wguDistanceTableFormatted.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for index, location in enumerate(csv_reader):
        h = Hub(index, location[0], location[1], location[2], location[3:])
        master_hubs.add_hub(h)

# Read in formatted CSV file (no header, hidden characters stripped), iterate through each line, and create instance
# of Package class for each package. While doing so, instantiate a Packages variable to create a master reference.
# This reference uses the package ID number as a direct hash for sorting and referencing individual packages.
with open('wguPackageTableFormatted.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for package in csv_reader:
        p = Package(package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7])
        master_packages.add_package(p)

# Instantiate truck objects to hold and deliver packages, track time and mileage, and calculate efficient delivery
# routes. Create lists to track package delivery categories, and delivery status, variable to track total daily mileage.
default_awaiting_delivery_list = []
special_instructions_list = []
priority_awaiting_delivery_list = []
delivered_list = []
truck_a = Truck('A', 16, 0, master_hubs.get_hub(0), 8, 0, 0)
truck_b = Truck('B', 16, 0, master_hubs.get_hub(0), 9, 5, 0)  # Truck 2, responsible for deadline deliveries
truck_c = Truck('C', 16, 0, master_hubs.get_hub(0), 8, 0, 0)

# Check for packages with individual handling instructions requiring individual attention. All packages with notes will
# be handled individually to ensure compliance with special instructions. Update notes on other packages where
# appropriate.
master_packages.add_note(13, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
master_packages.add_note(16, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
master_packages.add_note(20, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
master_packages.add_note(15, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
master_packages.add_note(14, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
master_packages.add_note(19, 'Package Group Delivery: 13, 16, 20, 15, 14, 19')
print('The following packages have individual handling instructions: ' + str(master_packages.get_packages_by_note()))

# Iterate through dictionary provided by get_packages_by_zip method and build a list of packages sequenced
# by zip code. This will later be iterated through when loading trucks
# to be sure that packages are grouped by zip for deliveries.
for packages in master_packages.group_packages_by_zip().values():
    for package in packages:
        default_awaiting_delivery_list.append(package)

# Iterate through the master_packages list to search for all packages with priority delivery deadlines. If any found
# packages are also in the default_awaiting_delivery_list, they are removed from that list and added to the
# priority_awaiting_delivery_list.
for package in master_packages.get_packages_by_deadline():
    if package in default_awaiting_delivery_list:
        priority_awaiting_delivery_list.append(package)
        default_awaiting_delivery_list.remove(package)

# Iterate through the master_packages list to search for all packages with special instructions. If any found packages
# are also in the default_awaiting_delivery_list or the priority_awaiting_delivery_list, they are removed from that
# list and added to the special_instructions list.
for package in master_packages.get_packages_by_note():
    if package in default_awaiting_delivery_list:
        special_instructions_list.append(package)
        default_awaiting_delivery_list.remove(package)
    if package in priority_awaiting_delivery_list:
        special_instructions_list.append(package)
        priority_awaiting_delivery_list.remove(package)

# Build graph to represent route for trucks to deliver between hubs. Edge weights are distances imported from CSV
for hub in master_hubs.hub_list:
    for adjacent_hub in master_hubs.hub_list:
        master_hubs.add_undirected_edge(hub, adjacent_hub, hub.neighbors[adjacent_hub.hub_id])

# Load Truck A with priority packages without deadlines or special instructions
truck_a.load_truck_priority()  # Priority packages loaded up automatically
# Fill remainder of Truck A with regular packages
truck_a.load_truck_regular()    # Regular packages loaded up automatically
# Truck A leaves depot at 0800 military time to deliver its route. Last priority package (#30) is delivered to Council
# Hall at 0910 military time. Regular packages are then delivered, and the truck returns to the WGU depot at
# 1044 military time with 49 total miles driven
truck_a.deliver_route() # Mileage: 49

# At 0905 military time, late packages arrive. Load up those late arrivals with a priority deadline individually.
truck_b.load_priority_individual_package(6, special_instructions_list)
truck_b.load_priority_individual_package(13, special_instructions_list)
truck_b.load_priority_individual_package(16, special_instructions_list)
truck_b.load_priority_individual_package(20, special_instructions_list)
truck_b.load_priority_individual_package(15, special_instructions_list)
truck_b.load_priority_individual_package(14, special_instructions_list)
truck_b.load_priority_individual_package(19, special_instructions_list)
truck_b.load_priority_individual_package(25, special_instructions_list)
# Fill in remainder with other special packages with individual handling instructions (packages that must be delivered
# by Truck B), then finally fill in with remaining regular packages. Package #9 has not had its address updated yet,
# so it is not loaded.
truck_b.load_regular_individual_package(3, special_instructions_list)
truck_b.load_regular_individual_package(18, special_instructions_list)
truck_b.load_regular_individual_package(28, special_instructions_list)
truck_b.load_regular_individual_package(32, special_instructions_list)
truck_b.load_regular_individual_package(36, special_instructions_list)
truck_b.load_regular_individual_package(38, special_instructions_list)
truck_b.load_truck_regular()    # Regular packages automatically loaded
# Truck B leaves depot at 0905 military time. Last priority package (#13) is delivered to Salt Lake City Streets and
# Sanitation at 1009 miltary time. Regular packages are then delivered, and the truck returns to the WGU depot at 1156
# military time with 51.5 total miles driven.
truck_b.deliver_route() # Mileage: 51.5

# When Truck A returns from its first delivery, the address on package #9 has been updated. The truck loads up all
# remaining packages, which are all regular packages except for #9, then delivers its route.
truck_a.load_truck_regular()    # Regular packages automatically loaded
truck_a.load_regular_individual_package(9, special_instructions_list)
# Truck A leaves depot at 1044 military time. No packages are priority, so deadlines are not a concern. Last packages
# (#8 and #9) are delivered to Council Hall at 1125 military time, then the truck returns to the WGU depot at 1150
# military time with 69 total miles driven.
truck_a.deliver_route() # Mileage: 59

# All packages have been delivered at this point, and the day is finished before lunch at noon.
print('\nList of packages delivered today: ' + str(delivered_list))
print('All packages delivered.')
print('Total mileage of all delivery trucks today: ' + str(truck_a.mileage + truck_b.mileage + truck_c.mileage))

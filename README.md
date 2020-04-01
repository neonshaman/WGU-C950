# WGU-C950

This project was the culmination of Data Structures & Algorithms I & II. It was developed with Python in the Pycharm IDE.

In this project, I was presented with the following scenario:

"The Western Governors University Parcel Service (WGUPS) needs to determine the best route and delivery distribution for their Daily Local Deliveries (DLD) because packages are not currently being consistently delivered by their promised deadline. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day; each package has specific criteria and delivery requirements.
Your task is to determine the best algorithm, write code, and present a solution where all 40 packages, listed in the attached “WGUPS Package File,” will be delivered on time with the least number of miles added to the combined mileage total of all trucks. The specific delivery locations are shown on the attached “Salt Lake City Downtown Map” and distances to each location are given in the attached “WGUPS Distance Table.”
While you work on this assessment, take into consideration the specific delivery time expected for each package and the possibility that the delivery requirements—including the expected delivery time—can be changed by management at any time and at any point along the chosen route. In addition, you should keep in mind that the supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed in the “WGUPS Package File,” including what has been delivered and what time the delivery occurred.
The intent is to use this solution (program) for this specific location and to use the same program in many cities in each state where WGU has a presence. As such, you will need to include detailed comments, following the industry-standard Python style guide, to make your code easy to read and to justify the decisions you made while writing your program.

Assumptions:

•  Each truck can carry a maximum of 16 packages.

•  Trucks travel at an average speed of 18 miles per hour.

•  Trucks have a “infinite amount of gas” with no need to stop.

•  Each driver stays with the same truck as long as that truck is in service.

•  Drivers leave the hub at 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed. The day ends when all 40 packages have been delivered.

•  Delivery time is instantaneous, i.e., no time passes while at a delivery (that time is factored into the average speed of the trucks).


•  There is up to one special note for each package.
•  The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.

•  The package ID is unique; there are no collisions.

•  No further assumptions exist or are allowed."

This project is a console application that simulates a solution. It takes in two CSV files and from a parse of the data within them generates an efficient route for drivers to take, optimizing for mileage. It employs Dijkstra's algorithm as the core (making careful point to clean the graph after each use), bounding it within mailing zip codes to prevent undesireable edge case behavior. Included is a paper analyzing the complexity of the solution with a code walkthrough.

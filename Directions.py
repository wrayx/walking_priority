from datetime import datetime

# from datetime import timedelta
# from datetime import date

import json
import pprint

import googlemaps

from Route import Route


class Directions:
    """class for storing all routes recommended by Google Maps"""

    def __init__(
        self,
        start,
        end,
        mode="transit",
        alternatives=True,
        departure_time=datetime(
            year=2023,
            month=7,
            day=31,
            hour=14,
            minute=0,
            second=0,
        ),
        output_file="output/directions.json",
    ):
        self.mode = mode
        self.origin_input = start
        self.destination_input = end
        self.origin = ""
        self.destination = ""
        self.routes = []
        self.alternatives = alternatives
        self.departure_time = departure_time
        self.output_file = output_file

        # setup API key
        self.setup()

    def setup(self):
        """set up the api key for the directions platform"""
        # store api key in api_key variable
        with open("api_key.txt", encoding="utf8") as file:
            self.key = file.readline()

        self.client = googlemaps.Client(self.key)

    def get_directions_transit(self):
        """request directions/routes from Google Maps APIs"""
        # set the test date time on tomorrow 13.00
        # current_date = date.today() + timedelta(days=7)
        # test_datetime = datetime(
        #     year=current_date.year,
        #     month=current_date.month,
        #     day=current_date.day,
        #     hour=14,
        #     minute=0,
        #     second=0,
        # )
        # test_datetime = datetime(
        #     year=2023,
        #     month=7,
        #     day=31,
        #     hour=14,
        #     minute=0,
        #     second=0,
        # )

        directions_result = self.client.directions(
            self.origin_input,
            self.destination_input,
            mode=self.mode,
            alternatives=True,
            departure_time=self.departure_time,
        )

        # save output to a file
        self.save_output(directions_result)
        self.save_pretty_output(directions_result)

        for output in directions_result:
            self.parse_output_and_save(output)
            break  # stop after the first entry
            # if self.alternatives is False:
            #     # stop after the first entry
            #     break

    def parse_output_and_save(self, output):
        """parse useful information from json output and and save information as class variables"""

        self.origin = output["legs"][0]["start_address"]
        self.destination = output["legs"][0]["end_address"]

        route = Route(self.origin, self.destination)

        route.setTotalDuration(output["legs"][0]["duration"]["value"])
        route.setTotalDistance(output["legs"][0]["distance"]["value"])

        travel_modes = []
        travel_distances = []
        travel_durations = []
        origin_destination_pairs = []
        waypoints = []

        for step in output["legs"][0]["steps"]:
            travel_mode = step["travel_mode"]

            distance = step["distance"]["value"]
            duration = step["duration"]["value"]
            travel_distances.append(distance)
            travel_durations.append(duration)
            waypoints.append(step["end_location"])

            if travel_mode == "WALKING":
                travel_modes.append((travel_mode.capitalize(), step["html_instructions"]))
                origin_destination_pairs.append(("n/a", "n/a"))
            if travel_mode == "TRANSIT":
                travel_modes.append((travel_mode.capitalize(), step["transit_details"]["line"]["color"]))
                depart = step["transit_details"]["departure_stop"]["name"]
                arrive = step["transit_details"]["arrival_stop"]["name"]
                origin_destination_pairs.append((depart, arrive))

        route.setTravelModes(travel_modes)
        route.setTravelDurations(travel_durations)
        route.setTravelDistances(travel_distances)
        route.setPartialOriginDestinationPairs(origin_destination_pairs)
        route.setWaypoints(waypoints)
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(waypoints))
            f.write("\n")
            f.write(json.dumps(travel_modes))
            f.write("\n")
        print(waypoints)
        print(travel_modes)

        self.routes.append(route)

    # saves the json output to an external file
    def save_output(self, output_json):
        """save the json output to file"""
        with open("output/result_directions_original.json", "w", encoding="utf8") as file:
            file.write(json.dumps(output_json))

    # fetch the json output from an external file
    def fetch_output(self, output_json_path):
        """fetch json output from a file"""
        with open(output_json_path, encoding="utf-8") as file:
            output = json.load(file)
        return output

    # save pretty version of json file to an external file
    def save_pretty_output(self, output_json):
        """save the prettified json output to file"""
        pretty_print_json = pprint.pformat(output_json).replace("'", '"')
        with open("output/result_directions_pp.json", "w", encoding="utf8") as file:
            file.write(pretty_print_json)

    # display class variables
    def display_directions_result(self):
        """display the route information"""
        print(f"Input Start:\t{self.origin_input}")
        print(f"Input End:\t{self.destination_input}\n")
        print(f"Start address:\t{self.origin}")
        print(f"End address:\t{self.destination}\n")

        num_route = 0

        for route in self.routes:
            num_route += 1
            print(f"ROUTE {num_route}")

            if self.mode == "transit":
                print("Steps are as follows:")
                print("========================")

                num_steps = 0

                for i, travel_mode in enumerate(route.travel_modes):
                    # print("!!!!!!!!!!")
                    # print(route.travel_modes[i][0])
                    # print("!!!!!!!!!!")
                    num_steps += 1
                    print(f"STEP {num_steps}")
                    print(f"travel mode:\t{travel_mode[0]}")
                    print(f"instruction:\t{travel_mode[1]}")
                    if route.origin_destination_pairs[i][0] != "n/a" and route.origin_destination_pairs[i][1] != "n/a":
                        print(f"depart at: \t{route.origin_destination_pairs[i][0]}")
                        print(f"arrive at: \t{route.origin_destination_pairs[i][1]}")

                    print(f"distance: \t{Route.str_distance(route.travel_distances[i])}")
                    print(f"time taken: \t{Route.str_duration(route.travel_durations[i])}")
                    print("========================")
            else:
                # print("!!!!!!!!!!")
                # print(route.travel_modes[0][0])
                # print("!!!!!!!!!!")
                # the only travel mode is walking
                print(f"travel mode:\t{self.mode}")

            print("\n[In total]")
            print(f"distance: \t{Route.str_distance(route.total_distance)}")
            print(f"time taken: \t{Route.str_duration(route.total_duration)}")
            print(f"walking time: \t{Route.str_duration(route.getTotalWalkingDuration())}")
            print(f"tp time: \t{Route.str_duration(route.getTotalTransportingDuration())}\n\n")

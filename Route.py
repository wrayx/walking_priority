from datetime import timedelta


class Route:
    def __init__(self, origin, destination) -> None:
        self.origin = origin
        self.destination = destination
        self.travel_modes = []
        self.travel_distances = []
        self.travel_durations = []
        self.origin_destination_pairs = []
        self.waypoints = []
        self.total_duration = -1
        self.total_distance = -1

    def setTravelModes(self, travel_modes: list):
        self.travel_modes = travel_modes

    def getTravelModes(self):
        return self.travel_modes

    def getTransfersTimes(self):
        return len(self.travel_modes)

    def setTravelDistances(self, travel_distances: list):
        self.travel_distances = travel_distances

    def setTravelDurations(self, travel_durations: list):
        self.travel_durations = travel_durations

    def setWaypoints(self, waypoints: list):
        self.waypoints = waypoints

    def getWaypoints(self):
        return self.waypoints

    def setPartialOriginDestinationPairs(self, origin_destination_pairs: list):
        self.origin_destination_pairs = origin_destination_pairs

    def setTotalDuration(self, total_duration):
        self.total_duration = total_duration

    def getTotalDuration(self):
        return self.total_duration

    def setTotalDistance(self, total_distance):
        self.total_distance = total_distance

    def getTotalWalkingDuration(self) -> int:
        total_time = 0
        for i, travel_mode in enumerate(self.travel_modes):
            if travel_mode[0] == "Walking":
                total_time += self.travel_durations[i]
        return total_time

    def getTotalTransportingDuration(self) -> int:
        # time spent on transportation includes time waiting for train or buses to come
        return self.total_duration - self.getTotalWalkingDuration()

    @staticmethod
    def str_distance(distance):
        """format distance value from meter to kilo meter"""
        return f"{round(distance / 1000, 3)} km"

    @staticmethod
    def str_duration(duration):
        """format duration value from seconds to h:m:s"""
        convert = str(timedelta(seconds=duration))
        return convert

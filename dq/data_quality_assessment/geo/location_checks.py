class LocationChecks:
    """
    A class to perform checks on location data, focusing on geo coordinates.
    """

    def __init__(self, locations):
        """
        Initializes the LocationChecks class with location data.

        :param locations: A list of tuples containing (latitude, longitude).
        """
        self.locations = locations

    def check_coordinates_format(self):
        """
        Validates the format of geo coordinates.

        :return: A list of booleans indicating whether each location has valid latitude and longitude values.
        """
        valid_format = []
        for lat, lon in self.locations:
            valid_lat = -90 <= lat <= 90
            valid_lon = -180 <= lon <= 180
            valid_format.append(valid_lat and valid_lon)
        return valid_format

    def check_within_bounds(self, south_west, north_east):
        """
        Checks if the locations are within specified geographic boundaries.

        :param south_west: A tuple containing the (latitude, longitude) of the southwest boundary corner.
        :param north_east: A tuple containing the (latitude, longitude) of the northeast boundary corner.
        :return: A list of booleans indicating whether each location is within the bounds.
        """
        within_bounds = []
        for lat, lon in self.locations:
            within_lat = south_west[0] <= lat <= north_east[0]
            within_lon = south_west[1] <= lon <= north_east[1]
            within_bounds.append(within_lat and within_lon)
        return within_bounds


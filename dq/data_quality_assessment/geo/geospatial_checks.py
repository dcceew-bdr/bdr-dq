import numpy as np

class GeospatialDataQuality:
    """
    A class for assessing the quality of geo data, including detecting outliers.
    """

    @staticmethod
    def calculate_median_absolute_deviation(coordinates):
        """
        Calculate the Median Absolute Deviation (MAD) for geo data.

        :param coordinates: A list of tuples/lists where each tuple/list contains the latitude and longitude.
        :return: MAD for latitude and longitude.
        """
        latitudes, longitudes = zip(*coordinates)
        med_lat = np.median(latitudes)
        med_long = np.median(longitudes)
        mad_lat = np.median([abs(lat - med_lat) for lat in latitudes])
        mad_long = np.median([abs(long - med_long) for long in longitudes])
        return mad_lat, mad_long

    @staticmethod
    def detect_outliers(coordinates, threshold=3):
        """
        Detect outliers in geo data using the MAD method.

        :param coordinates: A list of tuples/lists where each tuple/list contains the latitude and longitude.
        :param threshold: The threshold for detecting outliers (the number of MADs away from the median).
        :return: A list of booleans indicating whether each coordinate is an outlier.
        """
        mad_lat, mad_long = GeospatialDataQuality.calculate_median_absolute_deviation(coordinates)
        med_lat = np.median([lat for lat, _ in coordinates])
        med_long = np.median([long for _, long in coordinates])

        is_outlier = []
        for lat, long in coordinates:
            deviation_lat = abs(lat - med_lat) / mad_lat if mad_lat else 0
            deviation_long = abs(long - med_long) / mad_long if mad_long else 0
            is_outlier.append(deviation_lat > threshold or deviation_long > threshold)
        return is_outlier

    @staticmethod
    def assess_coordinate_precision(longitude, latitude):
        """
        Assess the precision of geographic coordinates based on the number of decimal places.

        :param longitude: The longitude as a string.
        :param latitude: The latitude as a string.
        :return: A label indicating the precision quality ("High", "Medium", or "Low").
        """

        def assess_quality(decimal_length):
            if decimal_length > 4:
                return "High"
            elif 2 <= decimal_length <= 4:
                return "Medium"
            else:
                return "Low"

        lat_precision = len(latitude.split('.')[-1]) if '.' in latitude else 0
        long_precision = len(longitude.split('.')[-1]) if '.' in longitude else 0

        lat_quality = assess_quality(lat_precision)
        long_quality = assess_quality(long_precision)

        # Return the lower quality of the two as the overall quality
        if lat_quality == "Low" or long_quality == "Low":
            return "Low"
        elif lat_quality == "Medium" or long_quality == "Medium":
            return "Medium"
        else:
            return "High"



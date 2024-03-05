import numpy as np


class OutlierDetection:
    """
    A class for detecting outliers in outlier data using different statistical methods.
    """

    def __init__(self, data):
        """
        Initializes the OutlierDetection class with outlier data.

        :param data: A list or array-like structure containing outlier data.
        """
        self.data = np.array(data)  # Convert data to NumPy array for efficient computations

    def iqr_outliers(self):
        """
        Identifies outliers using the Interquartile Range (IQR) method.

        :return: A boolean array where True indicates an outlier.
        """
        quartile1, quartile3 = np.percentile(self.data, [25, 75])
        iqr = quartile3 - quartile1
        lower_bound = quartile1 - (1.5 * iqr)
        upper_bound = quartile3 + (1.5 * iqr)

        # Identify outliers
        outliers = (self.data < lower_bound) | (self.data > upper_bound)
        return outliers

    def z_score_outliers(self, threshold=3):
        """
        Identifies outliers using the Z-score method.

        :param threshold: The Z-score threshold to identify an outlier. Defaults to 3.
        :return: A boolean array where True indicates an outlier.
        """
        mean = np.mean(self.data)
        std_dev = np.std(self.data)
        z_scores = np.abs((self.data - mean) / std_dev)

        # Identify outliers
        outliers = z_scores > threshold
        return outliers


from datetime import datetime


class DateChecks:
    """
    A class for performing various checks on date data to assess its quality.
    Includes methods for checking date formats and validating date ranges.
    """

    def __init__(self, data, date_format="%Y-%m-%d"):
        """
        Initializes the DateChecks class with date data.

        :param data: A list or array-like structure containing date data as strings.
        :param date_format: The expected format of the date strings (default is ISO format: "%Y-%m-%d").
        """
        self.data = data
        self.date_format = date_format

    def check_date_format(self):
        """
        Validates the format of date strings in the dataset.

        :return: A list of booleans indicating whether each date string matches the expected format.
        """
        checks = []
        for date_str in self.data:
            try:
                datetime.strptime(date_str, self.date_format)
                checks.append(True)
            except ValueError:
                checks.append(False)
        return checks

    def check_date_range(self, start_date, end_date):
        """
        Checks if dates in the dataset fall within a specified date range.

        :param start_date: The start date of the acceptable range as a string.
        :param end_date: The end date of the acceptable range as a string.
        :return: A list of booleans indicating whether each date falls within the specified range.
        """
        start_date = datetime.strptime(start_date, self.date_format)
        end_date = datetime.strptime(end_date, self.date_format)
        checks = []
        for date_str in self.data:
            date = datetime.strptime(date_str, self.date_format)
            checks.append(start_date <= date <= end_date)
        return checks

    def find_date_format(self):
        """
        Method to find and return the format of a given date string.
        Returns the format string if a common format is detected, otherwise None.
        """
        date_formats = [
            "%Y-%m-%d",  # YYYY-MM-DD
            "%d/%m/%Y",  # DD/MM/YYYY
            "%m/%d/%Y",  # MM/DD/YYYY
            "%Y/%m/%d",  # YYYY/MM/DD (included for completeness)
        ]

        for fmt in date_formats:
            try:
                datetime.strptime(self.data, fmt)
                return fmt
            except ValueError:
                continue
        return None

    def check_date_format_and_validate(self):
        """
        Method to both detect the date format of a given string and validate the date.
        Returns a tuple of (boolean, format) indicating whether the date is valid and its format.
        """
        detected_format = self.find_date_format()
        if detected_format:
            try:
                # If a format is detected, try to parse it to validate the date.
                valid_date = datetime.strptime(self.data, detected_format)
                return (True, detected_format)  # Date is valid and format is returned
            except ValueError:
                return (False, detected_format)  # Date string is invalid but format is detected
        else:
            return (False, None)  # No valid format found


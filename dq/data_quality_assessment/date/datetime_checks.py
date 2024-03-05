from datetime import datetime
from rdflib import XSD, Literal
class DateTimeDataQuality:
    """
    A class for assessing the quality of date data.
    """

    @staticmethod
    def is_valid_date(date_str, date_format="%Y-%m-%d"):
        """
        Validates if the given string matches the specified date format.

        :param date_str: The date string to validate.
        :param date_format: The format to validate against.
        :return: True if the date string is valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_within_date_range(date_str, start_date_str, end_date_str, date_format="%Y-%m-%d"):
        """
        Checks if a date falls within a specified range.

        :param date_str: The date string to check.
        :param start_date_str: The start date of the range.
        :param end_date_str: The end date of the range.
        :param date_format: The format of the provided date strings.
        :return: True if the date is within the range, False otherwise.
        """
        date = datetime.strptime(date_str, date_format)
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        return start_date <= date <= end_date

    @staticmethod
    def is_date_recent(date_literal, years_back=20):
        """
        Checks if a given RDF date literal is within the specified number of years back from the current year.

        :param date_literal: An RDF Literal with datatype XSD.date.
        :param years_back: The number of years back to consider a date as recent.
        :return: True if the date is recent, False otherwise.
        """
        if date_literal.datatype == XSD.date:
            current_year = datetime.now().year
            date_year = date_literal.toPython().year
            return (current_year - years_back) <= date_year <= current_year
        return False

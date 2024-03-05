import re


class ScientificNameDataQuality:
    """
    A class for assessing the quality of scientific name data, including validation of scientific names.
    """
    def check_empty(self, data):
        """
        Checks for empty strings in the dataset.

        :return: A list of booleans indicating whether each string is empty.
        """
        return [s == "" for s in data]

    @staticmethod
    def is_valid_scientific_name(scientific_name):
        """
        Validates if the given string follows the convention for scientific names.

        This is a basic implementation that checks if the name consists of two parts
        (genus and species) and starts with a capital letter followed by lowercase letters.
        More complex rules can be added as needed.

        :param scientific_name: The scientific name to validate.
        :return: True if the name is valid, False otherwise.
        """
        # Basic pattern for a scientific name: Genus species

        # TODO: Use the URL link for checking the scientific names

        pattern = r'^[A-Z][a-z]+(?:\s[a-z]+)?$'
        return bool(re.match(pattern, scientific_name))

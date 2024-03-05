import datetime
import difflib
import re
from datetime import datetime
from pathlib import Path
from typing import Union

import numpy as np
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import NamespaceManager, SOSA, TIME, GEO, SDO, XSD

from .data_quality_assessment.date.date_checks import DateChecks
from .data_quality_assessment.geo.australia_geography_checker import AustraliaGeographyChecker
from .data_quality_assessment.geo.geospatial_checks import GeospatialDataQuality
from dq.data_quality_assessment.date.datetime_checks import DateTimeDataQuality
from .data_quality_assessment.uri.uri_class import AssessmentTypes, BaseUris
from .defined_namespaces import DQAF, TERN
from .defined_namespaces import RDF
from .label_manager import LabelManager
from .report_analysis import ReportAnalysis


class RDFDataQualityAssessment:
    def __init__(self, g: Union[Path, Graph], report_file=None):
        self.report_file = report_file

        self.g = self.load_data(g)
        self.label_manager = LabelManager()
        self.geo_checker = AustraliaGeographyChecker()
        self.report_analysis = ReportAnalysis(self.g, report_file)

        # Call the function to bind namespaces
        self.label_manager.bind_custom_namespaces(self.g)

        # Now, graph `self.g` is initialized with all namespaces

    @staticmethod
    def load_data(path_or_graph: Union[Path, Graph]) -> Graph:
        if isinstance(path_or_graph, Path):
            return Graph().parse(source=str(path_or_graph), format='ttl')
        elif isinstance(path_or_graph, Graph):
            return path_or_graph
        else:
            raise ValueError("Input must be either a Path object pointing to a Turtle file or an RDFlib Graph")

    def assess(self):

        # Add custom labels definition to the new graph and save it into new file name
        self.label_manager.create_output_definition_file('Label_Definition.ttl')

        # Bind custom labels
        self.label_manager.bind_custom_namespaces(self.g)

        # Add methods to call the specific assessment methods here
        # Example:
        self.assess_observation_date_recency()
        self.assess_observation_date_check_format_validation()
        self.assess_coordinate_precision()
        self.assess_point_in_australia_state()
        self.assess_observation_date_outliers_irq()
        self.assess_observation_date_outliers_lower_upper_thresholds()
        self.assess_observation_location_outliers_zscore()
        self.assess_observation_location_outliers_irq()
        # TODO: Add other assessments methods

    def calculate_predicate_completeness(self, predicate_uri):
        """
        Calculate the completeness of a given predicate in the graph.

        Completeness is defined as the ratio of the number of subjects with the predicate
        to the total number of unique subjects.

        :param predicate_uri: The URI of the predicate to calculate completeness for.
        :return: Completeness ratio.
        """
        # Ensure predicate_uri is a URIRef object
        if isinstance(predicate_uri, str):
            predicate_uri = URIRef(predicate_uri)

        # Get subjects that have the specified predicate (with values)
        subjects_with_predicate = set(self.g.subjects(predicate=predicate_uri))

        # In this specific context, all subjects relevant to the predicate are those that have the predicate,
        # since we are only considering those subjects that are associated with the predicate.
        # If there's a way to determine subjects that should have the predicate but don't,
        # that logic would need to be added here.
        all_relevant_subjects = subjects_with_predicate

        # Calculate completeness
        if len(all_relevant_subjects) > 0:
            completeness = len(subjects_with_predicate) / len(all_relevant_subjects)
        else:
            completeness = 0  # Define completeness as 0 if there are no subjects at all

        return completeness

    def assess_observation_date_recency(self):
        total_assessments = 0
        namespace = self.label_manager.get_namespace("date_recency")
        result_counts = {"recent": 0, "outdated": 0}  # Initialize result counts for True and False

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if BaseUris.check_base_uri(str(s), BaseUris.OBSERVATION):
                date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if DateTimeDataQuality.is_date_recent(date_literal):
                        result_counts["recent"] += 1
                        date_within_range = True

                    else:
                        result_counts["outdated"] += 1
                    break  # Assuming only one date per observation; remove if multiple dates need assessment

                total_assessments += 1
                # Use  labels for the result
                result_label = namespace["recent"] if date_within_range else namespace["outdated"]

                self._add_assessment_result(s, AssessmentTypes.OBSERVATION_DATE_RECENCY, result_label)

        self.add_to_report('Date Recency Assessments', total_assessments, result_counts)

    def assess_coordinate_precision(self):
        total_assessments = 0
        namespace = self.label_manager.get_namespace("coordinate_precision")
        quality_counts = {"Low": 0, "Medium": 0, "High": 0}  # Use the new labels

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    longitude, latitude = match.groups()
                    precision_label = GeospatialDataQuality.assess_coordinate_precision(longitude, latitude)

                    quality_counts[
                        precision_label] += 1  # Increment by 1 to account for both lat and long assessments together

                    total_assessments += 1

                    precision_label_uri = namespace[precision_label.lower()]  # Convert label to URI

                    # Add assessment results linking to the SKOS concepts
                    self._add_assessment_result(s, AssessmentTypes.COORDINATE_PRECISION, precision_label_uri)

        self.add_to_report('Coordinate Precision Assessments', total_assessments, quality_counts)

    def _get_observation_dates(self):
        # Collect all observation dates
        observation_dates = []
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if BaseUris.check_base_uri(str(s), BaseUris.OBSERVATION):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if date_literal.datatype == XSD.date:
                        observation_dates.append(date_literal.toPython())
        return observation_dates

    def _assess_outlier_and_add_results(self, assessment_type, outlier_condition, type_str):
        namespace = self.label_manager.get_namespace("outlier_date")
        results = {"normal": 0, "outlier": 0}
        # Step 1 : Data gathering
        observation_dates = self._get_observation_dates()

        ordinal_dates = np.array([date.toordinal() for date in observation_dates])

        total_assessments = 0
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if BaseUris.check_base_uri(str(s), BaseUris.OBSERVATION):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if date_literal.datatype == XSD.date:
                        observation_date = date_literal.toPython().toordinal()
                        is_outlier = outlier_condition(observation_date, ordinal_dates)
                        result_label = namespace["outlier"] if is_outlier else namespace["normal"]
                        if is_outlier:
                            results["outlier"] += 1
                        else:
                            results["normal"] += 1

                        total_assessments += 1
                        self._add_assessment_result(s, assessment_type, result_label)

        self.add_to_report(f'Outlier Assessments ({type_str})', total_assessments, results)

    def assess_observation_date_outliers_irq(self):

        def is_outlier(date, dates):
            q1 = np.percentile(dates, 25)
            q3 = np.percentile(dates, 75)
            irq = q3 - q1
            return date < q1 - 1.5 * irq or date > q3 + 1.5 * irq

        self._assess_outlier_and_add_results(AssessmentTypes.OBSERVATION_DATE_OUTLIERS, is_outlier,
                                             "IRQ Outlier Method")

    def assess_observation_date_outliers_lower_upper_thresholds(self):

        observation_dates = self._get_observation_dates()
        min_date = min(observation_dates).toordinal()
        max_date = max(observation_dates).toordinal()
        date_range = max_date - min_date

        def is_outlier(date, dates):
            lower_threshold = min_date + date_range * 0.1
            upper_threshold = max_date - date_range * 0.1
            return date < lower_threshold or date > upper_threshold

        self._assess_outlier_and_add_results(AssessmentTypes.OBSERVATION_DATE_OUTLIERS, is_outlier,
                                             "10% Lower Upper Thresholds Method")

    def assess_point_in_australia_state(self):
        total_assessments = 0
        results_count = {}
        namespace = self.label_manager.get_namespace("australia_state")

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    long, lat = map(float, match.groups())
                    in_australia, state_name = self.geo_checker.is_point_in_australia_state(lat, long)
                    assessment_result = state_name if in_australia else "Outside Australia"
                    if assessment_result not in results_count:
                        # If not found, add the state with an initial count of 0
                        results_count[assessment_result] = 0

                        # Now you can safely increment the count for the state name
                    results_count[assessment_result] += 1

                    total_assessments += 1
                    # Fetch the label URI from the namespace
                    result_label_uri = namespace[assessment_result.replace(' ', '_')]

                    self._add_assessment_result(s, AssessmentTypes.POINT_IN_AUSTRALIA_STATE, result_label_uri)
        self.add_to_report(f'Point in Australia with States', total_assessments, results_count)

    def _add_assessment_result(self, subject, assessment_type, value, assessment_date=None):
        result_bn = BNode()
        self.g.add((subject, DQAF.hasDQAFResult, result_bn))
        self.g.add((result_bn, SOSA.observedProperty, assessment_type))

        # Check if value is a URIRef or needs to be converted to one
        if isinstance(value, URIRef):
            # It's already a URIRef, so we add it directly
            self.g.add((result_bn, SDO.value, value))
        elif isinstance(value, str):
            # Convert the prefixed name back to a URIRef
            prefixed_name = self.__uri_to_prefixed_name(value)
            uri_value = self.__prefixed_name_to_uri(prefixed_name)
            self.g.add((result_bn, SDO.value, uri_value))
        else:
            # If it's neither, treat it as a literal value
            self.g.add((result_bn, SDO.value, Literal(value)))
            # Check if assessment_date is None, and replace it with date.date.now()
        if assessment_date is None:
            assessment_date = datetime.now()
        elif isinstance(assessment_date, datetime.date) and not isinstance(assessment_date, datetime.datetime):
            assessment_date = datetime.datetime.combine(assessment_date, datetime.time.min)

        self.g.add((result_bn, SOSA.resultTime, Literal(assessment_date, datatype=XSD.dateTime)))

    def __prefixed_name_to_uri(self, prefixed_name):
        """
        Converts a prefixed name to a URIRef using the graph's registered namespaces.

        Parameters:
        - prefixed_name: The prefixed name to convert to a URIRef.

        Returns:
        - A URIRef object representing the URI or the original prefixed name if no prefix is found.
        """
        prefix, _, local_part = prefixed_name.partition(':')
        for ns_prefix, namespace in self.g.namespaces():
            if prefix == ns_prefix:
                return URIRef(namespace + local_part)
        return URIRef(prefixed_name)  # Return the original prefixed name as a URIRef if no matching prefix is found

    def __uri_to_prefixed_name(self, uri):
        """
        Convert a URI to its prefixed name using the graph's namespace manager.

        Parameters:
        - uri: The URIRef object to convert to a prefixed name.

        Returns:
        - A string representing the prefixed name if a prefix is found;
          otherwise, the original URI as a string.
        """
        # Ensure uri is of type URIRef
        if not isinstance(uri, URIRef):
            raise ValueError("uri must be an instance of URIRef")

        # Use the namespace manager to find a prefix for the URI's namespace
        ns_manager = NamespaceManager(self.g)
        for prefix, namespace in ns_manager.namespaces():
            if uri.startswith(namespace):
                # Replace the namespace URI with its prefix to form the prefixed name
                return uri.replace(namespace, prefix + ":")

        # If no matching prefix is found, return the original URI as a string
        return str(uri)

    def assess_observation_date_check_format_validation(self):
        total_assessments = 0
        result_counts = {"valid": 0, "invalid": 0}  # Initialize result counts for valid and invalid dates
        namespace = self.label_manager.get_namespace("date_validation")

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if BaseUris.check_base_uri(str(s), BaseUris.OBSERVATION):
                found_date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    date_str = str(date_literal)  # Convert the RDF Literal to a string
                    # Use the method to check the date format and validate
                    date_check = DateChecks(date_str)

                    is_valid_date, detected_format = date_check.check_date_format_and_validate()
                    # Increment counters based on the validation result
                    if is_valid_date:
                        result_counts["valid"] += 1
                    else:
                        result_counts["invalid"] += 1

                    # Prepare a result node (BNode) and add the assessment result to the graph

                    total_assessments += 1

                    # Use  labels for the result
                    result_label = namespace["valid"] if is_valid_date else namespace["invalid"]

                    self._add_assessment_result(s, AssessmentTypes.OBSERVATION_DATE_CHECK_FORMAT_VALIDATION,
                                                result_label)

        self.add_to_report(f'Date Format Validation Assessments', total_assessments, result_counts)

    @staticmethod
    def detect_unusual_numbers(number_str):
        """
        Attempts to detect unusual numbers by looking for repeating patterns in the decimal part.
        This is a heuristic approach and may not accurately detect all repeating patterns.
        """
        # Extract the decimal part of the number
        decimal_part = number_str.split('.')[-1] if '.' in number_str else ''

        # Check for any kind of repeating pattern
        for length in range(1, len(decimal_part)):
            for start in range(len(decimal_part) - length):
                pattern = decimal_part[start:start + length]
                # Check if the pattern repeats in the remainder of the decimal part
                remainder = decimal_part[start + length:]
                if remainder.startswith(pattern):
                    # Found a repeating pattern
                    return 'unusual'
        # No repeating pattern found
        return 'usual'

    def search_scientific_name(self, search_term, similarity_threshold=0.8):
        results = {
            "exact_matches": [],
            "similar_matches": []
        }

        # Iterate through the graph to find scientific names
        for s, p, o in self.g.triples((None, RDF.value, None)):
            if (s, RDF.type, TERN.FeatureOfInterest) in self.g:
                scientific_name = str(o)
                # Check for exact match
                if scientific_name.lower() == search_term.lower():
                    results["exact_matches"].append(scientific_name)
                # Check for similarity
                elif difflib.SequenceMatcher(None, search_term.lower(),
                                             scientific_name.lower()).ratio() > similarity_threshold:
                    results["similar_matches"].append(scientific_name)

        return results

    def collect_location_data(self):
        """
        Collect latitude and longitude values from the RDF graph.

        Returns:
            tuple: A tuple containing two lists: (latitudes, longitudes).
        """
        latitudes = []
        longitudes = []
        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    long, lat = map(float, match.groups())
                    latitudes.append(lat)
                    longitudes.append(long)

        return latitudes, longitudes

    def assess_observation_location_outliers_zscore(self):
        results = {"normal": 0, "outlier": 0}
        namespace = self.label_manager.get_namespace("outlier_point")

        # Collect latitude and longitude values
        latitudes, longitudes = self.collect_location_data()

        # Check if latitudes and longitudes are not empty
        if not latitudes or not longitudes:
            print("No valid geographic points found.")
            return  # Exit the method if no geographic points are collected

        # Ensure there's enough data to calculate statistics
        if len(latitudes) < 2 or len(longitudes) < 2:
            print("Insufficient data for outlier analysis.")
            return  # Consider all points as 'normal' or handle differently

        # Step 2: Calculate mean and standard deviation
        # Ensure you handle NaN values or divisions by zero if applicable
        try:
            lat_mean, lat_std = np.mean(latitudes), np.std(latitudes)
            long_mean, long_std = np.mean(longitudes), np.std(longitudes)
        except RuntimeWarning:
            print("Error calculating statistics.")
            return

        # Step 3: Assess each point for being an outlier
        total_assessments = 0

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    long, lat = map(float, match.groups())
                    lat_z = (lat - lat_mean) / lat_std
                    long_z = (long - long_mean) / long_std
                    is_outlier = abs(lat_z) > 3 or abs(long_z) > 3
                    result_label = "outlier" if is_outlier else "normal"
                    if is_outlier:
                        results["outlier"] += 1
                    else:
                        results["normal"] += 1

                    total_assessments += 1

                    result_uri = namespace[result_label.lower()]
                    self._add_assessment_result(s, AssessmentTypes.OBSERVATION_LOCATION_OUTLIERS, result_uri)

        self.add_to_report(f'Location Outlier Assessments (z-score method)', total_assessments, results)

    def assess_observation_location_outliers_irq(self):
        results = {"normal": 0, "outlier": 0}
        namespace = self.label_manager.get_namespace("outlier_point")

        # Collect latitude and longitude values
        latitudes, longitudes = self.collect_location_data()

        # Check if latitudes and longitudes are not empty
        if not latitudes or not longitudes:
            print("No valid geographic points found.")
            return  # Exit the method if no geographic points are collected

        # Ensure there's enough data to calculate statistics
        if len(latitudes) < 4 or len(longitudes) < 4:
            print("Insufficient data for outlier analysis.")
            return  # Consider all points as 'normal' or handle differently

        # Step 2: Calculate quartiles and IQR
        lat_q1, lat_q3 = np.percentile(latitudes, [25, 75])
        long_q1, long_q3 = np.percentile(longitudes, [25, 75])
        lat_iqr = lat_q3 - lat_q1
        long_iqr = long_q3 - long_q1

        # Step 3: Assess each point for being an outlier
        total_assessments = 0

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    long, lat = map(float, match.groups())
                    lat_outlier = lat < lat_q1 - 1.5 * lat_iqr or lat > lat_q3 + 1.5 * lat_iqr
                    long_outlier = long < long_q1 - 1.5 * long_iqr or long > long_q3 + 1.5 * long_iqr
                    is_outlier = lat_outlier or long_outlier
                    result_label = "outlier" if is_outlier else "normal"
                    if is_outlier:
                        results["outlier"] += 1
                    else:
                        results["normal"] += 1

                    total_assessments += 1
                    # Assuming namespace maps labels to their URIs
                    result_uri = namespace[result_label.lower()]
                    self._add_assessment_result(s, AssessmentTypes.OBSERVATION_LOCATION_OUTLIERS, result_uri)

        self.add_to_report(f'Location Outlier Assessments (IRQ method)', total_assessments, results)

    def add_to_report(self, assessment_name, total_assessments, result_counts):
        if self.report_file:
            print(f'', file=self.report_file)
            print(f'- {assessment_name}: {total_assessments}', file=self.report_file)
            for quality, count in result_counts.items():
                print(f'\t{quality}: {count}', file=self.report_file)

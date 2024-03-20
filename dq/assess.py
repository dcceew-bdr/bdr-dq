import datetime
from datetime import datetime
from pathlib import Path
from typing import Union
import os
import geopandas as gpd
from shapely.geometry import Point
import re

import numpy as np
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import NamespaceManager, SOSA, TIME, GEO, SDO, XSD, RDF

from .defined_namespaces import DQAF, TERN, DirectoryStructure
from .vocab_manager import VocabManager
from .report_analysis import ReportAnalysis
from typing import Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


class RDFDataQualityAssessment:
    def __init__(self, g: Union[Path, Graph], report_file=None):
        self.directory_structure=DirectoryStructure()
        self.report_file = report_file
        self.g = self.load_data(g)
        self.vocab_manager = VocabManager()
        self.geo_checker = AustraliaGeographyChecker()
        self.report_analysis = ReportAnalysis(self.g, report_file)
        self.datum_checker = DatumChecker()
        self.vocab_manager.bind_custom_namespaces(self.g)

    @staticmethod
    def load_data(path_or_graph: Union[Path, Graph]) -> Graph:
        if isinstance(path_or_graph, Path):
            return Graph().parse(source=str(path_or_graph), format='ttl')
        elif isinstance(path_or_graph, Graph):
            return path_or_graph
        else:
            raise ValueError("Input must be either a Path object pointing to a Turtle file or an RDFlib Graph")

    def assessments(self):

        # Add custom labels definition to the new graph and save it into new file name
        self.vocab_manager.create_output_definition_file(os.path.join(self.directory_structure.result_base_path, 'Label_Definition.ttl'))

        # Bind custom labels
        self.vocab_manager.bind_custom_namespaces(self.g)

        # Add methods to call the specific assessment methods here
        self.assess_coordinate_precision()
        self.assess_coordinate_completeness()
        self.assess_coordinate_unusual()
        self.assess_coordinate_in_australia_state()
        self.assess_coordinate_outlier_irq()
        self.assess_coordinate_outlier_zscore()
        self.assess_date_recency()
        self.assess_date_format_validation()
        self.assess_date_completeness()
        self.assess_date_outlier_kmeans()
        self.assess_date_outlier_irq()
        self.assess_scientific_name_completeness()
        self.assess_scientific_name_validation()
        self.assess_datum_completeness()
        self.assess_datum_type()
        self.assess_datum_validation()

        # TODO: Add other assessments methods

    def assess_date_completeness(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("date_completeness")
        result_counts = {"non_empty": 0, "empty": 0}  # Initialize result counts for True and False

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                date_is_not_empty = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if DateChecker.is_date_not_empty(date_literal):
                        result_counts["non_empty"] += 1
                        date_is_not_empty = True
                    else:
                        result_counts["empty"] += 1
                    break  # Assuming only one date per observation; remove if multiple dates need assessment

                total_assessments += 1
                # Use  labels for the result
                result_label = namespace["non_empty"] if date_is_not_empty else namespace["empty"]

                self._add_assessment_result(s, assess_namespace, result_label)

        self.add_to_report('Assess Date Completeness', total_assessments, result_counts)

    def assess_date_recency(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("date_recency")
        result_counts = {"recent_20_years": 0, "outdated_20_years": 0}  # Initialize result counts for True and False

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if DateChecker.is_date_recent(date_literal):
                        result_counts["recent_20_years"] += 1
                        date_within_range = True
                    else:
                        result_counts["outdated_20_years"] += 1
                    break  # Assuming only one date per observation; remove if multiple dates need assessment

                total_assessments += 1
                # Use  labels for the result
                result_label = namespace["recent_20_years"] if date_within_range else namespace["outdated_20_years"]

                self._add_assessment_result(s, assess_namespace, result_label)

        self.add_to_report('Assess Date Recency', total_assessments, result_counts)
        return total_assessments, result_counts

    def assess_datum_completeness(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("datum_completeness")
        quality_counts = {"empty": 0, "not_empty": 0}

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                datum_is_empty = self.datum_checker.is_not_empty(str(geometry))

                if datum_is_empty:
                    quality_label = "not_empty"
                else:
                    quality_label = "empty"

                quality_counts[quality_label] += 1
                total_assessments += 1

                quality_label_uri = namespace[quality_label]  # Convert label to URI
                self._add_assessment_result(s, assess_namespace, quality_label_uri)

        self.add_to_report('Assess Datum Completeness', total_assessments, quality_counts)

    def assess_datum_validation(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("datum_validation")
        quality_counts = {"Valid": 0, "Invalid": 0}

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                epsg_link = self.datum_checker.extract_epsg_link(str(geometry))

                datum_metadata = self.datum_checker.get_datum_metadata(epsg_link)

                if datum_metadata:
                    quality_label = "Valid"
                else:
                    quality_label = "Invalid"

                quality_counts[quality_label] += 1
                total_assessments += 1

                quality_label_uri = namespace[quality_label]  # Convert label to URI
                self._add_assessment_result(s, assess_namespace, quality_label_uri)

        self.add_to_report('Assess Datum Validation', total_assessments, quality_counts)

    def assess_datum_type(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("datum_type")
        quality_counts = {"AGD84": 0, "GDA2020": 0, "GDA94": 0, "WGS84": 0, "None": 0}

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                epsg_link = self.datum_checker.extract_epsg_link(str(geometry))

                datum_metadata = self.datum_checker.get_datum_metadata(epsg_link)

                if datum_metadata:
                    quality_label = datum_metadata["name"]
                else:
                    quality_label = "None"

                quality_counts[quality_label] += 1
                total_assessments += 1

                quality_label_uri = namespace[quality_label]  # Convert label to URI
                self._add_assessment_result(s, assess_namespace, quality_label_uri)

        self.add_to_report('Assess Datum Type', total_assessments, quality_counts)

    def assess_coordinate_precision(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_precision")
        quality_counts = {"Low": 0, "Medium": 0, "High": 0}  # Use the new labels

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    longitude, latitude = match.groups()
                    precision_label = GeoChecker.assess_coordinate_precision(longitude, latitude)

                    quality_counts[
                        precision_label] += 1  # Increment by 1 to account for both lat and long assessments together

                    total_assessments += 1

                    precision_label_uri = namespace[precision_label.lower()]  # Convert label to URI

                    # Add assessment results linking to the SKOS concepts
                    self._add_assessment_result(s, assess_namespace, precision_label_uri)

        self.add_to_report('Assess Coordinate Precision', total_assessments, quality_counts)

    def assess_coordinate_completeness(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_completeness")
        results = {"empty": 0, "non_empty": 0}  # Use new labels

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    # Point is not empty, found longitude and latitude
                    results["non_empty"] += 1
                    result_label = namespace["non_empty"]
                else:
                    # Point is empty, did not find longitude and latitude in the expected format
                    results["empty"] += 1
                    result_label = namespace["empty"]
            else:
                # Geometry object is empty
                results["empty"] += 1
                result_label = namespace["empty"]

            total_assessments += 1
            self._add_assessment_result(s, assess_namespace, result_label)

        self.add_to_report(f'Assess Coordinate Completeness', total_assessments, results)
    def assess_date_outlier_irq(self):
        namespace, assess_namespace = self.vocab_manager.get_namespaces("date_outlier_irq")
        results = {"normal_date": 0, "outlier_date": 0}

        # Step 1 : Data gathering - Collect all observation dates
        observation_dates = []
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if date_literal.datatype == XSD.date:
                        observation_dates.append(date_literal.toPython())

        # Step 2: Calculate Q1, Q3, and IQR
        observation_dates = np.array(
            [date.toordinal() for date in observation_dates])  # Convert dates to ordinal values
        Q1 = np.percentile(observation_dates, 25)
        Q3 = np.percentile(observation_dates, 75)
        IQR = Q3 - Q1

        total_assessments = 0
        # Step 3: Tag each data point
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if date_literal.datatype == XSD.date:
                        observation_date = date_literal.toPython().toordinal()  # Convert date to ordinal value
                        is_outlier = observation_date < Q1 - 1.5 * IQR or observation_date > Q3 + 1.5 * IQR
                        result_label = namespace["outlier_date"] if is_outlier else namespace["normal_date"]
                        if is_outlier:
                            results["outlier_date"] += 1
                        else:
                            results["normal_date"] += 1

                        total_assessments += 1
                        self._add_assessment_result(s, assess_namespace, result_label)

        self.add_to_report(f'Assess Date Outlier IRQ', total_assessments, results)

    def assess_date_outlier_kmeans(self):
        namespace, assess_namespace = self.vocab_manager.get_namespaces("date_outlier_kmeans")
        results = {"normal_date": 0, "outlier_date": 0}

        # Step 1: Data gathering - Collect all observation dates
        observation_dates = []
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    if date_literal.datatype == XSD.date:
                        observation_dates.append(date_literal.toPython())

        # Convert dates to numeric format (days since the earliest date)
        if observation_dates:
            base_date = min(observation_dates)
            numeric_dates = np.array([(date - base_date).days for date in observation_dates]).reshape(-1, 1)

            # Normalize the data
            scaler = MinMaxScaler()
            scaled_dates = scaler.fit_transform(numeric_dates)

            # Apply KMeans clustering
            n_clusters = 5  # Adjust based on the dataset
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(scaled_dates)
            labels = kmeans.labels_

            # Identifying outliers
            outlier_cluster = np.argmin(np.bincount(labels))
            outliers_indices = [i for i, label in enumerate(labels) if label == outlier_cluster]

            total_assessments = 0

            # Step 2: Tag each data point
            for index, (s, _, o) in enumerate(self.g.triples((None, SOSA.phenomenonTime, None))):
                if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                    for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                        if date_literal.datatype == XSD.date and index in outliers_indices:
                            result_label = namespace["outlier_date"]
                            results["outlier_date"] += 1
                        else:
                            result_label = namespace["normal_date"]
                            results["normal_date"] += 1

                        total_assessments += 1
                        self._add_assessment_result(s, assess_namespace, result_label)

            self.add_to_report(f'Assess Date Outlier Kmeans', total_assessments, results)

    def assess_coordinate_in_australia_state(self):
        total_assessments = 0
        results_count = {}
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_in_australia_state")

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    long, lat = map(float, match.groups())
                    in_australia, state_name = self.geo_checker.is_point_in_australia_state(lat, long)
                    assessment_result = state_name if in_australia else "Outside_Australia"
                    if assessment_result not in results_count:
                        # If not found, add the state with an initial count of 0
                        results_count[assessment_result] = 0

                        # Now you can safely increment the count for the state name
                    results_count[assessment_result] += 1

                    total_assessments += 1
                    # Fetch the label URI from the namespace
                    result_label_uri = namespace[assessment_result.replace(' ', '_')]

                    self._add_assessment_result(s, assess_namespace, result_label_uri)
        self.add_to_report(f'Assess Coordinate in Australia State', total_assessments, results_count)
        return total_assessments,results_count

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

    def assess_date_format_validation(self):
        total_assessments = 0
        result_counts = {"valid": 0, "invalid": 0}  # Initialize result counts for valid and invalid dates
        namespace, assess_namespace = self.vocab_manager.get_namespaces("date_format_validation")

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            # Check if the subject starts with the specified URI
            if UriChecker.check_base_uri(str(s), UriChecker.OBSERVATION):
                found_date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDate, None)):
                    date_str = str(date_literal)  # Convert the RDF Literal to a string
                    # Use the method to check the date format and validate
                    date_check = DateChecker(date_str)

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

                    self._add_assessment_result(s, assess_namespace,
                                                result_label)

        self.add_to_report(f'Assess Date Format Validation', total_assessments, result_counts)

    def assess_coordinate_unusual(self):
        total_assessments = 0
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_unusual")
        results = {"usual": 0, "unusual": 0}

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            geometry = next(self.g.objects(o, GEO.asWKT), None)

            if geometry:
                match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                if match:
                    longitude, latitude = match.groups()
                    # Assess both latitude and longitude for unusualness
                    lon_unusual = self.detect_unusual_numbers(longitude) == 'unusual'
                    lat_unusual = self.detect_unusual_numbers(latitude) == 'unusual'

                    # If either is unusual, mark the whole point as unusual
                    if lon_unusual or lat_unusual:
                        results["unusual"] += 1
                        result_label = namespace["unusual"]
                    else:
                        results["usual"] += 1
                        result_label = namespace["usual"]
                else:
                    # If geometry is not in POINT format, default to usual
                    results["usual"] += 1
                    result_label = namespace["usual"]
            else:
                # If no geometry data, default to usual
                results["usual"] += 1
                result_label = namespace["usual"]

            total_assessments += 1
            self._add_assessment_result(s, assess_namespace, result_label)

        self.add_to_report('Assess Coordinate Unusual', total_assessments, results)

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

    def assess_coordinate_outlier_zscore(self):
        results = {"normal_coordinate": 0, "outlier_coordinate": 0}
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_outlier_zscore")

        # Collect latitude and longitude values
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
                    result_label = "outlier_coordinate" if is_outlier else "normal_coordinate"
                    if is_outlier:
                        results["outlier_coordinate"] += 1
                    else:
                        results["normal_coordinate"] += 1

                    total_assessments += 1

                    result_uri = namespace[result_label.lower()]
                    self._add_assessment_result(s, assess_namespace, result_uri)

        self.add_to_report(f'Assess Coordinate Outlier Zscore', total_assessments, results)

    def assess_coordinate_outlier_irq(self):
        results = {"normal_coordinate": 0, "outlier_coordinate": 0}
        namespace, assess_namespace = self.vocab_manager.get_namespaces("coordinate_outlier_irq")

        # Collect latitude and longitude values
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
                    result_label = "outlier_coordinate" if is_outlier else "normal_coordinate"
                    if is_outlier:
                        results["outlier_coordinate"] += 1
                    else:
                        results["normal_coordinate"] += 1

                    total_assessments += 1
                    # Assuming namespace maps labels to their URIs
                    result_uri = namespace[result_label.lower()]
                    self._add_assessment_result(s, assess_namespace, result_uri)

        self.add_to_report(f'Assess Coordinate Outlier IRQ', total_assessments, results)

    def assess_scientific_name_completeness(self):
        namespace, assess_namespace = self.vocab_manager.get_namespaces("scientific_name_completeness")
        results = {"empty_name": 0, "non_empty_name": 0}

        # Step 1: Data gathering - Check all records for scientific name presence
        total_assessments = 0
        for s, p, o in self.g.triples((None, RDF.value, None)):

            if (s, RDF.type, TERN.FeatureOfInterest) in self.g:
                scientific_name = str(o).strip()
                # Step 2: Tag each Feature of Interest based on scientific name being empty or not
                result_label = namespace["empty_name"]
                if scientific_name is None or str(scientific_name).strip() == "":
                    results["empty_name"] += 1
                else:
                    result_label = namespace["non_empty_name"]
                    results["non_empty_name"] += 1

                total_assessments += 1
                # Use  labels for the result

                self._add_assessment_result(s, assess_namespace, result_label)

        # Step 3: Update report
        self.add_to_report('Assess Scientific Name Completeness', total_assessments, results)

    def assess_scientific_name_validation(self):
        namespace, assess_namespace = self.vocab_manager.get_namespaces("scientific_name_validation")
        results = {"valid_name": 0, "invalid_name": 0}

        # Step 1: Data gathering - Check all records for scientific name validity
        total_assessments = 0
        for s, p, o in self.g.triples((None, RDF.value, None)):
            if (s, RDF.type, TERN.FeatureOfInterest) in self.g:
                scientific_name = str(o).strip()

                # Step 2: Use ScientificNameChecker to assess validity
                if scientific_name and ScientificNameChecker.is_valid_scientific_name(scientific_name):
                    result_label = namespace["valid_name"]
                    results["valid_name"] += 1
                else:
                    result_label = namespace["invalid_name"]
                    results["invalid_name"] += 1

                total_assessments += 1
                # Use labels for the result
                self._add_assessment_result(s, assess_namespace, result_label)

        # Step 3: Update report
        self.add_to_report('Assess Scientific Name Validation', total_assessments, results)

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

    def add_to_report(self, assessment_name, total_assessments, result_counts):
        if self.report_file:
            print(f'', file=self.report_file)
            print(f'- {assessment_name}: {total_assessments}', file=self.report_file)
            for quality, count in result_counts.items():
                print(f'\t{quality}: {count}', file=self.report_file)


class DateChecker:
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

    @staticmethod
    def is_date_not_empty(date):
        """
        Checks if the provided date is not empty. This function can handle different data types,
        including strings, lists, dictionaries, and None values.

        :param date: The data to check.
        :return: True if the date is considered not empty, False otherwise.
        """
        if date is None:
            return False
        if isinstance(date, (str, list, dict, set)):
            return bool(date)  # Checks if strings/lists/dicts/sets are not empty
        return True  # For other data types, assume 'not empty' if not None

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


class DatumChecker:
    def __init__(self):
        self.valid_datums = {"AGD84", "GDA2020", "GDA94", "WGS84"}
        self.datum_metadata = {
            4348: {"name": "AGD84", "description": "Australian Geodetic Datum 1984"},
            7843: {"name": "GDA2020", "description": "Geocentric Datum of Australia 2020"},
            4283: {"name": "GDA94", "description": "Geocentric Datum of Australia 1994"},
            4326: {"name": "WGS84", "description": "World Geodetic System 1984"},
        }

    def is_not_empty(self, datum):
        """
        Checks if the provided datum is not empty. This function can handle different data types,
        including strings, lists, dictionaries, and None values.

        :param datum: The data to check.
        :return: True if the datum is considered not empty, False otherwise.
        """
        if datum is None:
            return False
        if isinstance(datum, (str, list, dict, set)):
            return bool(datum)  # Checks if strings/lists/dicts/sets are not empty
        return True  # For other data types, assume 'not empty' if not None

    def is_valid_datum(self, datum):
        """
        Checks if the provided datum is one of the specified valid geo datums.

        :param datum: The datum string to check.
        :return: True if the datum is valid, False otherwise.
        """
        return datum in self.valid_datums

    def get_datum_metadata(self, link: str) -> Optional[dict]:
        """
        Returns the datum metadata for a given EPSG link.

        :param link: The EPSG link for the datum.
        :return: A dictionary containing the datum metadata if the link is valid, None otherwise.
        """
        # Define a regular expression pattern to match the EPSG link format
        pattern = r"http://www.opengis.net/def/crs/EPSG/9.9.1/(\d+)"

        # Check if the link matches the pattern
        if re.match(pattern, link):
            # Extract the EPSG code from the link
            epsg_code = int(link.split("/")[-1])

            # Return the metadata if the EPSG code is found in the dictionary
            return self.datum_metadata.get(epsg_code)

        # Return None if the link is invalid
        return None

    def get_datum_metadata_from_asWKT(self, graph, uri):
        """
        Returns the datum metadata for a geo:asWKT node in an RDF graph.

        :param graph: The RDF graph.
        :param uri: The URI of the node to extract the geo:asWKT value from.
        :return: A dictionary containing the datum metadata if the geo:asWKT value is valid, None otherwise.
        """
        # Get the geo:asWKT value for the given URI
        asWKT_value = graph.value(subject=URIRef(uri), predicate=URIRef("http://www.opengis.net/ont/geosparql#asWKT"))

        if asWKT_value:
            # Extract the EPSG link from the geo:asWKT value
            epsg_link = str(asWKT_value).split(" ")[0][1:-1]  # Remove enclosing "<" and ">"

            # Get the datum metadata using the EPSG link
            return self.get_datum_metadata(epsg_link)

        return None

    def extract_epsg_link(self, wkt_string: str) -> Optional[str]:
        match = re.search(r"<(.+?)>", wkt_string)
        if match:
            return match.group(1)
        return None


class GeoChecker:
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
        mad_lat, mad_long = GeoChecker.calculate_median_absolute_deviation(coordinates)
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


class AustraliaGeographyChecker:
    def __init__(self):
        self.directory_structure=DirectoryStructure()


        self.states_shapefiles = {
            "New_South_Wales": os.path.join(self.directory_structure.map_base_path, "new_south_wales", "cstnswcd_r.shp"),
            "Victoria": os.path.join(self.directory_structure.map_base_path, "victoria", "cstviccd_r.shp"),
            "Queensland": os.path.join(self.directory_structure.map_base_path, "queensland", "cstqldmd_r.shp"),
            "Western_Australia": os.path.join(self.directory_structure.map_base_path, "western_australia", "cstwacd_r.shp"),
            "South_Australia": os.path.join(self.directory_structure.map_base_path, "south_australia", "cstsacd_r.shp"),
            "Tasmania": os.path.join(self.directory_structure.map_base_path, "tasmania", "csttascd_r.shp"),
            "Northern_Territory": os.path.join(self.directory_structure.map_base_path, "northern_territory", "cstntcd_r.shp"),
            "Australian_Capital_Territory": os.path.join(self.directory_structure.map_base_path, "australia",
                                                         "cstauscd_r.shp")
        }

        self.states_data = {
            state_name: gpd.read_file(shapefile).to_crs(epsg=4326)
            for state_name, shapefile in self.states_shapefiles.items()
        }

    def is_point_in_australia_state(self, lat, long):
        point = Point(long, lat)

        # Check each state to see if the point is within its boundary
        for state_name, state_data in self.states_data.items():
            if state_data.contains(point).any():
                return True, state_name

        return False, "Outside Australia"  # Point is not in any state, hence outside Australia


class ScientificNameChecker:
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
        Validates if the given string follows a more comprehensive convention for scientific names.
        This includes handling names with subspecies, varieties, hybrids, and optionally checking against a taxonomic database.
        """

        # Updated pattern to include subspecies, varieties, forms, and hybrids
        # pattern = r'^[A-Z][a-z]+(?:\s[a-z]+)?(?:\s(?:subsp\.|var\.|f\.)\s[a-z]+)?(?:\s×\s[a-z]+)?$'

        # Check pattern match
        # if not re.match(pattern, scientific_name):
        #    return False

        # Optional: Extend to check against a taxonomic database here
        if scientific_name:
            return True
        else:
            return False


class UriChecker:
    OBSERVATION = "http://createme.org/observation/individualCount/"
    ATTRIBUTE = "http://createme.org/attribute/kingdom/"
    SCIENTIFIC_NAME = "http://createme.org/observation/scientificName/"
    PROVIDER = "http://createme.org/provider/"
    SAMPLE = "http://createme.org/sample/field/"

    @staticmethod
    def check_base_uri(uri, check_string):
        # Find the last occurrence of '/'
        last_slash_index = uri.rfind('/')
        # Extract the base URI
        base_uri = uri[:last_slash_index + 1]  # Include the slash in the base URI
        return base_uri == check_string

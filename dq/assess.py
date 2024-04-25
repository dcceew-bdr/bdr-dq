import datetime
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from typing import Union

import geopandas as gpd
import numpy as np
import pandas as pd
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import NamespaceManager, SOSA, TIME, GEO, SDO, XSD, RDF, RDFS
from shapely.geometry import Point
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score

from .defined_namespaces import DQAF, TERN, DirectoryStructure
from .report_analysis import ReportAnalysis
from .usecase_manager import UseCaseManager
from .vocab_manager import VocabManager


class RDFDataQualityAssessment:
    def __init__(self, g: Union[Path, Graph], report_file=None):
        self.directory_structure = DirectoryStructure()
        self.report_file = report_file
        self.g = self.load_data(g)
        self.vocab_manager = VocabManager()
        self.geo_checker = AustraliaGeographyChecker()
        self.report_analysis = ReportAnalysis(self.g, report_file)
        self.datum_checker = DatumChecker()
        self.vocab_manager.bind_custom_namespaces(self.g)
        columns = ['observation_id'] + self.vocab_manager.get_all_labels()
        self.result_matrix_df = pd.DataFrame(columns=columns)

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
        self.vocab_manager.create_output_definition_file(
            os.path.join(self.directory_structure.result_base_path, 'vocab_Definition.ttl'))

        self.vocab_manager.bind_custom_namespaces(self.g)

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

    def assess_date_completeness(self):
        assessment_name = "date_completeness"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):
                date_is_not_empty = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    if DateChecker.is_date_not_empty(date_literal):
                        date_is_not_empty = True
                    break  # Assuming only one date per observation; remove if multiple dates need assessment

                result_label = "non_empty" if date_is_not_empty else "empty"
                result_counts[result_label] += 1
                total_assessments += 1

                self._add_assessment_result(s, assess_namespace, namespace[result_label])
                self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Date Completeness', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_date_recency(self):
        assessment_name = "date_recency"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):

                date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    if DateChecker.is_date_recent(date_literal):
                        date_within_range = True
                    break  # Assuming only one date per observation; remove if multiple dates need assessment

                result_label = "recent_20_years" if date_within_range else "outdated_20_years"
                result_counts[result_label] += 1
                total_assessments += 1

                self._add_assessment_result(s, assess_namespace, namespace[result_label])
                self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Date Recency', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_datum_completeness(self):
        assessment_name = "datum_completeness"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    datum_is_empty = self.datum_checker.is_not_empty(str(geometry))
                    result_label = "not_empty" if datum_is_empty else "empty"

                    result_counts[result_label] += 1
                    total_assessments += 1

                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Datum Completeness', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_datum_validation(self):
        assessment_name = "datum_validation"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    epsg_link = self.datum_checker.extract_epsg_link(str(geometry))
                    datum_metadata = self.datum_checker.get_datum_metadata(epsg_link)
                    result_label = "valid" if datum_metadata else "invalid"

                    result_counts[result_label] += 1
                    total_assessments += 1
                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Datum Validation', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_datum_type(self):
        assessment_name = "datum_type"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    epsg_link = self.datum_checker.extract_epsg_link(str(geometry))
                    datum_metadata = self.datum_checker.get_datum_metadata(epsg_link)

                    result_label = datum_metadata["name"] if datum_metadata else "None"

                    result_counts[result_label] += 1
                    total_assessments += 1

                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Datum Type', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def has_relevant_comment(self, s, rel_comment):
        found_relevant_comment = False
        for _, _, comment in self.g.triples((s, RDFS.comment, None)):
            if rel_comment in str(comment):
                found_relevant_comment = True
                break
        return found_relevant_comment

    def assess_coordinate_precision(self):
        assessment_name = "coordinate_precision"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    result_label = GeoChecker.extract_and_assess_coordinate_precision(geometry)

                    if result_label:
                        result_counts[result_label] += 1
                        total_assessments += 1
                        self._add_assessment_result(s, assess_namespace, namespace[result_label])
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Coordinate Precision', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_coordinate_completeness(self):
        assessment_name = "coordinate_completeness"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    result_label = GeoChecker.check_geometry_completeness(geometry)
                    result_counts[result_label] += 1

                    total_assessments += 1
                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Coordinate Completeness', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_date_outlier_irq(self):
        assessment_name = "date_outlier_irq"
        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        observation_dates = []
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):

                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    if date_literal.datatype in [XSD.dateTime, XSD.dateTimeStamp]:
                        datetime_obj = datetime.fromisoformat(date_literal)
                        observation_dates.append(datetime_obj.date())

        observation_dates = np.array(
            [date.toordinal() for date in observation_dates])
        Q1 = np.percentile(observation_dates, 25)
        Q3 = np.percentile(observation_dates, 75)
        IQR = Q3 - Q1

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    if date_literal.datatype in [XSD.dateTime, XSD.dateTimeStamp]:
                        datetime_obj = datetime.fromisoformat(date_literal)
                        observation_date = datetime_obj.date().toordinal()  # Convert date to ordinal value
                        is_outlier = observation_date < Q1 - 1.5 * IQR or observation_date > Q3 + 1.5 * IQR
                        result_label = "outlier_date" if is_outlier else "normal_date"
                        result_counts[result_label] += 1

                        total_assessments += 1
                        self._add_assessment_result(s, assess_namespace, namespace[result_label])
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Date Outlier IRQ', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_date_outlier_kmeans(self):
        assessment_name = "date_outlier_kmeans"
        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        observation_dates = []
        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    if date_literal.datatype in [XSD.dateTime, XSD.dateTimeStamp]:
                        datetime_obj = datetime.fromisoformat(date_literal)
                        observation_dates.append(datetime_obj.date())

        if observation_dates:
            base_date = min(observation_dates)
            numeric_dates = np.array([(date - base_date).days for date in observation_dates]).reshape(-1, 1)

            scaler = MinMaxScaler()
            scaled_dates = scaler.fit_transform(numeric_dates)

            best_k = 2
            best_score = -1

            if len(np.unique(scaled_dates)) > 1:
                for k in range(2, min(len(scaled_dates), 10)):
                    kmeans = KMeans(n_clusters=k, random_state=42)
                    labels = kmeans.fit_predict(scaled_dates)
                    if len(set(labels)) > 1:
                        score = silhouette_score(scaled_dates, labels)
                        if score > best_score:
                            best_k = k
                            best_score = score
                    else:
                        break  # Break the loop if only one cluster has been formed

            print('Best K for kmeans as the number of clusters is ', best_k)
            kmeans = KMeans(n_clusters=best_k, random_state=42)
            kmeans.fit(scaled_dates)
            labels = kmeans.labels_

            outlier_cluster = np.argmin(np.bincount(labels))
            outliers_indices = [i for i, label in enumerate(labels) if label == outlier_cluster]

            for index, (s, _, o) in enumerate(self.g.triples((None, SOSA.phenomenonTime, None))):
                if self.has_relevant_comment(s, "NSL name match Observation"):
                    for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                        if date_literal.datatype == XSD.dateTimeStamp and index in outliers_indices:
                            result_label = "outlier_date"
                        else:
                            result_label = "normal_date"

                        result_counts[result_label] += 1
                        total_assessments += 1
                        self._add_assessment_result(s, assess_namespace, namespace[result_label])
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

            self.add_to_report(f'Assess Date Outlier Kmeans', total_assessments, result_counts)
            return assessment_name, total_assessments, result_counts

    def assess_coordinate_in_australia_state(self):
        assessment_name = "coordinate_in_australia_state"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                    if match:
                        long, lat = map(float, match.groups())
                        in_australia, state_name = self.geo_checker.is_point_in_australia_state(lat, long)
                        result_label = state_name if in_australia else "Outside_Australia"

                        result_counts[result_label] += 1

                        total_assessments += 1
                        result_label_uri = namespace[result_label.replace(' ', '_')]

                        self._add_assessment_result(s, assess_namespace, result_label_uri)
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Coordinate in Australia State', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def __prefixed_name_to_uri(self, prefixed_name):
        prefix, _, local_part = prefixed_name.partition(':')
        for ns_prefix, namespace in self.g.namespaces():
            if prefix == ns_prefix:
                return URIRef(namespace + local_part)
        return URIRef(prefixed_name)  # Return the original prefixed name as a URIRef if no matching prefix is found

    def __uri_to_prefixed_name(self, uri):
        if not isinstance(uri, URIRef):
            raise ValueError("uri must be an instance of URIRef")

        ns_manager = NamespaceManager(self.g)
        for prefix, namespace in ns_manager.namespaces():
            if uri.startswith(namespace):
                # Replace the namespace URI with its prefix to form the prefixed name
                return uri.replace(namespace, prefix + ":")

        return str(uri)

    def assess_date_format_validation(self):
        assessment_name = "date_format_validation"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, SOSA.phenomenonTime, None)):
            if self.has_relevant_comment(s, "NSL name match Observation"):
                found_date_within_range = False
                for _, _, date_literal in self.g.triples((o, TIME.inXSDDateTimeStamp, None)):
                    date_str = str(date_literal)
                    date_check = DateChecker(date_str[:10])
                    is_valid_date, detected_format = date_check.check_date_format_and_validate()
                    result_label = "valid" if is_valid_date else "invalid"
                    result_counts[result_label] += 1
                    total_assessments += 1

                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Date Format Validation', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_coordinate_unusual(self):
        assessment_name = "coordinate_unusual"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    result_label = GeoChecker.unusual_check(geometry)

                    result_counts[result_label] += 1
                    total_assessments += 1
                    self._add_assessment_result(s, assess_namespace, namespace[result_label])
                    self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Coordinate Unusual', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    @staticmethod
    def detect_unusual_numbers(number_str):
        """
        Attempts to detect unusual numbers by looking for repeating patterns in the decimal part.
        This is a heuristic approach and may not accurately detect all repeating patterns.
        """
        decimal_part = number_str.split('.')[-1] if '.' in number_str else ''
        for length in range(1, len(decimal_part)):
            for start in range(len(decimal_part) - length):
                pattern = decimal_part[start:start + length]
                remainder = decimal_part[start + length:]
                if remainder.startswith(pattern):
                    return 'unusual'
        return 'usual'

    def assess_coordinate_outlier_zscore(self):
        assessment_name = "coordinate_outlier_zscore"
        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        latitudes = []
        longitudes = []
        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                    if match:
                        long, lat = map(float, match.groups())
                        latitudes.append(lat)
                        longitudes.append(long)

        if not latitudes or not longitudes:
            print("No valid geographic points found.")
            return

        if len(latitudes) < 2 or len(longitudes) < 2:
            print("Insufficient data for outlier analysis.")
            return

        try:
            lat_mean, lat_std = np.mean(latitudes), np.std(latitudes)
            long_mean, long_std = np.mean(longitudes), np.std(longitudes)
        except RuntimeWarning:
            print("Error calculating statistics.")
            return

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                    if match:
                        long, lat = map(float, match.groups())
                        lat_z = (lat - lat_mean) / lat_std
                        long_z = (long - long_mean) / long_std
                        is_outlier = abs(lat_z) > 3 or abs(long_z) > 3
                        result_label = "outlier_coordinate" if is_outlier else "normal_coordinate"

                        total_assessments += 1
                        result_counts[result_label] += 1

                        self._add_assessment_result(s, assess_namespace, namespace[result_label.lower()])
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Coordinate Outlier Zscore', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_coordinate_outlier_irq(self):
        assessment_name = "coordinate_outlier_irq"

        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        latitudes = []
        longitudes = []
        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                    if match:
                        long, lat = map(float, match.groups())
                        latitudes.append(lat)
                        longitudes.append(long)

        if not latitudes or not longitudes:
            print("No valid geographic points found.")
            return

        if len(latitudes) < 4 or len(longitudes) < 4:
            print("Insufficient data for outlier analysis.")
            return

        lat_q1, lat_q3 = np.percentile(latitudes, [25, 75])
        long_q1, long_q3 = np.percentile(longitudes, [25, 75])
        lat_iqr = lat_q3 - lat_q1
        long_iqr = long_q3 - long_q1

        for s, _, o in self.g.triples((None, GEO.hasGeometry, None)):
            if self.has_relevant_comment(s, "field-sampling"):
                geometry = next(self.g.objects(o, GEO.asWKT), None)

                if geometry:
                    match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                    if match:
                        long, lat = map(float, match.groups())
                        lat_outlier = lat < lat_q1 - 1.5 * lat_iqr or lat > lat_q3 + 1.5 * lat_iqr
                        long_outlier = long < long_q1 - 1.5 * long_iqr or long > long_q3 + 1.5 * long_iqr
                        is_outlier = lat_outlier or long_outlier
                        result_label = "outlier_coordinate" if is_outlier else "normal_coordinate"

                        total_assessments += 1
                        result_counts[result_label] += 1

                        self._add_assessment_result(s, assess_namespace, namespace[result_label.lower()])
                        self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report(f'Assess Coordinate Outlier IRQ', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_scientific_name_completeness(self):
        assessment_name = "scientific_name_completeness"
        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, p, o in self.g.triples((None, RDF.value, None)):

            if (s, RDF.type, TERN.FeatureOfInterest) in self.g:
                scientific_name = str(o).strip()

                if scientific_name is None or str(scientific_name).strip() == "":
                    result_label = "empty_name"
                else:
                    result_label = "non_empty_name"

                result_counts[result_label] += 1
                total_assessments += 1

                self._add_assessment_result(s, assess_namespace, namespace[result_label])
                self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Scientific Name Completeness', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def assess_scientific_name_validation(self):
        assessment_name = "scientific_name_validation"
        namespace, assess_namespace, result_counts, total_assessments = self.vocab_manager.init_assessment(
            assessment_name)

        for s, p, o in self.g.triples((None, RDF.value, None)):
            if (s, RDF.type, TERN.FeatureOfInterest) in self.g:
                scientific_name = str(o).strip()

                if scientific_name and ScientificNameChecker.is_valid_scientific_name(scientific_name):
                    result_label = "valid_name"
                else:
                    result_label = "invalid_name"

                total_assessments += 1
                result_counts[result_label] += 1
                self._add_assessment_result(s, assess_namespace, namespace[result_label])
                self._add_assessment_result_to_matrix(s, assessment_name, result_label)

        self.add_to_report('Assess Scientific Name Validation', total_assessments, result_counts)
        return assessment_name, total_assessments, result_counts

    def _add_assessment_result(self, subject, assessment_type, value, assessment_date=None):
        result_bn = BNode()
        self.g.add((subject, DQAF.hasDQAFResult, result_bn))

        self.g.add((result_bn, SOSA.observedProperty, assessment_type))

        if isinstance(value, URIRef):
            self.g.add((result_bn, SDO.value, value))
        elif isinstance(value, str):
            prefixed_name = self.__uri_to_prefixed_name(value)
            uri_value = self.__prefixed_name_to_uri(prefixed_name)
            self.g.add((result_bn, SDO.value, uri_value))
        else:
            self.g.add((result_bn, SDO.value, Literal(value)))
        if assessment_date is None:
            assessment_date = datetime.now()
        elif isinstance(assessment_date, datetime.date) and not isinstance(assessment_date, datetime.datetime):
            assessment_date = datetime.datetime.combine(assessment_date, datetime.time.min)

        self.g.add((result_bn, SOSA.resultTime, Literal(assessment_date, datatype=XSD.dateTime)))

    def _add_assessment_result_to_matrix(self, subject, assessment_name, label):
        observation_id = UseCaseManager.extract_record_number(subject)
        field_name = assessment_name + ":" + label

        if 'observation_id' in self.result_matrix_df.columns and \
                any(self.result_matrix_df['observation_id'] == observation_id):
            row_index = self.result_matrix_df[self.result_matrix_df['observation_id'] == observation_id].index
            if field_name not in self.result_matrix_df.columns:
                self.result_matrix_df[field_name] = pd.NA
            self.result_matrix_df.loc[row_index, field_name] = 1
        else:
            new_row = {'observation_id': observation_id, field_name: 1}
            self.result_matrix_df.loc[len(self.result_matrix_df)] = new_row

    def add_to_report(self, assessment_name, total_assessments, result_counts):
        if self.report_file:
            print(f'', file=self.report_file)
            print(f'- {assessment_name}: {total_assessments}', file=self.report_file)
            for quality, count in result_counts.items():
                print(f'\t{quality}: {count}', file=self.report_file)


class DateChecker:
    def __init__(self, data, date_format="%Y-%m-%d"):
        self.data = data
        self.date_format = date_format

    @staticmethod
    def is_date_recent(date_literal, years_back=20):
        if date_literal.datatype in [XSD.dateTime, XSD.dateTimeStamp]:
            datetime_obj = datetime.fromisoformat(date_literal)
            current_year = datetime.now().year
            date_year = datetime_obj.date().year
            return (current_year - years_back) <= date_year <= current_year
        return False

    @staticmethod
    def is_date_not_empty(date):
        if date is None:
            return False
        if isinstance(date, (str, list, dict, set)):
            return bool(date)
        return True

    def find_date_format(self):
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
        if datum is None:
            return False
        if isinstance(datum, (str, list, dict, set)):
            return bool(datum)  # Checks if strings/lists/dicts/sets are not empty
        return True  # For other data types, assume 'not empty' if not None

    def is_valid_datum(self, datum):
        return datum in self.valid_datums

    def get_datum_metadata(self, link: str) -> Optional[dict]:
        # Define a regular expression pattern to match the EPSG link format
        patterns = [r"http://www.opengis.net/def/crs/EPSG/9.9.1/(\d+)", r"http://www.opengis.net/def/crs/EPSG/0/(\d+)"]

        for pattern in patterns:
            if re.match(pattern, link):
                epsg_code = int(link.split("/")[-1])
                return self.datum_metadata.get(epsg_code)
        return None

    def get_datum_metadata_from_asWKT(self, graph, uri):
        asWKT_value = graph.value(subject=URIRef(uri), predicate=URIRef("http://www.opengis.net/ont/geosparql#asWKT"))

        if asWKT_value:
            epsg_link = str(asWKT_value).split(" ")[0][1:-1]  # Remove enclosing "<" and ">"

            return self.get_datum_metadata(epsg_link)

        return None

    def extract_epsg_link(self, wkt_string: str) -> Optional[str]:
        match = re.search(r"<(.+?)>", wkt_string)
        if match:
            return match.group(1)
        return None


class GeoChecker:
    @staticmethod
    def calculate_median_absolute_deviation(coordinates):
        latitudes, longitudes = zip(*coordinates)
        med_lat = np.median(latitudes)
        med_long = np.median(longitudes)
        mad_lat = np.median([abs(lat - med_lat) for lat in latitudes])
        mad_long = np.median([abs(long - med_long) for long in longitudes])
        return mad_lat, mad_long

    @staticmethod
    def assess_coordinate_precision(longitude, latitude):
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

        if lat_quality == "Low" or long_quality == "Low":
            return "Low"
        elif lat_quality == "Medium" or long_quality == "Medium":
            return "Medium"
        else:
            return "High"

    @staticmethod
    def extract_and_assess_coordinate_precision(geometry: object) -> object:
        match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
        if match:
            longitude, latitude = match.groups()
            return GeoChecker.assess_coordinate_precision(longitude, latitude)
        return None

    @staticmethod
    def unusual_check(geometry):
        match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
        if match:
            longitude, latitude = match.groups()
            lon_unusual = RDFDataQualityAssessment.detect_unusual_numbers(longitude) == 'unusual'
            lat_unusual = RDFDataQualityAssessment.detect_unusual_numbers(latitude) == 'unusual'
            if lon_unusual or lat_unusual:
                result_label = "unusual"
            else:
                result_label = "usual"
        else:
            result_label = "usual"
        return result_label

    @staticmethod
    def check_geometry_completeness(geometry):
        match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
        if match:
            return "non_empty"
        else:
            return "empty"


class AustraliaGeographyChecker:
    def __init__(self):
        self.directory_structure = DirectoryStructure()

        self.states_shapefiles = {
            "New_South_Wales": os.path.join(self.directory_structure.map_base_path, "new_south_wales",
                                            "cstnswcd_r.shp"),
            "Victoria": os.path.join(self.directory_structure.map_base_path, "victoria", "cstviccd_r.shp"),
            "Queensland": os.path.join(self.directory_structure.map_base_path, "queensland", "cstqldmd_r.shp"),
            "Western_Australia": os.path.join(self.directory_structure.map_base_path, "western_australia",
                                              "cstwacd_r.shp"),
            "South_Australia": os.path.join(self.directory_structure.map_base_path, "south_australia", "cstsacd_r.shp"),
            "Tasmania": os.path.join(self.directory_structure.map_base_path, "tasmania", "csttascd_r.shp"),
            "Northern_Territory": os.path.join(self.directory_structure.map_base_path, "northern_territory",
                                               "cstntcd_r.shp"),
            "Australian_Capital_Territory": os.path.join(self.directory_structure.map_base_path, "australia",
                                                         "cstauscd_r.shp")
        }

        self.states_data = {
            state_name: gpd.read_file(shapefile).to_crs(epsg=4326)
            for state_name, shapefile in self.states_shapefiles.items()
        }

    def is_point_in_australia_state(self, lat, long):
        point = Point(long, lat)
        for state_name, state_data in self.states_data.items():
            if state_data.contains(point).any():
                return True, state_name
        return False, "Outside Australia"


class ScientificNameChecker:
    def __init__(self):
        pass

    #   self.nsl_df=pd.read_csv(f'nsl\APNI-names-2024-03-27-4556.csv')

    # def check_name(self, name):
    #    self.nsl_df.any( )

    def check_empty(self, data):
        return [s == "" for s in data]

    @staticmethod
    def is_valid_scientific_name(scientific_name):
        if scientific_name:
            return True
        else:
            return False

import os
import sys

import pandas as pd
from rdflib import Graph

# Adjust the path to include the 'dq' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This should be the 'frontend' directory
grandparent_dir = os.path.dirname(parent_dir)  # This should be the project root directory, where 'dq' resides

if grandparent_dir not in sys.path:
    sys.path.append(grandparent_dir)

# Now attempt the import
from dq.assess import RDFDataQualityAssessment
import streamlit as st


def data_quality_assessment_page():
    st.set_page_config(page_title='Data Quality Assessment', layout="wide")

    st.write("This page allows you to run the assessments for the selected input file.")

    uploaded_file = st.file_uploader("Choose a file", type=['ttl'])
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write('Input file:', file_details)

        # choice = st.selectbox(
        #    'Select an Assessment to do',
        #    ('assess_date_completeness', 'assess_coordinate_in_australia_state', 'Predicate 3')
        # )

        if st.button('Do Assessments'):
            with st.spinner('Preparing data...'):
                g = Graph().parse(uploaded_file)
                assessment = RDFDataQualityAssessment(g, None)
            st.success('Data prepared')

            assessments_functions = [assessment.assess_coordinate_precision
                , assessment.assess_coordinate_completeness
                , assessment.assess_coordinate_unusual
                , assessment.assess_coordinate_in_australia_state
                , assessment.assess_coordinate_outlier_irq
                , assessment.assess_coordinate_outlier_zscore
                , assessment.assess_date_recency
                , assessment.assess_date_format_validation
                , assessment.assess_date_completeness
                , assessment.assess_date_outlier_kmeans
                , assessment.assess_date_outlier_irq
                , assessment.assess_scientific_name_completeness
                , assessment.assess_scientific_name_validation
                , assessment.assess_datum_completeness
                , assessment.assess_datum_type
                , assessment.assess_datum_validation]

            assessment_results_df = pd.DataFrame(columns=['Assessment Name', 'Total Assessments', 'Result Counts'])
            df_display = st.empty()

            df_display.dataframe(assessment_results_df,hide_index=True)

            for assess in assessments_functions:
                assessment_name, total_assessments, result_counts = assess()

                new_row_df = pd.DataFrame({
                    'Assessment Name': [assessment_name],
                    'Total Assessments': [total_assessments],
                    'Result Counts': [result_counts]
                })
                assessment_results_df = pd.concat([assessment_results_df, new_row_df], ignore_index=True)
                df_display.dataframe(assessment_results_df)


    else:
        st.write("Please upload a dataset to begin assessment.")


def dict_to_visual_table(dict_obj):
    # Start the HTML table string
    table_str = '<table style="border-collapse: collapse; width: 100%;">'
    # Optional: Add a header row
    table_str += '<tr style="border: 1px solid black;"><th style="border: 1px solid black; padding: 8px;">Label</th><th style="border: 1px solid black; padding: 8px;">Value</th></tr>'
    # Iterate over key-value pairs and add them as rows to the table
    for key, value in dict_obj.items():
        table_str += f'<tr style="border: 1px solid black;"><td style="border: 1px solid black; padding: 8px;">{key}</td><td style="border: 1px solid black; padding: 8px;">{value}</td></tr>'
    # Close the table tag
    table_str += '</table>'
    return table_str


data_quality_assessment_page()

import sys
import os

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
    st.title('Data Quality Assessment')

    st.write("This page allows you to assess the completeness of your dataset based on a selected predicate.")

    # File uploader allows user to add their own dataset
    uploaded_file = st.file_uploader("Choose a file", type=['ttl'])
    if uploaded_file is not None:
        # File details
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write('Input file:', file_details)

        # Dummy predicate selection for demonstration
        predicate_option = st.selectbox(
            'Select Predicate for Completeness Assessment',
            ('Predicate 1', 'Predicate 2', 'Predicate 3')
        )

        if st.button('Assess Completeness'):
            # Initialize your RDFDataQualityAssessment class
            dq_assessor = RDFDataQualityAssessment(uploaded_file)  # Adjust initialization as needed
            # Assuming 'assess_completeness' method exists and expecting parameters as needed
            completeness_score = dq_assessor.get_prime_candidates_for_completeness_checks()

            st.write(f"Completeness Score: {completeness_score}")
    else:
        st.write("Please upload a dataset to begin assessment.")


data_quality_assessment_page()

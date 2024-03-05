import streamlit as st
import pandas as pd
from datetime import datetime


def check_recency(data, year_threshold):
    # Assuming 'date_column' is the name of your date column
    # Convert the date column to date
    data['date_column'] = pd.to_datetime(data['date_column'])
    # Filter data for observations more recent than the threshold
    recent_data = data[data['date_column'].dt.year > year_threshold]
    outdated_data = data[data['date_column'].dt.year <= year_threshold]
    return recent_data, outdated_data


def app():
    st.title('Observation Recency Check')

    st.write("""
    This page allows you to upload your dataset and specify a year to check the recency of observations.
    All observations after the specified year are considered recent.
    """)

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        year_threshold = st.number_input('Enter the year threshold', min_value=1900, max_value=datetime.now().year,
                                         value=datetime.now().year - 1)

        if st.button('Check Recency'):
            recent_data, outdated_data = check_recency(data, year_threshold)
            st.write(f"Total observations: {len(data)}")
            st.write(f"Recent observations (after {year_threshold}): {len(recent_data)}")
            st.write(f"Outdated observations (on or before {year_threshold}): {len(outdated_data)}")

            # Optionally display the data
            show_data = st.checkbox('Show detailed results')
            if show_data:
                st.subheader("Recent Observations")
                st.dataframe(recent_data)
                st.subheader("Outdated Observations")
                st.dataframe(outdated_data)

# Only needed if you are running this script outside of a multipage app context
# Uncomment the next line if you're testing this script standalone
app()

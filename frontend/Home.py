import streamlit as st

# Setting the page title and layout
st.set_page_config(page_title="Data Quality and Geographical Checker", layout="wide")

# Title for your application
st.title("Data Quality and Geographical Checker")

# Introduction
st.markdown("""
Welcome to the Data Quality and Geographical Checker application! 
This tool is designed to help you assess the quality of your environmental or observational data, 
check the recency of observations, and verify geographical relevance, specifically for locations within Australia.

### Features:
- **Data Quality Assessment**: Evaluate the completeness of your datasets based on specific criteria.
- **Observation Recency Check**: Determine whether the observations in your dataset are recent or outdated.
- **Geographical Checker**: Verify if a given location falls within Australia or a specific Australian state.
- **Similarity Search**: Find scientific names similar to a given search term to validate species names in your dataset.

Navigate through the app using the sidebar to access these features and improve your data analysis workflow.
""")

# Optional: Add images or additional instructions
# st.image('path_to_image.jpg', caption='An insightful caption.')

# Footer or additional notes
st.markdown("""
For more information, visit the About/Documentation page or contact us through the Feedback/Contact section.
""")
import streamlit as st

# Setting the page title and layout
st.set_page_config(page_title="About/Documentation", layout="wide")

st.write("""
# About This App

### Purpose and Functionality

This application is designed to facilitate comprehensive data quality assessments for datasets, particularly those structured according to the Resource Description Framework (RDF). It serves as a valuable tool for data scientists, researchers, and information professionals who are working with RDF data, providing them with the capability to evaluate their data against a variety of quality dimensions including completeness, consistency, accuracy, and relevancy.

The app features a user-friendly interface that guides users through various stages of data quality assessment, from initial data upload to detailed analysis and reporting. Key functionalities include:

- **Data Quality Assessment:** Allows users to perform detailed evaluations of their datasets, focusing on specific quality metrics such as completeness, accuracy, and consistency.
- **Observation Recency Check:** Facilitates the examination of data for timeliness and relevance, ensuring that the information remains current and accurate.
- **Geographical Checker:** Provides tools for verifying the geographical data within datasets, ensuring that spatial references are accurate and relevant.
- **Similarity Search:** Enables users to identify duplicate or similar entries within their data, helping to maintain data uniqueness and integrity.
- **Settings/Configuration:** Offers customizable settings to tailor the assessment process to specific user needs or preferences.
- **Documentation and Help:** Includes comprehensive guides and documentation to assist users in navigating the app, understanding its features, and making the most of its capabilities.

### Target Audience

The app is targeted at individuals and organizations dealing with RDF datasets who need to ensure the quality of their data before analysis, publication, or sharing. It caters to a wide range of users, from academic researchers and data librarians to corporate data managers and IT professionals involved in data governance and quality control.

### Motivation Behind Development

The motivation for developing this app stems from the recognition of the critical importance of data quality in the digital age. High-quality data is the foundation of reliable analysis, insightful research, and informed decision-making. However, assessing and ensuring the quality of RDF datasets can be complex and time-consuming without the right tools. This app was developed to address this gap, providing an accessible, efficient, and effective solution for data quality assessment that supports best practices in data management and stewardship.

By streamlining the data quality assessment process, the app aims to empower users to improve the integrity and reliability of their data, thereby enhancing the value of their work and contributing to the broader goal of fostering trust and confidence in digital information resources.

## How to Use

Provide detailed instructions on how to use the app. This could include:
- Step-by-step guides
- Tips for input formats
- Examples of typical use cases

## Technology

Detail the technology stack and algorithms used in this app. For example:
- Python libraries: Streamlit, Pandas, Geopandas, etc.
- Data sources and how they are processed
- Any machine learning models or analytical methods employed

## Acknowledgments

Acknowledge any contributions from individuals, organizations, or open-source projects that have been instrumental in the development of this app.

## Contact Information

Provide information on how users can contact you for support, feedback, or inquiries. This could include an email address, a GitHub repository, or a social media profile.
""")

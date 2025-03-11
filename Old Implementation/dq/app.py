import pandas as pd
import streamlit as st
from rdflib import Graph


st.write("""

### Data Quality Assessment Framework Application
#### RDF file Assessment and Analysis
Using the UI to Interact with the **RDF File**.

""")
st.sidebar.header('User Input Parameters')




# Function to analyze the RDF file
def analyze_rdf(uploaded_file):
    g = Graph()
    g.parse(uploaded_file, format='ttl')
    # Perform your analysis here. For demonstration, we'll just count the triples.
    total_triples = len(g)
    # Count unique subjects, predicates, and objects
    unique_subjects = len(set(g.subjects()))
    unique_predicates = len(set(g.predicates()))
    unique_objects = len(set(g.objects()))
    # Generate the report
    report = (f"The RDF file you've provided contains {total_triples} triples, "
              f"which are the basic units of information in RDF, composed of "
              f"a subject, predicate, and object. It includes {unique_subjects} "
              f"unique subjects, {unique_predicates} unique predicates, and "
              f"{unique_objects} unique objects.")
    return report


# Creating a sidebar for file upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload RDF file", type=['ttl'])
    analyze_button = st.button('Analyze')

# Main area
if uploaded_file is not None:
    # File details
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.write('Input file:', file_details)

    # Analyze the file when the button is clicked
    if analyze_button:
        result = analyze_rdf(uploaded_file)
        st.write(f"The file contains {result} triples.")


        # Display further analysis results here
else:
    st.write("Please upload an RDF file (.ttl) to proceed.")

def user_input_features():
    date_recency_year = st.sidebar.slider('Date Recency Years', 5, 30, 20, 1)
    quality = st.sidebar.slider('High Quality decimal points', 4, 8, 4, 1)

    data = {
        "date_recency": date_recency_year,
        "high_quality": quality

    }
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features()
st.subheader('Input Parameters')
st.write(df)

# Add a button
if st.button('Load Data..'):
    st.write('Hello')

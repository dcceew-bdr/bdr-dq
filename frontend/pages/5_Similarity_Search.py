import streamlit as st
import difflib

st.set_page_config(page_title="Similarity Search", layout="wide")


def find_similar_names(input_name, names_list, cutoff=0.6):
    # Find close matches to the input name from the list, based on the given cutoff for similarity
    similar_names = difflib.get_close_matches(input_name, names_list, n=5, cutoff=cutoff)
    return similar_names


st.write("""
This page allows you to search for similar names based on your input. 
It's particularly useful for finding scientific names that might be spelled differently.
""")

# Example list of names - you might want to load this from a file or a database in a real app
names_list = ["Eucalyptus globulus", "Acacia dealbata", "Banksia serrata", "Grevillea robusta",
              "Callistemon citrinus"]

input_name = st.text_input('Enter a name to search for:')
similarity_threshold = st.slider('Similarity threshold', min_value=0.0, max_value=1.0, value=0.6, step=0.05)

if st.button('Search'):
    similar_names = find_similar_names(input_name, names_list, cutoff=similarity_threshold)

    if similar_names:
        st.success("Found similar names:")
        for name in similar_names:
            st.write(name)
    else:
        st.error("No similar names found.")

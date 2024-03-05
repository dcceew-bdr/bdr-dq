import sys
import os

# Adjust the path to include the 'dq' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This should be the 'frontend' directory
grandparent_dir = os.path.dirname(parent_dir)  # This should be the project root directory, where 'dq' resides

if grandparent_dir not in sys.path:
    sys.path.append(grandparent_dir)

import streamlit as st
import geopandas as gpd
from shapely.geometry import Point

from dq.assess import AustraliaGeographyChecker


# Placeholder function to check if a point is in Australia or a specific state
# This function needs a shapefile of Australia or its states to work
def check_location(lat, lon, shapefile):
    # Load the shapefile
    gdf = gpd.read_file(shapefile)

    # Create a point from the provided latitude and longitude
    point = Point(lon, lat)

    # Check if the point is within the GeoDataFrame
    is_within = gdf.contains(point).any()

    return is_within

st.set_page_config(page_title="Geographical Checker", layout="wide")


st.write("""
This page allows you to check if a given latitude and longitude falls within Australia or a specific Australian state.
""")

lat = st.number_input('Latitude', format="%f")
long = st.number_input('Longitude', format="%f")




if st.button('Check Location'):
    st.write('Latitude: ', lat)
    st.write('Longitude: ', long)

    geo_checker = AustraliaGeographyChecker()
    is_within = geo_checker.is_point_in_australia(lat, long)
    if is_within:
        st.success("The location is within the Australia.")
        state=geo_checker.is_point_in_australia_state(lat,long)
        st.write("State: ",state[1])

    else:
        st.error("The location is outside the Australia.")



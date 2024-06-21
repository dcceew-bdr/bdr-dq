import sys
from pathlib import Path
from typing import Union
import streamlit as st
import folium
from streamlit_folium import st_folium
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import Namespace, SOSA, GEO
import os
import re

# Adjust the path to include the 'dq' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(
    os.path.dirname(current_dir))  # This should be the project root directory, where 'dq' resides

if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

from dq.assess import AustraliaGeographyChecker

# Define namespaces
BDRM = Namespace("https://linked.data.gov.au/def/bdr-msg/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
TERN = Namespace("https://w3id.org/tern/ontologies/tern/")

geo_checker = AustraliaGeographyChecker()

# State colors from Wikipedia (https://en.wikipedia.org/wiki/Australian_state_and_territory_colours)
state_colors = {
    "Australian_Capital_Territory": "#003DA5",  # Blue
    "New_South_Wales": "#9BCBEB",  # Sky Blue
    "Northern_Territory": "#C25E03",  # Red Ochre
    "Queensland": "#73182C",  # Maroon
    "South_Australia": "#D50032",  # Red
    "Tasmania": "#006747",  # Bottle Green
    "Victoria": "#003c71",  # Navy Blue
    "Western_Australia": "#FFD100",  # Gold
    "Outside_Australia": "#808080"  # Gray
}


@st.cache_data
def extract_geo_points(file_content):
    g = Graph().parse(data=file_content, format="ttl")
    geo_points = []
    for observation in g.subjects(RDF.type, TERN.Observation):
        for sample in g.objects(observation, SOSA.hasFeatureOfInterest):
            if (sample, RDF.type, TERN.Sample) in g:
                for procedure in g.objects(sample, SOSA.isResultOf):
                    for geometry_node in g.objects(procedure, GEO.hasGeometry):
                        geometry = next(g.objects(geometry_node, GEO.asWKT), None)
                        if geometry:
                            match = re.search(r"POINT \(([^ ]+) ([^ ]+)\)", str(geometry))
                            if match:
                                lon, lat = map(float, match.groups())
                                in_australia, state_name = geo_checker.is_point_in_australia_state(lat, lon)
                                result_label = state_name if in_australia else "Outside_Australia"
                                info = {
                                    'observation_id': str(observation),
                                    'sample_id': str(sample),
                                    'loc': result_label
                                }
                                geo_points.append({'lat': lat, 'lon': lon, 'info': info, 'state': result_label})
    return geo_points


def create_popup_content(info):
    return f"""
    <div style="font-size:14px;">
        <b>Observation ID:</b> <span style="color:blue;">{info['observation_id']}</span><br>
        <b>Sample ID:</b> <span style="color:green;">{info['sample_id']}</span><br>
        <b>Location:</b> <span style="color:red;">{info['loc']}</span>
    </div>
    """


def filter_geo_points(geo_points, selected_states):
    return [point for point in geo_points if point['state'] in selected_states]


# Streamlit app layout
st.set_page_config(page_title='Geo Points Map with File Upload', layout="wide")

uploaded_file = st.file_uploader("Choose a TTL file", type="ttl")
if uploaded_file:
    file_content = uploaded_file.getvalue()
    st.session_state['geo_points'] = extract_geo_points(file_content)

if 'geo_points' in st.session_state:
    geo_points = st.session_state['geo_points']

    col1, col2 = st.columns([3, 1])
    with col2:
        st.write("### State Filters")
        selected_states = []
        for state in state_colors.keys():
            if st.checkbox(state.replace("_", " "), value=True):
                selected_states.append(state)

    filtered_geo_points = filter_geo_points(geo_points, selected_states)

    with col1:
        if filtered_geo_points:
            m = folium.Map(location=[filtered_geo_points[0]['lat'], filtered_geo_points[0]['lon']], zoom_start=5)
            for point in filtered_geo_points:
                color = state_colors.get(point['state'], '#808080')  # Default to gray if state not found
                folium.CircleMarker(
                    location=[point['lat'], point['lon']],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=folium.Popup(create_popup_content(point['info']), max_width=300)
                ).add_to(m)
            st_folium(m, width=900, height=700, returned_objects=[])
        else:
            st.write("No geo points found for the selected states.")
else:
    st.write("Please upload a TTL file.")

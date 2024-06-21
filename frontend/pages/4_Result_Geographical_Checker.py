import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import re

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
row_state_title = [
    'coordinate_in_australia_state:New_South_Wales',
    'coordinate_in_australia_state:Victoria',
    'coordinate_in_australia_state:Queensland',
    'coordinate_in_australia_state:Western_Australia',
    'coordinate_in_australia_state:South_Australia',
    'coordinate_in_australia_state:Tasmania',
    'coordinate_in_australia_state:Northern_Territory',
    'coordinate_in_australia_state:Australian_Capital_Territory'
]


def get_state_from_row(row):
    state_name = ""
    for state_title in row_state_title:
        if row[state_title] == 1:
            parts = state_title.split(':')
            _, state_name = parts[0], parts[1]
    if len(state_name) == 0:
        state_name = 'Outside_Australia'
    return state_name


# Function to extract geo points from Excel
def extract_geo_points_from_excel(df):
    geo_points = []
    for index, row in df.iterrows():
        try:
            lon, lat = map(float, re.findall(r"[-+]?\d*\.\d+|\d+", row['location']))
            info = row.to_dict()
            state_name= get_state_from_row(row)

            geo_points.append(
                {'lat': lat, 'lon': lon, 'info': info, 'observation_id': row['observation_id'], 'state': state_name})
        except Exception as e:
            st.write(f"Error parsing row {index}: {e}")  # Debugging statement
            continue  # Skip rows with invalid or missing location data
    return geo_points


def create_popup_content(info):
    content = "<div style='font-size:14px;'>"
    for key, value in info.items():
        if pd.notna(value) and value != '':
            content += f"<b>{key}:</b> <span style='color:blue;'>{value}</span><br>"
    content += "</div>"
    return content


def filter_geo_points(geo_points, selected_filters):
     if not selected_filters:
        return geo_points  # No filters applied, return all points

     filtered_points = []
     for point in geo_points:
        match = True
        for group, values in selected_filters.items():
            if not any(point['info'].get(f"{group}:{value}") == 1.0 for value in values):
                match = False
                break
        if match:
           filtered_points.append(point)
     return filtered_points


# Streamlit app layout
st.set_page_config(page_title='Geo Points Map with File Upload', layout="wide")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("File uploaded successfully.")
    st.write("Data Sample:")
    st.write(df.head())  # Display the first few rows of the data frame
    geo_points= extract_geo_points_from_excel(df)
    st.write(f'Geo points: {len(geo_points)}')
    st.session_state['geo_points'] = geo_points

if 'geo_points' in st.session_state:
    geo_points = st.session_state['geo_points']
    st.write(f"Total geographical points extracted: {len(geo_points)}")  # Debugging statement

    if geo_points:
        initial_map_location = [geo_points[0]['lat'], geo_points[0]['lon']]
    else:
        initial_map_location = [0, 0]

    col1, col2 = st.columns([3, 1])
    with col2:
        st.write("### Attribute Filters")
        selected_filters = {}
        attribute_groups = {}

        for column in df.columns:
            if ':' in column:
                group, value = column.split(':')
                if group not in attribute_groups:
                    attribute_groups[group] = []
                attribute_groups[group].append(value)

        for group, values in attribute_groups.items():
            with st.expander(group):
                selected_values = []
                for value in values:
                    if st.checkbox(value, value=True, key=f"{group}:{value}"):
                        selected_values.append(value)
                if selected_values:
                    selected_filters[group] = selected_values

    st.write("Selected Filters:")
    st.write(selected_filters)  # Debugging statement

    filtered_geo_points = filter_geo_points(geo_points, selected_filters)
    st.write(f"Total filtered geographical points: {len(filtered_geo_points)}")  # Debugging statement

    with col1:
        m = folium.Map(location=initial_map_location, zoom_start=5)
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
    st.write("Please upload an Excel file.")

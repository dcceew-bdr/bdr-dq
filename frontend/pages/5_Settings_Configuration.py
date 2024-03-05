import streamlit as st

st.set_page_config(page_title="Settings/Configuration", layout="wide")

st.write("""
Use this page to customize the app settings. (Now is Demo...)
""")

# Assuming you store settings in a session state or similar persistent storage
if 'data_quality_threshold' not in st.session_state:
    st.session_state.data_quality_threshold = 0.8  # Default value
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''  # Default value
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = 'Light'  # Default value

with st.form("settings_form"):
    data_quality_threshold = st.slider('Data Quality Threshold', min_value=0.0, max_value=1.0,
                                       value=st.session_state.data_quality_threshold, step=0.05)
    api_key = st.text_input('API Key', value=st.session_state.api_key)
    app_theme = st.selectbox('App Theme', ['Light', 'Dark'],
                             index=['Light', 'Dark'].index(st.session_state.app_theme))

    submitted = st.form_submit_button("Save Settings")
    if submitted:
        st.session_state.data_quality_threshold = data_quality_threshold
        st.session_state.api_key = api_key
        st.session_state.app_theme = app_theme
        st.success('Settings saved!')

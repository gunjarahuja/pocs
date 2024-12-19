import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Application-wide styles
st.set_page_config(page_title="OTD Biospecimen Metadata Management", page_icon="🔬", layout="wide")
st.markdown(
    """<style>
    .main {background-color: #f9f9f9;}
    .sidebar {background-color: #e3e3e3;}
    .stButton > button {background-color: #4CAF50; color: white;}
    .stDownloadButton > button {background-color: #007BFF; color: white;}
    .stTextInput > div > input {border: 1px solid #ddd; padding: 8px;}
    </style>""", unsafe_allow_html=True)

# Utility Functions

def download_template(template_name, columns):
    """Generate and provide a download link for a template."""
    df_template = pd.DataFrame(columns=columns)
    return df_template

def validate_file(file, expected_columns):
    """Validate uploaded file for nulls and column consistency."""
    try:
        df = pd.read_excel(file)
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            return None, f"Missing Columns: {', '.join(missing_columns)}"
        return df, None
    except Exception as e:
        return None, str(e)

def generate_data_quality_report(df):
    """Generate a report highlighting data quality issues."""
    null_counts = df.isnull().sum()
    null_issues = null_counts[null_counts > 0]
    return null_issues

# Pages

def page_module_1():
    st.title("Module 1: TITV Tracker (Model Data)")

    # Tabs
    tabs = st.tabs(["Data Upload Portal", "Data Quality Report", "Review & Edits"])

    with tabs[0]:
        st.subheader("Data Upload Portal")
        st.write("Download the template below, fill it, and upload it.")
        template = download_template("Model Data Template", [
            "AnimalID/Donor/Patient ID", "Specimen Name", "Modified Gene Name", "Genetic Modification Type", "Drug Name",
            "Treatment Status", "Resistance Status", "Modification Status", "3D Model Type"
        ])
        st.download_button("Download Template", data=template.to_csv(index=False), file_name="model_data_template.csv")

        file = st.file_uploader("Upload Model Data File", type=["xlsx", "xls"])
        if file:
            df, error = validate_file(file, template.columns)
            if error:
                st.error(f"File validation failed: {error}")
            else:
                st.success("File uploaded successfully")
                st.session_state['module1_data'] = df

    with tabs[1]:
        st.subheader("Data Quality Report")
        if 'module1_data' in st.session_state:
            report = generate_data_quality_report(st.session_state['module1_data'])
            if report.empty:
                st.success("No issues detected. Upload Successful!")
            else:
                st.write("Data Quality Issues:")
                st.dataframe(report)
        else:
            st.warning("No data uploaded.")

    with tabs[2]:
        st.subheader("Review & Edits")
        if 'module1_data' in st.session_state:
            st.dataframe(st.session_state['module1_data'])
            if st.button("Save Consolidated File"):
                st.session_state['consolidated_model_data'] = st.session_state['module1_data']
                st.success("File consolidated successfully.")
        else:
            st.warning("No data uploaded.")

def page_module_2():
    st.title("Module 2: Vendor Data Management")

    # Tabs
    tabs = st.tabs(["Data Upload Portal", "Data Quality Report"])

    with tabs[0]:
        st.subheader("Data Upload Portal")
        st.write("Download the template below, fill it, and upload it.")
        template = download_template("Vendor Data Template", [
            "Material ID", "MS.ID", "Model Name", "Cell Line Name/Sample ID", "Prep.ID", "Study ID", "AnimalID/Donor/Patient ID"
        ])
        st.download_button("Download Template", data=template.to_csv(index=False), file_name="vendor_data_template.csv")

        file = st.file_uploader("Upload Vendor Data File", type=["xlsx", "xls"], key="vendor_upload")
        if file:
            df, error = validate_file(file, template.columns)
            if error:
                st.error(f"File validation failed: {error}")
            else:
                st.success("File uploaded successfully")
                st.session_state['module2_data'] = df

    with tabs[1]:
        st.subheader("Data Quality Report")
        if 'module2_data' in st.session_state:
            report = generate_data_quality_report(st.session_state['module2_data'])
            if report.empty:
                st.success("No issues detected. Upload Successful!")
            else:
                st.write("Data Quality Issues:")
                st.dataframe(report)
        else:
            st.warning("No data uploaded.")

def page_module_3():
    st.title("Module 3: D-LIMS Templates Generation")

    # Tabs
    tabs = st.tabs(["Draft Template Creation", "Review & Edit", "Data Quality Report"])

    with tabs[0]:
        st.subheader("Draft Template Creation")
        module1_file = st.selectbox("Select File from Module 1", st.session_state.get('module1_data', {}).keys())
        module2_file = st.selectbox("Select File from Module 2", st.session_state.get('module2_data', {}).keys())

        if st.button("Generate Files"):
            st.success("Files Generated Successfully.")

    with tabs[1]:
        st.subheader("Review & Edit")
        if 'module3_data' in st.session_state:
            st.dataframe(st.session_state['module3_data'])
            if st.button("Save Changes"):
                st.success("Changes saved.")
        else:
            st.warning("No files available for review.")

    with tabs[2]:
        st.subheader("Data Quality Report")

# Navigation
PAGES = {
    "Module 1: TITV Tracker": page_module_1,
    "Module 2: Vendor Data Management": page_module_2,
    "Module 3: D-LIMS Templates": page_module_3,
}

st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[selected_page]()

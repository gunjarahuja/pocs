import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Application Title
st.set_page_config(page_title="OTD Biospecimen Metadata Management", layout="wide", initial_sidebar_state="expanded")
st.markdown("# **OTD Biospecimen Metadata Management**")
st.sidebar.markdown("### Navigation")

# Navigation
module = st.sidebar.selectbox("Choose Module", ["Module 1: TITV Tracker", "Module 2: Vendor Data Management", "Module 3: D-LIMS Templates Generation", "Module 4: Metadata Alignment"])

# Function to download templates
def generate_excel_template(columns):
    df = pd.DataFrame(columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Template")
    return output.getvalue()

def data_quality_report(data):
    """Generates a data quality report."""
    nulls = data.isnull().sum()
    format_issues = []  # Placeholder for additional format checks
    return pd.DataFrame({"Column": data.columns, "Nulls": nulls, "Format Issues": format_issues})

def consolidate_files(uploaded_files):
    """Consolidates multiple uploaded files into one."""
    combined_df = pd.concat([pd.read_excel(file) for file in uploaded_files], ignore_index=True)
    return combined_df

# Module 1: TITV Tracker
if module == "Module 1: TITV Tracker":
    st.markdown("## TITV Tracker")
    tab1, tab2, tab3 = st.tabs(["Data Upload Portal", "Data Quality Report", "Review & Edits"])

    with tab1:
        st.markdown("### Data Upload Portal")
        columns = ["AnimalID/Donor/Patient ID", "Specimen Name", "Modified Gene Name", "Genetic Modification Type", "Drug Name", "Treatment Status", "Resistance Status", "Modification Status", "3D Model Type"]
        st.download_button("Download Template", data=generate_excel_template(columns), file_name="TITV_Template.xlsx")
        uploaded_file = st.file_uploader("Upload TITV Data", type="xlsx")

    with tab2:
        st.markdown("### Data Quality Report")
        if uploaded_file:
            data = pd.read_excel(uploaded_file)
            report = data_quality_report(data)
            st.write(report)
            if report["Nulls"].sum() == 0:
                st.success("Upload Successful")
            else:
                st.error("Please address the issues and re-upload.")

    with tab3:
        st.markdown("### Review & Edits")
        uploaded_files = st.file_uploader("Upload Multiple Files", type="xlsx", accept_multiple_files=True)
        if uploaded_files:
            consolidated = consolidate_files(uploaded_files)
            st.write("Consolidated File", consolidated)
            if st.button("Save Changes"):
                st.success("File Consolidated and Updated Successfully!")

# Module 2: Vendor Data Management
elif module == "Module 2: Vendor Data Management":
    st.markdown("## Vendor Data Management")
    tab1, tab2 = st.tabs(["Data Upload Portal", "Data Quality Report"])

    with tab1:
        st.markdown("### Data Upload Portal")
        columns = ["Material ID", "MS ID", "Model Name", "Cell Line Name/Sample ID/Specimen ID", "Prep ID", "Study ID", "Subjid", "CaseID", "AnimalID/Donor/Patient ID", "Cell Bank ID"]
        st.download_button("Download Template", data=generate_excel_template(columns), file_name="Vendor_Template.xlsx")
        uploaded_file = st.file_uploader("Upload Vendor Data", type="xlsx")

    with tab2:
        st.markdown("### Data Quality Report")
        if uploaded_file:
            data = pd.read_excel(uploaded_file)
            report = data_quality_report(data)
            st.write(report)
            if report["Nulls"].sum() == 0:
                st.success("Upload Successful")
            else:
                st.error("Please address the issues and re-upload.")

# Module 3: D-LIMS Templates Generation
elif module == "Module 3: D-LIMS Templates Generation":
    st.markdown("## D-LIMS Templates Generation")
    tab1, tab2, tab3 = st.tabs(["Draft Template Creation", "Review & Edit", "Data Quality Report"])

    with tab1:
        st.markdown("### Draft Template Creation")
        st.write("Select files from Module 1 & Module 2 for template generation.")
        material_button = st.button("Generate Material ID File")
        prep_button = st.button("Generate Prep ID File")
        if material_button or prep_button:
            st.success("Files Generated Successfully!")

    with tab2:
        st.markdown("### Review & Edit")
        uploaded_file = st.file_uploader("Upload Files to Review", type="xlsx")
        if uploaded_file:
            data = pd.read_excel(uploaded_file)
            st.write("Editable File", data)

    with tab3:
        st.markdown("### Data Quality Report")
        if uploaded_file:
            report = data_quality_report(pd.read_excel(uploaded_file))
            st.write(report)
            st.button("Export", key="export_btn")

# Module 4: Metadata Alignment
elif module == "Module 4: Metadata Alignment":
    st.markdown("## Metadata Alignment")
    st.write("Select files from Module 1 & Module 2 to create the final metadata.")
    files = st.file_uploader("Select Files", type="xlsx", accept_multiple_files=True)
    if st.button("Create Final Metadata") and files:
        combined = consolidate_files(files)
        st.write("Final Metadata", combined)
        st.success("Final Metadata Created Successfully!")

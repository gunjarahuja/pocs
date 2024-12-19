import streamlit as st
import pandas as pd
import numpy as np

# Function to validate uploaded files
def validate_file(file):
    try:
        df = pd.read_excel(file)  # Or pd.read_csv(file) depending on file format
        if not all(df.apply(len) == len(df.index)):
            st.error("Error: Columns in the uploaded file have inconsistent lengths.")
            return None
        return df
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

# Initialize session state to store uploaded files
if 'module1_files' not in st.session_state:
    st.session_state['module1_files'] = {}
if 'module2_files' not in st.session_state:
    st.session_state['module2_files'] = {}

st.title("OTD Biospecimen Metadata Management")

# Module 1: TITV Tracker
with st.expander("Module 1: TITV Tracker"):
    st.subheader("TITV Tracker (Model Data)")

    # Tab 1: Data Upload Portal
    uploaded_file = st.file_uploader("Upload Model Data File (Excel Format)", type=["xlsx", "xls"])
    if uploaded_file:
        df = validate_file(uploaded_file)
        if df is not None:
            st.session_state['module1_files'][uploaded_file.name] = df
            st.success("File uploaded and validated successfully!")

    # Tab 2: Data Quality Report
    if st.button("Generate Data Quality Report (Module 1)"):
        for filename, df in st.session_state['module1_files'].items():
            st.write(f"Data Quality Report for {filename}")
            null_counts = df.isnull().sum()
            st.write("Null Value Counts:", null_counts)
        
    # Tab 3: Review & Edits
    if st.button("Review & Consolidate Files (Module 1)"):
        if st.session_state['module1_files']:
            consolidated_df = pd.concat(st.session_state['module1_files'].values(), ignore_index=True)
            st.dataframe(consolidated_df)
        else:
            st.warning("No files uploaded yet.")

# Module 2: Vendor Data Management
with st.expander("Module 2: Vendor Data Management"):
    st.subheader("Vendor Data Management")

    # Tab 1: Data Upload Portal
    uploaded_vendor_file = st.file_uploader("Upload Vendor Data File (Excel Format)", type=["xlsx", "xls"], key="vendor")
    if uploaded_vendor_file:
        df = validate_file(uploaded_vendor_file)
        if df is not None:
            st.session_state['module2_files'][uploaded_vendor_file.name] = df
            st.success("Vendor file uploaded and validated successfully!")

    # Tab 2: Data Quality Report
    if st.button("Generate Data Quality Report (Module 2)"):
        for filename, df in st.session_state['module2_files'].items():
            st.write(f"Data Quality Report for {filename}")
            null_counts = df.isnull().sum()
            st.write("Null Value Counts:", null_counts)

# Module 3: D-LIMS Templates Generation
with st.expander("Module 3: D-LIMS Templates Generation"):
    st.subheader("D-LIMS Templates Generation")

    # Dropdowns to select files from Module 1 and Module 2
    module1_file = st.selectbox("Select File from Module 1", options=list(st.session_state['module1_files'].keys()))
    module2_file = st.selectbox("Select File from Module 2", options=list(st.session_state['module2_files'].keys()))

    if st.button("Generate Material ID & Prep ID Files"):
        if module1_file and module2_file:
            module1_df = st.session_state['module1_files'][module1_file]
            module2_df = st.session_state['module2_files'][module2_file]

            material_id_file = module1_df.head()  # Placeholder for actual processing
            prep_id_file = module2_df.head()  # Placeholder for actual processing

            st.write("Material ID File:")
            st.dataframe(material_id_file)

            st.write("Prep ID File:")
            st.dataframe(prep_id_file)

# Module 4: Metadata Alignment
with st.expander("Module 4: Metadata Alignment"):
    st.subheader("Metadata Alignment")

    # Dropdowns to select files from Module 1 and Module 2
    module1_file_alignment = st.selectbox("Select File from Module 1 (Alignment)", options=list(st.session_state['module1_files'].keys()), key="align1")
    module2_file_alignment = st.selectbox("Select File from Module 2 (Alignment)", options=list(st.session_state['module2_files'].keys()), key="align2")

    if st.button("Create Final Metadata File"):
        if module1_file_alignment and module2_file_alignment:
            module1_df = st.session_state['module1_files'][module1_file_alignment]
            module2_df = st.session_state['module2_files'][module2_file_alignment]

            final_metadata = pd.merge(module1_df, module2_df, how="outer")  # Placeholder for actual alignment logic
            st.write("Final Metadata File:")
            st.dataframe(final_metadata)
        else:
            st.warning("Please select files from both Module 1 and Module 2.")

import streamlit as st
import pandas as pd
import numpy as np
import base64

# Utility Functions
def validate_file(file):
    try:
        df = pd.read_excel(file)
        if not all(df.apply(len) == len(df.index)):
            st.error("Error: Columns in the uploaded file have inconsistent lengths.")
            return None
        return df
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

def download_template(template_name, data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{template_name}.csv">Download {template_name} Template</a>'
    st.markdown(href, unsafe_allow_html=True)

def generate_quality_report(df):
    null_counts = df.isnull().sum()
    issues = null_counts[null_counts > 0]
    if issues.empty:
        return "No issues identified. Upload successful.", None
    else:
        return "Issues found. Please review:", issues

# Initialize session state for uploaded files
if 'module1_files' not in st.session_state:
    st.session_state['module1_files'] = {}
if 'module2_files' not in st.session_state:
    st.session_state['module2_files'] = {}
if 'generated_files' not in st.session_state:
    st.session_state['generated_files'] = {}

# Sidebar Navigation
st.sidebar.title("Navigation")
module = st.sidebar.radio("Go to", ["Home", "Module 1", "Module 2", "Module 3", "Module 4"])

# Home Page
if module == "Home":
    st.title("OTD Biospecimen Metadata Management")
    st.markdown("Manage biospecimen metadata effectively with quality checks, templates, and alignment.")

# Module 1: TITV Tracker (Model Data)
elif module == "Module 1":
    st.title("Module 1: TITV Tracker (Model Data)")

    with st.expander("1. Data Upload Portal"):
        st.write("Download the template below:")
        template_data = pd.DataFrame({
            "AnimalID/Donor/Patient ID": [],
            "Specimen Name": [],
            "Modified Gene Name": [],
            "Genetic Modification Type": [],
            "Drug Name": [],
            "Treatment Status": [],
            "Resistance Status": [],
            "Modification Status": [],
            "3D Model Type": []
        })
        download_template("TITV_Tracker_Template", template_data)

        uploaded_file = st.file_uploader("Upload TITV Tracker File", type=["xlsx"])
        if uploaded_file:
            df = validate_file(uploaded_file)
            if df is not None:
                st.session_state['module1_files'][uploaded_file.name] = df
                st.success("File uploaded and validated successfully!")

    with st.expander("2. Data Quality Report"):
        if st.button("Generate Data Quality Report (Module 1)"):
            if st.session_state['module1_files']:
                for filename, df in st.session_state['module1_files'].items():
                    st.write(f"Data Quality Report for {filename}")
                    message, issues = generate_quality_report(df)
                    st.write(message)
                    if issues is not None:
                        st.write(issues)
            else:
                st.warning("No files uploaded yet.")

    with st.expander("3. Review & Edits"):
        if st.button("Consolidate and Review Files"):
            if st.session_state['module1_files']:
                consolidated_df = pd.concat(st.session_state['module1_files'].values(), ignore_index=True)
                st.dataframe(consolidated_df)
                st.session_state['consolidated_module1'] = consolidated_df
            else:
                st.warning("No files to consolidate.")

# Module 2: Vendor Data Management
elif module == "Module 2":
    st.title("Module 2: Vendor Data Management")

    with st.expander("1. Data Upload Portal"):
        st.write("Download the template below:")
        vendor_template = pd.DataFrame({
            "Material ID": [],
            "MS ID": [],
            "Model Name": [],
            "Cell Line Name": [],
            "Prep ID": [],
            "Study ID": [],
            "AnimalID/Donor/Patient ID": [],
            "Cell Bank ID": []
        })
        download_template("Vendor_Data_Template", vendor_template)

        vendor_file = st.file_uploader("Upload Vendor Data File", type=["xlsx"], key="vendor")
        if vendor_file:
            df = validate_file(vendor_file)
            if df is not None:
                st.session_state['module2_files'][vendor_file.name] = df
                st.success("Vendor file uploaded and validated successfully!")

    with st.expander("2. Data Quality Report"):
        if st.button("Generate Data Quality Report (Module 2)"):
            if st.session_state['module2_files']:
                for filename, df in st.session_state['module2_files'].items():
                    st.write(f"Data Quality Report for {filename}")
                    message, issues = generate_quality_report(df)
                    st.write(message)
                    if issues is not None:
                        st.write(issues)
            else:
                st.warning("No files uploaded yet.")

# Module 3: D-LIMS Templates Generation
elif module == "Module 3":
    st.title("Module 3: D-LIMS Templates Generation")

    with st.expander("1. Draft Template Creation"):
        module1_file = st.selectbox("Select File from Module 1", options=list(st.session_state['module1_files'].keys()))
        module2_file = st.selectbox("Select File from Module 2", options=list(st.session_state['module2_files'].keys()))

        if st.button("Generate Templates"):
            if module1_file and module2_file:
                module1_df = st.session_state['module1_files'][module1_file]
                module2_df = st.session_state['module2_files'][module2_file]

                material_id_file = module1_df.head()  # Placeholder logic
                prep_id_file = module2_df.head()  # Placeholder logic

                st.session_state['generated_files']['Material_ID_File'] = material_id_file
                st.session_state['generated_files']['Prep_ID_File'] = prep_id_file

                st.success("Files generated successfully!")

    with st.expander("2. Review & Edit"):
        if 'generated_files' in st.session_state:
            for file_name, data in st.session_state['generated_files'].items():
                st.write(file_name)
                st.dataframe(data)

    with st.expander("3. Data Quality Report"):
        if st.button("Generate Data Quality Report (Generated Files)"):
            if 'generated_files' in st.session_state:
                for file_name, df in st.session_state['generated_files'].items():
                    st.write(f"Data Quality Report for {file_name}")
                    message, issues = generate_quality_report(df)
                    st.write(message)
                    if issues is not None:
                        st.write(issues)

# Module 4: Metadata Alignment
elif module == "Module 4":
    st.title("Module 4: Metadata Alignment")

    with st.expander("Metadata Alignment"):
        module1_file_align = st.selectbox("Select File from Module 1 for Alignment", options=list(st.session_state['module1_files'].keys()), key="align1")
        module2_file_align = st.selectbox("Select File from Module 2 for Alignment", options=list(st.session_state['module2_files'].keys()), key="align2")

        if st.button("Create Final Metadata File"):
            if module1_file_align and module2_file_align:
                module1_df = st.session_state['module1_files'][module1_file_align]
                module2_df = st.session_state['module2_files'][module2_file_align]

                final_metadata = pd.merge(module1_df, module2_df, how="outer")  # Placeholder for actual alignment logic
                st.write("Final Metadata File:")
                st.dataframe(final_metadata)
                st.session_state['final_metadata'] = final_metadata

            else:
                st.warning("Please select files from both Module 1 and Module 2.")

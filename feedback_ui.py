# Install required libraries (for deployment on Streamlit Cloud)
# To use this locally, uncomment and run the commands below.
# !pip install streamlit pandas openpyxl

import streamlit as st
import pandas as pd
import os

# Title for the Application
st.title("Data Processing Automation UI")

# Tab navigation for each step
tabs = st.tabs([
    "Upload Data Sources",
    "Generate Upload File",
    "Review & Edit Data",
    "Run Data Quality Checks",
    "Upload to System",
    "Manage Updates"
])

# Step 1: Upload Data Sources
with tabs[0]:
    st.header("Upload Data Sources")
    st.write("Upload your input files from the different data sources here.")
    
    uploaded_files = st.file_uploader(
        "Upload Data Files (CSV, Excel)", 
        type=["csv", "xlsx"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)} files uploaded successfully!")
        dataframes = {}
        for file in uploaded_files:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            dataframes[file.name] = df
            st.write(f"Preview of {file.name}:", df.head())

# Step 2: Generate Upload File
with tabs[1]:
    st.header("Generate Upload File")
    st.write("Click the button to merge data and generate the upload-ready file.")
    
    if st.button("Generate Upload File"):
        if uploaded_files:
            # Placeholder logic: Concatenate all uploaded data (adjust as needed)
            combined_df = pd.concat(dataframes.values())
            st.write("Generated File Preview:", combined_df.head())
            combined_df.to_excel("generated_upload_file.xlsx", index=False)
            st.download_button(
                "Download Generated Upload File", 
                data=open("generated_upload_file.xlsx", "rb"), 
                file_name="upload_file.xlsx"
            )
        else:
            st.warning("Please upload data sources first.")

# Step 3: Review & Edit Data
with tabs[2]:
    st.header("Review & Edit Data")
    st.write("Review the generated file and make manual edits here.")
    
    if "generated_upload_file.xlsx" in os.listdir():
        edited_df = st.experimental_data_editor(
            pd.read_excel("generated_upload_file.xlsx"), 
            num_rows="dynamic"
        )
        if st.button("Save Edits"):
            edited_df.to_excel("edited_upload_file.xlsx", index=False)
            st.success("Edits saved successfully!")
    else:
        st.warning("Generate the upload file first.")

# Step 4: Run Data Quality Checks
with tabs[3]:
    st.header("Run Data Quality Checks")
    st.write("Validate the data for errors or inconsistencies.")
    
    if "edited_upload_file.xlsx" in os.listdir():
        df = pd.read_excel("edited_upload_file.xlsx")
        errors = []
        
        # Sample DQ Checks (customize as needed)
        if df.isnull().values.any():
            errors.append("Missing values detected in the file.")
        if df.duplicated().any():
            errors.append("Duplicate rows found in the file.")
        
        if errors:
            st.error("Data Quality Issues Found:")
            for error in errors:
                st.write(f"- {error}")
        else:
            st.success("No Data Quality Issues Found!")
    else:
        st.warning("Please generate and review the upload file first.")

# Step 5: Upload to System
with tabs[4]:
    st.header("Upload to System")
    st.write("Once the data is validated, upload it to the target system.")
    
    if st.button("Upload File"):
        if "edited_upload_file.xlsx" in os.listdir():
            st.success("File uploaded successfully!")
        else:
            st.warning("Please prepare and validate the file before uploading.")

# Step 6: Manage Updates
with tabs[5]:
    st.header("Manage Updates")
    st.write("Make updates to the uploaded file and re-upload it to the system.")
    
    if "edited_upload_file.xlsx" in os.listdir():
        updated_df = st.experimental_data_editor(
            pd.read_excel("edited_upload_file.xlsx"), 
            num_rows="dynamic"
        )
        if st.button("Save Updated File"):
            updated_df.to_excel("final_upload_file.xlsx", index=False)
            st.success("Updated file saved successfully!")
            st.download_button(
                "Download Updated File", 
                data=open("final_upload_file.xlsx", "rb"), 
                file_name="updated_file.xlsx"
            )
    else:
        st.warning("Please generate and validate the initial file first.")

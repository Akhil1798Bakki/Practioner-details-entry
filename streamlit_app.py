import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Practitioner details")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Data", usecols=list(range(4)), ttl=5)
existing_data['Name'] = existing_data['Name'].astype(str)
existing_data = existing_data.dropna(subset=['Name'])
existing_data = existing_data.dropna(how="all")

# Onboarding New Practitioner Form
with st.form(key="Data_form"):
    name = st.text_input(label="Name*")
    emp_code = st.text_input(label="Emp_Code*")
    primary_skills = st.text_input(label="Primary_Skills*")
    secondary_skills = st.text_input(label="Secondary_Skills")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Practitioner Details")
    
    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not name or not emp_code or not primary_skills or not secondary_skills:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        
        # Drop NaN values from the existing_data DataFrame
        existing_data = existing_data.dropna()

            
        if existing_data["Name"].str.contains(name).any():
            st.warning("The practitioner details has already exists.")
            st.stop()
        
        else:
            # Create a new row of practitioner data
            emp_data = pd.DataFrame(
                [
                    {
                        "Name": name,
                        "Emp_Code": emp_code,
                        "Primary_Skills": primary_skills,
                        "Secondary_Skills": secondary_skills,
                    }
                ]
            )

            # Add the new Practitioner data to the existing data
            updated_df = pd.concat([existing_data, emp_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Data", data=updated_df)

            st.success("Practitioner details successfully submitted!")
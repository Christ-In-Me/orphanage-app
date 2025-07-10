import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title("Orphanage Partnership Database")

# Initialize session state for storing data
if "partnership_data" not in st.session_state:
    st.session_state.partnership_data = []

# Use a dynamic form key to ensure form state resets
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

# Form for data collection
with st.form(key=f"partnership_form_{st.session_state.form_key}"):
    st.subheader("Enter Partnership Details")
    
    # Input fields with explicit keys
    company_name = st.text_input("Company Name (or Individual Name)", key=f"company_name_{st.session_state.form_key}")
    location = st.text_input("Location (e.g., City, Country)", key=f"location_{st.session_state.form_key}")
    amount = st.number_input("Amount Donated (UGX)", min_value=0.0, step=1000.0, key=f"amount_{st.session_state.form_key}")
    date_deposited = st.date_input("Date Amount Deposited", min_value=datetime(2000, 1, 1), key=f"date_deposited_{st.session_state.form_key}")
    depositor_name = st.text_input("Name of Depositor", key=f"depositor_name_{st.session_state.form_key}")
    contact_info = st.text_input("Contact Information (e.g., Email or Phone)", key=f"contact_info_{st.session_state.form_key}")
    partnership_type = st.selectbox("Partnership Type", ["Individual", "Company", "Organization", "Other"], key=f"partnership_type_{st.session_state.form_key}")
    notes = st.text_area("Additional Notes (e.g., purpose of donation, special instructions)", key=f"notes_{st.session_state.form_key}")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# On form submission
if submit_button:
    # Get form values directly from session state to ensure validation
    company_name = st.session_state.get(f"company_name_{st.session_state.form_key}", "").strip()
    location = st.session_state.get(f"location_{st.session_state.form_key}", "").strip()
    depositor_name = st.session_state.get(f"depositor_name_{st.session_state.form_key}", "").strip()
    partnership_type = st.session_state.get(f"partnership_type_{st.session_state.form_key}", "")
    amount = st.session_state.get(f"amount_{st.session_state.form_key}", 0.0)
    date_deposited = st.session_state.get(f"date_deposited_{st.session_state.form_key}", datetime.now())
    contact_info = st.session_state.get(f"contact_info_{st.session_state.form_key}", "")
    notes = st.session_state.get(f"notes_{st.session_state.form_key}", "")

    # Validate required fields
    if not (company_name and location and depositor_name and partnership_type):
        st.error("Please fill in all required fields: Company Name, Location, Depositor Name, and Partnership Type.")
    else:
        new_entry = {
            "Company Name": company_name,
            "Location": location,
            "Amount (UGX)": amount,
            "Date Deposited": date_deposited,
            "Depositor Name": depositor_name,
            "Contact Information": contact_info,
            "Partnership Type": partnership_type,
            "Notes": notes
        }
        st.session_state.partnership_data.append(new_entry)
        st.success("Partnership data submitted successfully!")
        # Increment form key to reset form
        st.session_state.form_key += 1
        st.rerun()

# Debug: Display session state info
st.write(f"Number of entries in session state: {len(st.session_state.partnership_data)}")
if st.session_state.partnership_data:
    st.write("Raw session state data:", st.session_state.partnership_data)

# Display collected data
if st.session_state.partnership_data:
    st.subheader("Collected Partnership Data")
    try:
        df = pd.DataFrame(st.session_state.partnership_data)
        st.dataframe(df, use_container_width=True)
        
        # Download button for CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="orphanage_partnerships.csv",
            mime="text/csv"
        )

        # Bar chart for total donations by Partnership Type
        st.subheader("Total Donations by Partnership Type")
        chart_data = df.groupby("Partnership Type")["Amount (UGX)"].sum().reset_index()
        if not chart_data.empty:
            st.bar_chart(chart_data.set_index("Partnership Type"))
        else:
            st.warning("No data available to display the chart.")
    except Exception as e:
        st.error(f"Error rendering table or chart: {str(e)}")
else:
    st.info("No data submitted yet. Please fill out the form above.")
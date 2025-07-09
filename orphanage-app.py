import streamlit as st
import pandas as pd
from datetime import datetime

# Title of the app
st.title("Orphanage Partnership Database")

# Initialize session state for storing data
if "partnership_data" not in st.session_state:
    st.session_state.partnership_data = []

# Form for data collection
with st.form(key="partnership_form"):
    st.subheader("Enter Partnership Details")
    
    # Input fields
    company_name = st.text_input("Company Name (or Individual Name)")
    location = st.text_input("Location (e.g., City, Country)")
    amount = st.number_input("Amount Donated (UGX)", min_value=0.0, step=1000.0)
    date_deposited = st.date_input("Date Amount Deposited", min_value=datetime(2000, 1, 1))
    depositor_name = st.text_input("Name of Depositor")
    contact_info = st.text_input("Contact Information (e.g., Email or Phone)")
    partnership_type = st.selectbox("Partnership Type", ["Individual", "Company", "Organization", "Other"])
    notes = st.text_area("Additional Notes (e.g., purpose of donation, special instructions)")
    
    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# On form submission
if submit_button:
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

# Display collected data
if st.session_state.partnership_data:
    st.subheader("Collected Partnership Data")
    df = pd.DataFrame(st.session_state.partnership_data)
    st.dataframe(df)
    
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
    st.bar_chart(chart_data.set_index("Partnership Type"))
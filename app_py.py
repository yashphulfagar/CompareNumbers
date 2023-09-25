import subprocess

# Install openpyxl using pip
subprocess.check_call(['pip', 'install', 'openpyxl'])

# Import openpyxl in your Streamlit app
import openpyxl
import streamlit as st

# Your Streamlit app code here


import streamlit as st
import pandas as pd
import base64
import io

# Function to preprocess phone numbers
def preprocess_phone(phone):
    phone_str = str(phone)
    if len(phone_str) == 13:
        return phone_str
    elif len(phone_str) == 12:
        return "+" + phone_str
    elif len(phone_str) == 10:
        return "+91" + phone_str
    else:
        return "Invalid"

# Function to compare phone numbers
def compare_phone_numbers(file1, file2):
    df1 = pd.read_excel(file1, engine='openpyxl')
    df2 = pd.read_excel(file2, engine='openpyxl')

    df1['Phone'] = df1['Phone'].apply(preprocess_phone)
    df2['Phone'] = df2['Phone'].apply(preprocess_phone)

    missing_numbers = df2[~df2['Phone'].isin(df1['Phone'])]

    return missing_numbers

# Streamlit UI
st.title("Match Phone Numbers")
st.write("Upload the Main File in File 1")


# Add a message at the top
st.write("Made with ❤️ by Yash Jain")

uploaded_file1 = st.file_uploader("Upload Excel File 1", type=["xlsx"])
uploaded_file2 = st.file_uploader("Upload Excel File 2", type=["xlsx"])

if uploaded_file1 and uploaded_file2:
    with st.spinner("Processing..."):
        # Save the uploaded files to temporary files
        with open("temp_file1.xlsx", "wb") as f1, open("temp_file2.xlsx", "wb") as f2:
            f1.write(uploaded_file1.read())
            f2.write(uploaded_file2.read())

        missing_numbers = compare_phone_numbers("temp_file1.xlsx", "temp_file2.xlsx")
        st.success("Processing complete!")

        st.write("### Missing Phone Numbers in File 2:")
        st.write(missing_numbers)

        result_file = "missing_numbers.xlsx"
        missing_numbers.to_excel(result_file, index=False)

        with open(result_file, "rb") as f:
            result_data = f.read()
        st.write(f"Download the result: [missing_numbers.xlsx](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(result_data).decode()})")

# Add a message at the bottom
st.write("Made with ❤️ by Yash Jain")

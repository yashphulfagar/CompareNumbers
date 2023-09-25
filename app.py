# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15aGV8N0IqRaoDCrx9Wp14X_aS0NBePlf
"""

pip install openpyxl
pip install streamlit pandas openpyxl

import streamlit as st
import pandas as pd

# Function to preprocess phone numbers
def preprocess_phone(phone):
    if len(phone) == 13:
        return phone
    elif len(phone) == 12:
        return "+" + phone
    elif len(phone) == 10:
        return "+91" + phone
    else:
        return "Invalid"

# Function to compare phone numbers
def compare_phone_numbers(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Preprocess phone numbers in both DataFrames
    df1['Phone'] = df1['Phone'].apply(preprocess_phone)
    df2['Phone'] = df2['Phone'].apply(preprocess_phone)

    # Find numbers in file2 but not in file1
    missing_numbers = df2[~df2['Phone'].isin(df1['Phone'])]

    return missing_numbers

# Streamlit UI
st.title("Phone Number Comparison App")

uploaded_file1 = st.file_uploader("Upload Excel File 1", type=["xlsx"])
uploaded_file2 = st.file_uploader("Upload Excel File 2", type=["xlsx"])

if uploaded_file1 and uploaded_file2:
    with st.spinner("Processing..."):
        missing_numbers = compare_phone_numbers(uploaded_file1, uploaded_file2)
        st.success("Processing complete!")

        st.write("### Missing Phone Numbers in File 2:")
        st.write(missing_numbers)

        # Export the result to a new Excel file
        result_file = "missing_numbers.xlsx"
        missing_numbers.to_excel(result_file, index=False)
        st.write(f"Download the result: [missing_numbers.xlsx](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(open(result_file, 'rb').read()).decode()})")
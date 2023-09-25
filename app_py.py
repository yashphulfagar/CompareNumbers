import streamlit as st
import pandas as pd
import base64

import subprocess

# Command to install 'openpyxl' using pip
command = ["pip", "install", "openpyxl"]

try:
    # Run the command
    subprocess.check_call(command)
    print("openpyxl has been successfully installed.")
except subprocess.CalledProcessError:
    print("Error occurred while installing openpyxl.")


def preprocess_phone_numbers(phone):
    phone_str = str(phone)  # Convert to string to ensure it's treated as text
    if len(phone_str) == 12:
        return "+" + phone_str
    elif len(phone_str) == 10:
        return "+91" + phone_str
    return phone_str  # Return the original value if it doesn't match any condition

def main():
    st.title("Excel Processor")

    uploaded_file1 = st.file_uploader("Upload the first Excel file", type=["xlsx"])
    uploaded_file2 = st.file_uploader("Upload the second Excel file", type=["xlsx"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        # Preprocess phone numbers
        df1['Phone'] = df1['Phone'].apply(preprocess_phone_numbers)
        df2['Phone'] = df2['Phone'].apply(preprocess_phone_numbers)

        # Check if phone numbers in file 2 are in file 1
        df2_not_in_df1 = df2[~df2['Phone'].isin(df1['Phone'])]

        # Save the result to a new Excel file
        result_file_name = "result.xlsx"
        df2_not_in_df1.to_excel(result_file_name, index=False)

        # Display the result
        st.write("Resultant Excel file:")
        st.dataframe(df2_not_in_df1)

        # Provide a download link for the resultant Excel file
        st.write(f"Download the result: [result.xlsx](data:application/octet-stream;base64,{base64.b64encode(open(result_file_name, 'rb').read()).decode()})")

if __name__ == "__main__":
    main()

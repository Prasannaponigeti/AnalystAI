import streamlit as st
import pandas as pd
from io import BytesIO

# -------------------------------
# CSV Download
# -------------------------------
def download_csv(df):
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="analystai_report.csv",
        mime="text/csv"
    )

# -------------------------------
# Excel Download
# -------------------------------
def download_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')

    excel_data = output.getvalue()

    st.download_button(
        label="⬇ Download Excel",
        data=excel_data,
        file_name="analystai_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
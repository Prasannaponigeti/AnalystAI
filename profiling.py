import streamlit as st

def show_data_profile(df):

    st.markdown("---")
    st.header("📊 Data Profiling")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    st.write("### First 5 Rows")
    st.dataframe(df.head())

    st.write("### Available Columns")
    st.write(df.columns.tolist())

    st.write("### Data Types")

    dtypes_df = df.dtypes.astype(str).reset_index()
    dtypes_df.columns = ["Column Name", "Data Type"]

    st.dataframe(dtypes_df)

    st.write("### Summary Statistics")
    st.dataframe(df.describe())
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AnalystAI", layout="wide")

st.title("📊 AnalystAI Dashboard")

# Upload
file = st.file_uploader("Upload CSV", type=["csv"])

# Load data
if file is not None:
    df = pd.read_csv(file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/supermarket_sales.csv")
    st.info("Showing demo data")

# Basic check
st.write(df.head())

# Simple chart
st.subheader("Sales by City")
city_sales = df.groupby("City")["Total"].sum().reset_index()
fig = px.bar(city_sales, x="City", y="Total")
st.plotly_chart(fig)

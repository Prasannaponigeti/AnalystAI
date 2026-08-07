import streamlit as st
import pandas as pd
import plotly.express as px

st.title("AnalystAI")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
else:
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/supermarket_sales.csv")
    st.write("Using demo dataset")

st.write(df.head())

fig = px.bar(df, x="City", y="Total")
st.plotly_chart(fig)


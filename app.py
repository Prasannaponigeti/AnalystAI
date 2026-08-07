import streamlit as st
from modules.upload import upload_dataset
from modules.profiling import show_data_profile
from modules.dashboard import show_business_kpis
from modules.ai import generate_business_insights
from modules.report import download_csv, download_excel
import plotly.express as px
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AnalystAI",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📊 AnalystAI")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Reports", "About"]
)

# -------------------------------
# Upload Dataset
# -------------------------------
st.header("📁 Upload Dataset")

df = upload_dataset()

# ✅ FIXED DEMO DATA (NO ERROR)
if df is None:
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/supermarket_sales.csv")
    st.info("📊 Showing demo dataset. Upload your own file to explore.")

# -------------------------------
# If Data Available
# -------------------------------
if df is not None:

    st.success("✅ Dataset ready!")

    # Filter
    selected_city = st.selectbox(
        "Select a City",
        ["All"] + list(df["City"].unique())
    )

    if selected_city != "All":
        filtered_df = df[df["City"] == selected_city]
    else:
        filtered_df = df

    # -------------------------------
    # DASHBOARD
    # -------------------------------
    if page == "Dashboard":

        st.title("📊 AnalystAI Dashboard")

        # KPIs
        show_business_kpis(filtered_df)

        st.markdown("---")

        # Executive Summary
        st.header("📊 Executive Summary")

        total_sales = filtered_df["Total"].sum()
        avg_sales = filtered_df["Total"].mean()
        top_city = filtered_df.groupby("City")["Total"].sum().idxmax()
        top_product = filtered_df.groupby("Product line")["Total"].sum().idxmax()

        st.success(f"""
        📌 Total Sales: {total_sales:.2f}  
        📌 Average Sales: {avg_sales:.2f}  
        📌 Top City: {top_city}  
        📌 Top Product: {top_product}  
        """)

        st.markdown("---")

        # Charts
        st.subheader("📈 Sales by City")
        city_sales = filtered_df.groupby("City")["Total"].sum().reset_index()
        fig1 = px.bar(city_sales, x="City", y="Total", color="City")
        st.plotly_chart(fig1, use_container_width=True, key="chart1")

        st.subheader("📊 Product Sales")
        product_sales = filtered_df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True, key="chart2")

        st.subheader("💳 Payment Distribution")
        payment_data = filtered_df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True, key="chart3")

        st.subheader("📈 Sales Trend")
        trend_df = filtered_df.copy()
        trend_df["Date"] = pd.to_datetime(trend_df["Date"])
        trend = trend_df.groupby("Date")["Total"].sum().reset_index()
        fig4 = px.line(trend, x="Date", y="Total")
        st.plotly_chart(fig4, use_container_width=True, key="chart4")

        st.markdown("---")

        # AI Insights
        st.header("🤖 AI Business Insights")

        if st.button("Generate AI Insights"):

            prompt = f"""
            Analyze this data:
            Total Rows: {filtered_df.shape[0]}
            Total Sales: {filtered_df['Total'].sum()}
            """

            insights = generate_business_insights(prompt, filtered_df)

            st.success("Analysis Complete")
            st.write(insights)

    # -------------------------------
    # REPORTS
    # -------------------------------
    elif page == "Reports":

        st.title("📄 Reports")

        download_csv(filtered_df)
        download_excel(filtered_df)

        st.markdown("---")

        st.subheader("📊 Sales by City")
        city_sales = filtered_df.groupby("City")["Total"].sum().reset_index()
        fig1 = px.bar(city_sales, x="City", y="Total", color="City")
        st.plotly_chart(fig1, use_container_width=True, key="r_chart1")

        st.subheader("📊 Sales by Product")
        product_sales = filtered_df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True, key="r_chart2")

        st.subheader("💳 Payment Distribution")
        payment_data = filtered_df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True, key="r_chart3")

    # -------------------------------
    # ABOUT
    # -------------------------------
    elif page == "About":

        st.title("ℹ️ About AnalystAI")
        st.write("This is an AI-powered Business Intelligence dashboard built using Streamlit.")
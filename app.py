import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AnalystAI", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("📊 AnalystAI")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Reports", "About"]
)

st.sidebar.markdown("---")
st.sidebar.info("Upload a dataset to begin analysis")

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 AnalystAI Dashboard")

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.header("📁 Upload Dataset")

file = st.file_uploader("Upload CSV File", type=["csv"])

# STOP if no file
if file is None:
    st.info("👆 Please upload a dataset to continue")
    st.stop()

# -------------------------------
# READ DATA
# -------------------------------
df = pd.read_csv(file)

st.success("✅ Dataset Uploaded Successfully!")

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head())

# -------------------------------
# VALIDATION
# -------------------------------
if "Total" not in df.columns:
    st.error("Dataset must contain 'Total' column")
    st.stop()

# -------------------------------
# FILTER
# -------------------------------
if "City" in df.columns:
    selected_city = st.selectbox(
        "Select City",
        ["All"] + list(df["City"].dropna().unique())
    )

    if selected_city != "All":
        df = df[df["City"] == selected_city]

# -------------------------------
# DASHBOARD
# -------------------------------
if page == "Dashboard":

    st.markdown("## 📊 Business Dashboard")
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"{df['Total'].sum():.2f}")
    col2.metric("📊 Avg Sales", f"{df['Total'].mean():.2f}")
    col3.metric("🔥 Max Sale", f"{df['Total'].max():.2f}")
    col4.metric("📦 Transactions", df.shape[0])

    st.markdown("---")

    # CHARTS

    # Sales by City
    if "City" in df.columns:
        st.subheader("📊 Sales by City")
        city_sales = df.groupby("City")["Total"].sum().reset_index()
        fig1 = px.bar(city_sales, x="City", y="Total", color="City")
        st.plotly_chart(fig1, use_container_width=True)

    # Product Sales
    if "Product line" in df.columns:
        st.subheader("📦 Product Sales")
        product_sales = df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True)

    # Payment Distribution
    if "Payment" in df.columns:
        st.subheader("💳 Payment Distribution")
        payment_data = df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True)

    # Sales Trend
    if "Date" in df.columns:
        st.subheader("📈 Sales Trend")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        trend = df.groupby("Date")["Total"].sum().reset_index()
        fig4 = px.line(trend, x="Date", y="Total")
        st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------
    # 🤖 AI INSIGHTS (NO API)
    # -------------------------------
    st.markdown("---")
    st.subheader("🤖 AI Business Insights")

    if st.button("Generate AI Insights"):

        insights = []

        total_sales = df["Total"].sum()
        avg_sales = df["Total"].mean()

        insights.append(f"📊 Total revenue is {total_sales:.2f}")
        insights.append(f"📈 Average transaction is {avg_sales:.2f}")

        if "City" in df.columns:
            top_city = df.groupby("City")["Total"].sum().idxmax()
            insights.append(f"🏆 Top performing city: {top_city}")

        if "Product line" in df.columns:
            top_product = df.groupby("Product line")["Total"].sum().idxmax()
            insights.append(f"🔥 Best product category: {top_product}")

        if "Payment" in df.columns:
            top_payment = df["Payment"].value_counts().idxmax()
            insights.append(f"💳 Most used payment method: {top_payment}")

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            trend = df.groupby("Date")["Total"].sum()

            if len(trend) > 1:
                if trend.iloc[-1] > trend.iloc[0]:
                    insights.append("📈 Sales trend is increasing")
                else:
                    insights.append("📉 Sales trend is decreasing")

        st.success("✅ Insights Generated")

        for i in insights:
            st.write(i)

# -------------------------------
# REPORTS
# -------------------------------
elif page == "Reports":

    st.markdown("## 📄 Reports")
    st.markdown("---")

    # Download
    st.download_button(
        "📥 Download CSV",
        df.to_csv(index=False),
        file_name="processed_data.csv"
    )

    st.markdown("---")

    if "City" in df.columns:
        st.subheader("📊 City Report")
        city_sales = df.groupby("City")["Total"].sum().reset_index()
        fig1 = px.bar(city_sales, x="City", y="Total", color="City")
        st.plotly_chart(fig1, use_container_width=True)

    if "Product line" in df.columns:
        st.subheader("📦 Product Report")
        product_sales = df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True)

    if "Payment" in df.columns:
        st.subheader("💳 Payment Report")
        payment_data = df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# ABOUT
# -------------------------------
elif page == "About":

    st.markdown("## ℹ️ About AnalystAI")

    st.write("""
    AnalystAI is a Business Intelligence dashboard built using Streamlit.

    🔹 Upload any CSV dataset  
    🔹 Get KPIs and insights  
    🔹 Visualize data with charts  
    🔹 Generate AI-based insights (rule-based)  

    🚀 Built for Data Analysis & Decision Making
    """)
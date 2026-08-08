import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="AnalystAI", layout="wide")

st.title("📊 AnalystAI")

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("📊 AnalystAI")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Reports", "About"]
)

# -------------------------------
# FILE UPLOAD
# -------------------------------
st.header("📁 Upload Dataset")

file = st.file_uploader("Upload your CSV file", type=["csv"])

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
# DASHBOARD PAGE
# -------------------------------
if page == "Dashboard":

    st.header("📊 Dashboard")

    # KPIs
    if "Total" in df.columns:
        total_sales = df["Total"].sum()
        avg_sales = df["Total"].mean()

        col1, col2 = st.columns(2)
        col1.metric("Total Sales", f"{total_sales:.2f}")
        col2.metric("Average Sales", f"{avg_sales:.2f}")

    st.markdown("---")

    # 📊 Sales by City
    if "City" in df.columns and "Total" in df.columns:
        st.subheader("📊 Sales by City")
        city_sales = df.groupby("City")["Total"].sum().reset_index()
        fig1 = px.bar(city_sales, x="City", y="Total", color="City")
        st.plotly_chart(fig1, use_container_width=True)

    # 📦 Product Sales
    if "Product line" in df.columns and "Total" in df.columns:
        st.subheader("📦 Product Sales")
        product_sales = df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True)

    # 💳 Payment Distribution
    if "Payment" in df.columns and "Total" in df.columns:
        st.subheader("💳 Payment Distribution")
        payment_data = df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True)

    # 📈 Sales Trend
    if "Date" in df.columns and "Total" in df.columns:
        st.subheader("📈 Sales Trend")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        trend = df.groupby("Date")["Total"].sum().reset_index()
        fig4 = px.line(trend, x="Date", y="Total")
        st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------
    # 🤖 AI INSIGHTS
    # -------------------------------
    st.markdown("---")
    st.header("🤖 AI Insights")

    if st.button("Generate Insights"):

        insights = []

        if "City" in df.columns and "Total" in df.columns:
            top_city = df.groupby("City")["Total"].sum().idxmax()
            insights.append(f"🔹 Highest sales are in **{top_city}**")

        if "Product line" in df.columns and "Total" in df.columns:
            top_product = df.groupby("Product line")["Total"].sum().idxmax()
            insights.append(f"🔹 Top selling product is **{top_product}**")

        if "Payment" in df.columns:
            top_payment = df["Payment"].mode()[0]
            insights.append(f"🔹 Most used payment method is **{top_payment}**")

        if "Total" in df.columns:
            insights.append(f"🔹 Total revenue is **{df['Total'].sum():.2f}**")

        for i in insights:
            st.success(i)

# -------------------------------
# REPORTS PAGE
# -------------------------------
elif page == "Reports":

    st.header("📄 Reports")

    # City Filter
    if "City" in df.columns:
        selected_city = st.selectbox(
            "Select City",
            df["City"].dropna().unique()
        )
        filtered_df = df[df["City"] == selected_city]
        st.success(f"Showing data for: {selected_city}")
    else:
        filtered_df = df

    # Download
    st.download_button(
        "⬇ Download CSV",
        filtered_df.to_csv(index=False),
        file_name="report.csv"
    )

    st.markdown("---")

    # Charts
    if "Product line" in filtered_df.columns and "Total" in filtered_df.columns:
        st.subheader("📊 Product Sales")
        product_sales = filtered_df.groupby("Product line")["Total"].sum().reset_index()
        fig2 = px.bar(product_sales, x="Product line", y="Total", color="Product line")
        st.plotly_chart(fig2, use_container_width=True)

    if "Payment" in filtered_df.columns and "Total" in filtered_df.columns:
        st.subheader("💳 Payment Distribution")
        payment_data = filtered_df.groupby("Payment")["Total"].sum().reset_index()
        fig3 = px.pie(payment_data, names="Payment", values="Total")
        st.plotly_chart(fig3, use_container_width=True)

    if "Date" in filtered_df.columns and "Total" in filtered_df.columns:
        st.subheader("📈 Sales Trend")
        filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")
        trend = filtered_df.groupby("Date")["Total"].sum().reset_index()
        fig4 = px.line(trend, x="Date", y="Total")
        st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# ABOUT PAGE
# -------------------------------
elif page == "About":

    st.header("ℹ️ About AnalystAI")

    st.write("""
    AnalystAI is an AI-powered business analytics dashboard.

    🔹 Upload CSV datasets  
    🔹 Get instant KPIs  
    🔹 Interactive charts  
    🔹 AI-generated insights  

    Built using:
    - Python
    - Pandas
    - Plotly
    - Streamlit
    """)
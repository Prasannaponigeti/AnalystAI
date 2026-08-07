import streamlit as st

def show_business_kpis(filtered_df):

    st.markdown("---")
    st.header("📊 Business KPIs")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    total_sales = filtered_df["Total"].sum()
    average_sale = filtered_df["Total"].mean()
    total_transactions = filtered_df.shape[0]
    average_rating = filtered_df["Customer stratification rating"].mean()

    kpi1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    kpi2.metric("🛒 Average Sale", f"${average_sale:,.2f}")
    kpi3.metric("📦 Transactions", total_transactions)
    kpi4.metric("⭐ Average Rating", f"{average_rating:.2f}")
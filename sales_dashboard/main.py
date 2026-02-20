import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Superstore Sales Dashboard")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv(
    "sales_dashboard/Sample_ Superstore.csv"
)

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔎 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Order Date'].min(), df['Order Date'].max()]
)

start_date, end_date = date_range

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter)) &
    (df['Order Date'] >= pd.to_datetime(start_date)) &
    (df['Order Date'] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("⚠ No data available for selected filters.")
    st.stop()

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.markdown("## 📌 Key Business Metrics")

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()
avg_discount = filtered_df['Discount'].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)
col4.metric("🎯 Avg Discount", f"{avg_discount:.1f}%")

st.markdown("---")

# ---------------------------------------------------
# PROFIT BY REGION (Interactive)
# ---------------------------------------------------
st.subheader("Profit by Region")

region_profit = (
    filtered_df.groupby('Region')['Profit']
    .sum()
    .reset_index()
)

fig1 = px.bar(
    region_profit,
    x='Region',
    y='Profit',
    text_auto=True,
    title="Profit by Region"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# PROFIT BY SUB-CATEGORY (Interactive)
# ---------------------------------------------------
st.subheader("Profit by Sub-Category")

sub_profit = (
    filtered_df.groupby('Sub-Category')['Profit']
    .sum()
    .reset_index()
)

fig2 = px.bar(
    sub_profit,
    x='Profit',
    y='Sub-Category',
    orientation='h',
    title="Profit by Sub-Category"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# MONTHLY SALES TREND (Interactive)
# ---------------------------------------------------
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index('Order Date')
    .resample('M')['Sales']
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    title="Monthly Sales Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# DISCOUNT VS PROFIT (Interactive)
# ---------------------------------------------------
st.subheader("Discount vs Profit")

fig4 = px.scatter(
    filtered_df,
    x='Discount',
    y='Profit',
    color='Category',
    title="Discount vs Profit"
)

st.plotly_chart(fig4, use_container_width=True)



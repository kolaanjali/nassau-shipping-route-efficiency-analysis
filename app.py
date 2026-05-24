
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Shipping Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Create lead time
df['Lead_Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Title
st.title("Factory-to-Customer Shipping Route Efficiency Analysis")

# KPIs
avg_lead = round(df['Lead_Time'].mean(), 2)
total_orders = df.shape[0]
total_sales = round(df['Sales'].sum(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Average Lead Time", avg_lead)
col2.metric("Total Orders", total_orders)
col3.metric("Total Sales", f"${total_sales}")

# Histogram
st.subheader("Lead Time Distribution")

fig1 = px.histogram(
    df,
    x='Lead_Time',
    nbins=30
)

st.plotly_chart(fig1, use_container_width=True)

# Ship mode comparison
st.subheader("Ship Mode Comparison")

ship_perf = df.groupby('Ship Mode')['Lead_Time'].mean().reset_index()

fig2 = px.bar(
    ship_perf,
    x='Ship Mode',
    y='Lead_Time',
    color='Ship Mode'
)

st.plotly_chart(fig2, use_container_width=True)

# State analysis
st.subheader("State-wise Lead Time")

state_perf = df.groupby('State/Province')['Lead_Time'].mean().reset_index()

fig3 = px.bar(
    state_perf.sort_values(by='Lead_Time', ascending=False).head(15),
    x='State/Province',
    y='Lead_Time'
)

st.plotly_chart(fig3, use_container_width=True)

# Data preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

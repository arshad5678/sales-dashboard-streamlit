import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard - Sample Superstore")
st.subheader("Explore Sales, Profit, and Performance Metrics")

# Load the data
df = pd.read_csv("SampleSuperstore.csv", encoding='latin1')
df.columns = df.columns.str.strip()  # remove extra spaces

# Preprocess date
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False, errors='coerce')
df['Month'] = df['Order Date'].dt.to_period('M')

# Sidebar Filters
st.sidebar.header("📌 Filter Options")
selected_states = st.sidebar.multiselect("Select State(s):", df['State'].unique(), default=df['State'].unique())
selected_categories = st.sidebar.multiselect("Select Category(ies):", df['Category'].unique(), default=df['Category'].unique())
selected_region = st.sidebar.selectbox("Select Region:", df['Region'].unique())

# Apply filters
filtered_df = df[
    (df['State'].isin(selected_states)) &
    (df['Category'].isin(selected_categories)) &
    (df['Region'] == selected_region)
]

# ------------------- METRICS -------------------
st.subheader("📌 Key Metrics")
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df.shape[0]
avg_profit_margin = (filtered_df['Profit'] / filtered_df['Sales']).mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Orders", total_orders)
col4.metric("💹 Avg. Profit Margin", f"{avg_profit_margin:.2f}%")

# ------------------- CHARTS -------------------

# Sales by Category
st.subheader("📊 Sales by Category")
sales_by_cat = filtered_df.groupby('Category')['Sales'].sum().sort_values()
st.bar_chart(sales_by_cat)

# Profit by State
st.subheader("🏙️ Profit by State")
profit_by_state = filtered_df.groupby('State')['Profit'].sum().sort_values()
st.bar_chart(profit_by_state)

# Monthly Sales Trend
st.subheader("📆 Monthly Sales Trend")
monthly_sales = filtered_df.groupby('Month')['Sales'].sum()
st.line_chart(monthly_sales)

# Top 10 Sub-Categories by Sales
st.subheader("🏆 Top 10 Sub-Categories by Sales")
top_subcats = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
fig_top, ax_top = plt.subplots()
top_subcats.plot(kind='barh', ax=ax_top)
st.pyplot(fig_top)

# Heatmap: Region vs Category
st.subheader("🌍 Sales Heatmap (Region vs Category)")
pivot = filtered_df.pivot_table(values='Sales', index='Region', columns='Category', aggfunc='sum', fill_value=0)
fig_heat, ax_heat = plt.subplots()
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax_heat)
st.pyplot(fig_heat)

# Scatter: Profit vs Sales
st.subheader("🔬 Profit vs Sales Scatter Plot")
fig_scatter, ax_scatter = plt.subplots()
ax_scatter.scatter(filtered_df['Sales'], filtered_df['Profit'], alpha=0.6)
ax_scatter.set_xlabel("Sales")
ax_scatter.set_ylabel("Profit")
ax_scatter.set_title("Sales vs Profit")
st.pyplot(fig_scatter)

# Pie chart: Segment Sales
st.subheader("🥧 Sales by Segment")
segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
fig_pie = px.pie(segment_sales, names='Segment', values='Sales', title='Sales Distribution by Segment')
st.plotly_chart(fig_pie)

# Geo chart: Profit by State (Optional)
st.subheader("🗺️ Profit by State (Map View - optional)")
geo_data = df.groupby('State')[['Profit', 'Sales']].sum().reset_index()
fig_map = px.choropleth(geo_data,
                        locations='State',
                        locationmode='USA-states',
                        scope='usa',
                        color='Profit',
                        hover_data=['Sales'],
                        color_continuous_scale='RdBu')
st.plotly_chart(fig_map)

# ------------------- Raw Data -------------------
with st.expander("🔍 Show Raw Filtered Data"):
    st.dataframe(filtered_df)


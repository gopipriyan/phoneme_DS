import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load the dataset
data = pd.read_csv("/content/drive/MyDrive/Phone_pe/agg_trans.csv")

# Title of the web app
st.title("PhonePe Transaction Data Explorer")

# Sidebar filters for transaction data
with st.sidebar:
    st.title("Transaction Filters")
    # Add "Select All" option to the State, Year, and Quarter selection boxes for transaction data
    state_options = ["Select All"] + list(data["State"].unique())
    year_options = ["Select All"] + list(data["Year"].unique())
    quarter_options = ["Select All"] + list(data["Quarter"].unique())

    state = st.selectbox("Select State", state_options, format_func=lambda x: 'Select All' if x == '' else x, help="Choose the state")
    year = st.selectbox("Select Year", year_options, format_func=lambda x: 'Select All' if x == '' else x, help="Choose the year")
    quarter = st.selectbox("Select Quarter", quarter_options, format_func=lambda x: 'Select All' if x == '' else x, help="Choose the quarter")

# Filter transaction data based on selected filters
filtered_data_transaction = data.copy()  # Make a copy of the original data
if state != "Select All":
    filtered_data_transaction = filtered_data_transaction[filtered_data_transaction["State"] == state]
if year != "Select All":
    filtered_data_transaction = filtered_data_transaction[filtered_data_transaction["Year"] == year]
if quarter != "Select All":
    filtered_data_transaction = filtered_data_transaction[filtered_data_transaction["Quarter"] == quarter]

# One-hot encode the 'Transaction_type' column
filtered_data_transaction = pd.get_dummies(filtered_data_transaction, columns=['Transaction_type'])

# Drop non-numeric columns for correlation calculation
non_numeric_columns = ["Region", "Quarter", "State", "Payment_mode"]
filtered_data_transaction_numeric = filtered_data_transaction.drop(columns=non_numeric_columns, errors='ignore')

# Show some useful instructions of the transaction data using metrics
col1, col2, col3 = st.columns(3)

# Calculate metrics based on filtered transaction data
total_transactions = filtered_data_transaction["Transaction_count"].sum()
avg_transaction_amount = filtered_data_transaction["Transaction_amount"].mean()
max_transaction_amount = filtered_data_transaction["Transaction_amount"].max()

# Display metrics for transaction data
with col1:
    st.metric("Total Transactions", total_transactions)
with col2:
    st.metric("Average Transaction Amount", avg_transaction_amount)
with col3:
    st.metric("Highest Transaction Amount", max_transaction_amount)

# Create Altair chart for transaction data
c_transaction = alt.Chart(filtered_data_transaction).mark_circle().encode(
    x=alt.X('Transaction_count', title='Transaction Count', axis=alt.Axis(grid=False, labelColor="#707070")),
    y=alt.Y('Transaction_amount', title='Transaction Amount', axis=alt.Axis(grid=False, labelColor="#707070")),
    size=alt.Size(value=32),
    opacity=alt.value(0.8)
).properties(
    width=500, height=300
).configure_title(
    fontSize=20,
    color='#2E4057'
)

# Group data by "Region" and aggregate by count
grouped_data_region = filtered_data_transaction.groupby('Region').size().reset_index(name='Count')

# Create Altair chart for data grouped by "Region"
c_region = (
    alt.Chart(grouped_data_region)
    .mark_bar()
    .encode(
        x=alt.X("Count:Q", title="Count", axis=alt.Axis(grid=False, labelColor="#707070")),
        y=alt.Y("Region:N", title="Region", axis=alt.Axis(grid=False, labelColor="#707070")),
        color=alt.Color("Region:N", legend=None),
    )
    .properties(width=500, height=300)
)

# Plot line chart for 'Transaction_count'
st.subheader("Line Chart for Transaction Count")
st.line_chart(filtered_data_transaction['Transaction_count'], width=0, height=0)

# Plot Plotly distplot for 'Transaction_count'
st.subheader("Histogram for Transaction Count")
fig = px.histogram(filtered_data_transaction, x='Transaction_count', nbins=20)
fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font': {'color': "#707070"}
})
st.plotly_chart(fig, use_container_width=True)

# Show correlation heatmap
st.subheader("Correlation Heatmap")
corr = filtered_data_transaction_numeric.corr()
fig_heatmap = px.imshow(corr)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Display both Altair charts in a column layout
st.subheader("Transaction Data Visualization")
col1, col2 = st.columns(2)
with col1:
    st.altair_chart(c_transaction, use_container_width=True)
with col2:
    st.altair_chart(c_region, use_container_width=True)

# Additional Insights
st.subheader("Additional Insights")

# Show the distribution of Transaction Amount
st.subheader("Distribution of Transaction Amount")
fig_hist = px.histogram(filtered_data_transaction, x='Transaction_amount', nbins=20)
fig_hist.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font': {'color': "#707070"}
})
st.plotly_chart(fig_hist, use_container_width=True)

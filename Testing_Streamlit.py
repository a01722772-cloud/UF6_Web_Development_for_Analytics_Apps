# This app loads sales data from 'sellers.xlsx',
# lets the user filter by region and vendor,
# and displays tables and charts for units sold,
# total sales, and average sales.



import streamlit as st           
import pandas as pd              
import matplotlib.pyplot as plt  

# Streamlit page configuration 
st.set_page_config(page_title="Sellers Dashboard", layout="wide")

# App Title 
st.title(" Sellers Dashboard")
st.write("Analyze and visualize sales performance by region and vendor.")

#  Load the Excel file directly 
df = pd.read_csv("./sellers.csv", encoding='latin1')

# Clean column names (remove extra spaces and make uppercase)
df.columns = [col.strip().upper() for col in df.columns]

#  Sidebar filters 
st.sidebar.header(" Filters")

# Filter by REGION
regions = df["REGION"].dropna().unique()  # Unique region names
selected_regions = st.sidebar.multiselect(
    "Select Region(s):", regions, default=regions
)

# Filter by vendor (NAME)
vendors = df["NAME"].dropna().unique()  # Unique vendor names
selected_vendor = st.sidebar.selectbox(
    "Select Vendor:", ["All"] + list(vendors)
)

#  Apply filters 
filtered_df = df[df["REGION"].isin(selected_regions)]
if selected_vendor != "All":
    filtered_df = filtered_df[filtered_df["NAME"] == selected_vendor]

#  Display filtered data 
st.subheader(" Filtered Data Table")
st.dataframe(filtered_df)

#  Summary Metrics 
st.subheader(" Summary Statistics")

# Create three columns to show summary metrics
col1, col2, col3 = st.columns(3)

# Calculate metrics based on filtered data
total_units = filtered_df["SOLD UNITS"].sum()
total_sales = filtered_df["TOTAL SALES"].sum()
avg_sales = filtered_df["SALES AVERAGE"].mean()

# Display metrics neatly
col1.metric("Total Units Sold", f"{total_units:,}")
col2.metric("Total Sales", f"${total_sales:,.2f}")
col3.metric("Average Sales", f"${avg_sales:,.2f}")

#  Charts Section 
st.subheader(" Sales Charts")

# Create a figure with 3 side-by-side charts
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# Units Sold by Seller
filtered_df.groupby("NAME")["SOLD UNITS"].sum().plot(
    kind="bar", ax=ax[0], color="skyblue", title="Units Sold by Vendor"
)
ax[0].set_xlabel("Vendor")
ax[0].set_ylabel("Units")

# Total Sales by Seller
filtered_df.groupby("NAME")["TOTAL SALES"].sum().plot(
    kind="bar", ax=ax[1], color="lightgreen", title="Total Sales by Vendor"
)
ax[1].set_xlabel("Vendor")
ax[1].set_ylabel("Sales ($)")

# Average Sales by Seller
filtered_df.groupby("NAME")["SALES AVERAGE"].mean().plot(
    kind="bar", ax=ax[2], color="salmon", title="Average Sales by Vendor"
)
ax[2].set_xlabel("Vendor")
ax[2].set_ylabel("Average ($)")

# Display all charts in Streamlit
st.pyplot(fig)
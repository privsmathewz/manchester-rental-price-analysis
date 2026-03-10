import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple

from analysis_utils import (
    load_data,
    compute_average_rent_by_postcode,
    compute_average_yield_by_postcode,
    compute_monthly_trend,
    prepare_features,
    train_regression_model,
)

st.set_page_config(
    page_title="Manchester Rental Price Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Manchester Rental Price Analysis Dashboard")

# Sidebar configuration
st.sidebar.header("Configuration")

# Upload custom data or use sample
uploaded_file = st.sidebar.file_uploader(
    "Upload your rental data CSV", type=["csv"], help="Use the provided sample dataset or upload your own."
)

def load_dataset() -> pd.DataFrame:
    if uploaded_file is not None:
        data = load_data(uploaded_file)
    else:
        # Load default sample dataset
        data = load_data('data/sample_rental_data_small.csv')
    return data

data = load_dataset()

st.sidebar.markdown("### Filter options")
# Multi-select for postcodes and property types
all_postcodes = sorted(data['postcode'].unique())
selected_postcodes = st.sidebar.multiselect(
    "Select postcodes", options=all_postcodes, default=all_postcodes
)

all_types = sorted(data['property_type'].unique())
selected_types = st.sidebar.multiselect(
    "Select property types", options=all_types, default=all_types
)

# Date range slider
min_date = data['date'].min().to_timestamp()
max_date = data['date'].max().to_timestamp()

date_range = st.sidebar.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="%Y-%m",
)

# Apply filters
mask = (
    data['postcode'].isin(selected_postcodes)
    & data['property_type'].isin(selected_types)
    & (data['date'] >= pd.Period(date_range[0], freq='M'))
    & (data['date'] <= pd.Period(date_range[1], freq='M'))
)
filtered_data = data[mask].copy()

# Display summary statistics
st.subheader("Summary Metrics")
avg_rent_overall = filtered_data['avg_rent'].mean()
max_yield_row = filtered_data.loc[filtered_data['yield_percent'].idxmax()]
highest_yield_postcode = max_yield_row['postcode']
highest_yield_value = max_yield_row['yield_percent']

col1, col2 = st.columns(2)
with col1:
    st.metric("Average Monthly Rent (£)", f"{avg_rent_overall:.2f}")
with col2:
    st.metric(
        f"Highest Yield Postcode",
        f"{highest_yield_postcode} ({highest_yield_value:.2f}%)",
    )

# Average rent by postcode bar chart
st.subheader("Average Rent by Postcode")
avg_rent_df = compute_average_rent_by_postcode(filtered_data)
fig1, ax1 = plt.subplots()
sns.barplot(data=avg_rent_df, x='postcode', y='avg_rent_mean', ax=ax1, palette='viridis')
ax1.set_ylabel("Average Rent (£)")
ax1.set_xlabel("Postcode")
ax1.set_title("Average Rent per Postcode")
st.pyplot(fig1)

# Average yield by postcode bar chart
st.subheader("Average Yield by Postcode")
avg_yield_df = compute_average_yield_by_postcode(filtered_data)
fig2, ax2 = plt.subplots()
sns.barplot(data=avg_yield_df, x='postcode', y='yield_percent_mean', ax=ax2, palette='magma')
ax2.set_ylabel("Average Yield (%)")
ax2.set_xlabel("Postcode")
ax2.set_title("Average Yield per Postcode")
st.pyplot(fig2)

# Monthly trend line chart
st.subheader("Monthly Rent Trend")
monthly_trend = compute_monthly_trend(filtered_data)
fig3, ax3 = plt.subplots()
ax3.plot(monthly_trend['date'].astype(str), monthly_trend['avg_rent_mean'], marker='o')
ax3.set_ylabel("Average Rent (£)")
ax3.set_xlabel("Date (Month)")
ax3.set_title("Average Rent Trend Over Time")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Scatter plot: price vs rent by property type
st.subheader("Price vs Rent by Property Type")
fig4, ax4 = plt.subplots()
for p_type in selected_types:
    subset = filtered_data[filtered_data['property_type'] == p_type]
    ax4.scatter(subset['avg_price'], subset['avg_rent'], label=p_type, alpha=0.7)
ax4.set_xlabel("Average Price (£)")
ax4.set_ylabel("Average Rent (£)")
ax4.set_title("Price vs Rent")
ax4.legend()
st.pyplot(fig4)

# Optional model training
st.subheader("Predictive Modeling")
train_model = st.checkbox(
    "Train regression model to predict rents based on features",
    value=False,
)

if train_model:
    X_processed, y_target, preprocessor = prepare_features(filtered_data)
    model, metrics = train_regression_model(X_processed, y_target)
    st.write("### Model Evaluation")
    st.write(f"Mean Absolute Error (MAE): {metrics['mae']:.2f}")
    st.write(f"R² Score: {metrics['r2']:.3f}")
    st.success("Model training complete.")

# Sidebar notes
st.sidebar.markdown("\n---\n")
st.sidebar.markdown("**Notes:**")
st.sidebar.markdown(
    "This dashboard uses a synthetic dataset representing 2025 rental prices in Manchester.\n"
    "Use the filters to explore different postcodes and property types."
))

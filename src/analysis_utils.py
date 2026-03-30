# src/analysis_utils.py
# Utility functions for Manchester Rental and Affordability Dashboard
# Author: Sajan Mathew, MSc Data Science, Manchester Metropolitan University

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder


def load_data(filepath: str) -> pd.DataFrame:
    """Load and parse the rental dataset from a CSV file."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


def filter_data(
    df: pd.DataFrame,
    postcodes: list,
    property_types: list,
    date_range: tuple,
) -> pd.DataFrame:
    """
    Filter the dataset based on user selections.

    Parameters
    ----------
    df            : full dataframe
    postcodes     : list of selected postcodes
    property_types: list of selected property types
    date_range    : (start_date, end_date) as pandas Timestamps
    """
    mask = (
        df["postcode"].isin(postcodes)
        & df["property_type"].isin(property_types)
        & df["date"].between(date_range[0], date_range[1])
    )
    return df[mask].copy()


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Compute the four headline KPI metrics shown at the top of the dashboard.

    Returns
    -------
    dict with keys: avg_rent, avg_price, avg_yield, top_yield_postcode
    """
    avg_rent = df["avg_rent"].mean()
    avg_price = df["avg_price"].mean()
    avg_yield = df["yield_percent"].mean()

    # Identify the postcode with the highest average yield
    yield_by_postcode = df.groupby("postcode")["yield_percent"].mean()
    top_yield_postcode = yield_by_postcode.idxmax()

    return {
        "avg_rent": avg_rent,
        "avg_price": avg_price,
        "avg_yield": avg_yield,
        "top_yield_postcode": top_yield_postcode,
    }


def compute_affordability_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute an affordability score for each postcode.

    Methodology:
    - Groups data by postcode
    - Calculates avg rent, avg distance to city centre, avg yield
    - Normalises rent score:     lower rent     = higher score (0–1)
    - Normalises distance score: closer to city = higher score (0–1)
    - Combined affordability score = rent 60% + distance 40%
    - Multiplied by 100 for readability

    Returns
    -------
    DataFrame sorted by affordability_score descending
    """
    grouped = df.groupby("postcode").agg(
        avg_rent=("avg_rent", "mean"),
        avg_distance_to_city=("distance_to_city_center_km", "mean"),
        avg_yield=("yield_percent", "mean"),
    ).reset_index()

    # Normalise rent: invert so lower rent → score closer to 1
    rent_min = grouped["avg_rent"].min()
    rent_max = grouped["avg_rent"].max()
    if rent_max != rent_min:
        grouped["rent_score"] = 1 - (
            (grouped["avg_rent"] - rent_min) / (rent_max - rent_min)
        )
    else:
        grouped["rent_score"] = 1.0

    # Normalise distance: invert so closer to city → score closer to 1
    dist_min = grouped["avg_distance_to_city"].min()
    dist_max = grouped["avg_distance_to_city"].max()
    if dist_max != dist_min:
        grouped["distance_score"] = 1 - (
            (grouped["avg_distance_to_city"] - dist_min) / (dist_max - dist_min)
        )
    else:
        grouped["distance_score"] = 1.0

    # Weighted combined score × 100
    grouped["affordability_score"] = (
        0.6 * grouped["rent_score"] + 0.4 * grouped["distance_score"]
    ) * 100

    return grouped.sort_values("affordability_score", ascending=False).reset_index(
        drop=True
    )


def compute_best_areas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank postcodes for two distinct renter profiles.

    Student score:
    - 50% low rent component  (lower rent → higher score)
    - 50% close to university (closer to uni → higher score)

    Professional score:
    - 50% close to city centre (closer to city → higher score)
    - 50% high yield           (higher yield → higher score)

    Scores are on a 0–100 scale for easy comparison.

    Returns
    -------
    DataFrame with columns: postcode, avg_rent, avg_price, avg_yield,
    dist_to_city, dist_to_uni, student_score, professional_score
    """
    grouped = df.groupby("postcode").agg(
        avg_rent=("avg_rent", "mean"),
        avg_price=("avg_price", "mean"),
        avg_yield=("yield_percent", "mean"),
        dist_to_city=("distance_to_city_center_km", "mean"),
        dist_to_uni=("distance_to_university_km", "mean"),
    ).reset_index()

    # --- Student score components ---
    rent_min, rent_max = grouped["avg_rent"].min(), grouped["avg_rent"].max()
    if rent_max != rent_min:
        rent_component = 1 - (grouped["avg_rent"] - rent_min) / (rent_max - rent_min)
    else:
        rent_component = pd.Series([1.0] * len(grouped))

    uni_min, uni_max = grouped["dist_to_uni"].min(), grouped["dist_to_uni"].max()
    if uni_max != uni_min:
        uni_component = 1 - (grouped["dist_to_uni"] - uni_min) / (uni_max - uni_min)
    else:
        uni_component = pd.Series([1.0] * len(grouped))

    grouped["student_score"] = (0.5 * rent_component + 0.5 * uni_component) * 100

    # --- Professional score components ---
    city_min, city_max = grouped["dist_to_city"].min(), grouped["dist_to_city"].max()
    if city_max != city_min:
        city_component = 1 - (
            (grouped["dist_to_city"] - city_min) / (city_max - city_min)
        )
    else:
        city_component = pd.Series([1.0] * len(grouped))

    yield_min, yield_max = grouped["avg_yield"].min(), grouped["avg_yield"].max()
    if yield_max != yield_min:
        yield_component = (grouped["avg_yield"] - yield_min) / (yield_max - yield_min)
    else:
        yield_component = pd.Series([1.0] * len(grouped))

    grouped["professional_score"] = (
        0.5 * city_component + 0.5 * yield_component
    ) * 100

    return grouped


def compute_rent_by_postcode(df: pd.DataFrame) -> pd.DataFrame:
    """Return average rent grouped by postcode."""
    return (
        df.groupby("postcode")["avg_rent"]
        .mean()
        .reset_index()
        .rename(columns={"avg_rent": "avg_rent"})
        .sort_values("postcode")
    )


def compute_yield_by_postcode(df: pd.DataFrame) -> pd.DataFrame:
    """Return average yield grouped by postcode."""
    return (
        df.groupby("postcode")["yield_percent"]
        .mean()
        .reset_index()
        .sort_values("postcode")
    )


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Return average rent grouped by date for the trend line chart."""
    return (
        df.groupby("date")["avg_rent"]
        .mean()
        .reset_index()
        .sort_values("date")
    )


def run_regression(df: pd.DataFrame) -> dict:
    """
    Train a simple linear regression model to predict avg_rent.

    Features used:
    - postcode        (label encoded)
    - property_type   (label encoded)
    - avg_price
    - property_size_sqft
    - distance_to_city_center_km
    - distance_to_university_km

    Returns
    -------
    dict with keys: mae, r2, model, feature_names
    """
    model_df = df.copy()

    # Encode categorical columns as integers for the model
    le_postcode = LabelEncoder()
    le_type = LabelEncoder()
    model_df["postcode_enc"] = le_postcode.fit_transform(model_df["postcode"])
    model_df["type_enc"] = le_type.fit_transform(model_df["property_type"])

    feature_cols = [
        "postcode_enc",
        "type_enc",
        "avg_price",
        "property_size_sqft",
        "distance_to_city_center_km",
        "distance_to_university_km",
    ]

    X = model_df[feature_cols]
    y = model_df["avg_rent"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return {
        "mae": mean_absolute_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred),
        "model": model,
        "feature_names": feature_cols,
    }

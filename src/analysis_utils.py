"""
analysis_utils.py
------------------

This module contains a collection of helper functions for loading and
analyzing rental data for the Manchester rental price analysis project.

The functions defined here focus on common operations such as reading
CSV data, computing descriptive statistics grouped by postcode or
property type, generating time‑series summaries, and fitting a simple
regression model to estimate rental prices based on property
characteristics. All functions are documented with clear type
annotations to improve readability and ease of maintenance.

The synthetic dataset used in this project includes the following
fields:

```
date (YYYY‑MM)
postcode
property_type (Studio, 1‑bed, HMO)
avg_rent (average monthly rent in pounds)
avg_price (average purchase price in pounds)
yield_percent (gross rental yield expressed as a percentage)
property_size_sqft (size of the property in square feet)
distance_to_city_center_km (approximate distance from the property to Manchester city centre)
distance_to_university_km (approximate distance from the property to major universities)
```

Users of this module can import individual functions or the entire
module and use them to perform exploratory analysis, build models,
and prepare data for visualisations.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


def load_data(path: str) -> pd.DataFrame:
    """Load rental data from a CSV file and parse the date column.

    Parameters
    ----------
    path : str
        Path to the CSV file containing the rental data.

    Returns
    -------
    pd.DataFrame
        DataFrame with the parsed data. The ``date`` column is
        converted to a pandas ``Period`` type (monthly frequency).
    """
    df = pd.read_csv(path)
    # Convert date string to Period (year‑month)
    df['date'] = pd.PeriodIndex(df['date'], freq='M')
    return df


def compute_average_rent_by_postcode(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the mean monthly rent for each postcode across all dates and property types.

    Parameters
    ----------
    df : pd.DataFrame
        The rental dataset returned by ``load_data``.

    Returns
    -------
    pd.DataFrame
        A DataFrame with two columns: ``postcode`` and ``avg_rent_mean``,
        showing the average rent per postcode.
    """
    return (
        df.groupby('postcode')['avg_rent']
        .mean()
        .reset_index()
        .rename(columns={'avg_rent': 'avg_rent_mean'})
        .sort_values('avg_rent_mean', ascending=False)
    )


def compute_average_yield_by_postcode(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the mean gross rental yield for each postcode.

    Parameters
    ----------
    df : pd.DataFrame
        The rental dataset.

    Returns
    -------
    pd.DataFrame
        A DataFrame with ``postcode`` and ``yield_percent_mean`` columns.
    """
    return (
        df.groupby('postcode')['yield_percent']
        .mean()
        .reset_index()
        .rename(columns={'yield_percent': 'yield_percent_mean'})
        .sort_values('yield_percent_mean', ascending=False)
    )


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate average rent by month across all postcodes and property types.

    Parameters
    ----------
    df : pd.DataFrame
        The rental dataset with ``date`` as a PeriodIndex.

    Returns
    -------
    pd.DataFrame
        A DataFrame indexed by ``date`` with a single column
        ``avg_rent_mean`` representing the mean rent for each month.
    """
    monthly = df.groupby('date')['avg_rent'].mean().reset_index()
    monthly.rename(columns={'avg_rent': 'avg_rent_mean'}, inplace=True)
    return monthly


def prepare_features(df: pd.DataFrame) -> Tuple[Any, pd.Series, ColumnTransformer]:
    """Prepare feature matrix and target vector for regression modelling.

    Categorical variables (postcode and property_type) are one‑hot
    encoded, and numerical features are standardised. The target
    variable is ``avg_rent``.

    Parameters
    ----------
    df : pd.DataFrame
        The rental dataset.

    Returns
    -------
    X : array‑like
        The feature matrix ready for model fitting.
    y : pd.Series
        The target variable (average rent).
    preprocessor : ColumnTransformer
        The preprocessing transformer containing encoders and scalers.
    """
    # Select features and target
    X = df[['postcode', 'property_type', 'avg_price', 'yield_percent', 'property_size_sqft',
            'distance_to_city_center_km', 'distance_to_university_km']].copy()
    y = df['avg_rent'].copy()

    categorical_features = ['postcode', 'property_type']
    numerical_features = ['avg_price', 'yield_percent', 'property_size_sqft',
                          'distance_to_city_center_km', 'distance_to_university_km']

    # Preprocessing: one‑hot encode categorical variables, standardise numerical variables
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numerical_features),
        ]
    )

    X_processed = preprocessor.fit_transform(X)

    return X_processed, y, preprocessor


def train_regression_model(X: Any, y: pd.Series) -> Tuple[Pipeline, Dict[str, float]]:
    """Fit a linear regression model to predict average rent.

    The function splits the data into training and validation sets,
    fits a LinearRegression estimator, and returns the fitted model
    along with evaluation metrics (MAE and R²).

    Parameters
    ----------
    X : array‑like
        Feature matrix prepared by ``prepare_features``.
    y : pd.Series
        Target variable representing average rent.

    Returns
    -------
    model : Pipeline
        The fitted regression model.
    metrics : Dict[str, float]
        A dictionary containing MAE and R² scores.
    """
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    reg = LinearRegression()
    reg.fit(X_train, y_train)

    y_pred = reg.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    return reg, {'mae': mae, 'r2': r2}


if __name__ == '__main__':
    # Basic usage example when run from command line
    import argparse
    parser = argparse.ArgumentParser(description='Run basic analysis on rental data')
    parser.add_argument('csv_path', type=str, help='Path to the rental CSV data file')
    args = parser.parse_args()

    df = load_data(args.csv_path)
    print('Loaded data with shape:', df.shape)

    avg_rent = compute_average_rent_by_postcode(df)
    print('\nAverage rent by postcode:')
    print(avg_rent)

    avg_yield = compute_average_yield_by_postcode(df)
    print('\nAverage yield by postcode:')
    print(avg_yield)

    monthly_trend = compute_monthly_trend(df)
    print('\nMonthly rent trend:')
    print(monthly_trend.head())

    X_processed, y_target, preprocessor = prepare_features(df)
    model, metrics = train_regression_model(X_processed, y_target)

    print('\nModel evaluation:')
    print(f"Mean Absolute Error (MAE): {metrics['mae']:.2f}")
    print(f"R² Score: {metrics['r2']:.3f}")

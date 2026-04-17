# Manchester Rental Price Analysis

This repository contains a data analysis project exploring rental prices and property characteristics in Manchester, UK. The goal is to understand how factors like location, number of bedrooms, furnishings, and inclusion of bills influence rental costs, and to build models that estimate rent prices.

## Project Overview

Rising housing costs are a major concern for students and working professionals in Manchester. Understanding the drivers of rent helps tenants make informed decisions and property owners set fair prices. In this project we:

- Clean and prepare datasets on rental listings in Manchester.
- Perform exploratory data analysis (EDA) to uncover patterns in price distribution, bedroom counts, furnished vs. unfurnished properties, and inclusion of bills.
- Visualize trends across neighbourhoods and property types.
- Develop predictive models (e.g. linear regression, random forest) to estimate rent based on property features.
- Summarize insights and provide recommendations for renters and landlords.

## Features

- **Data preprocessing:** Handling missing values, converting features to numerical/categorical types, and encoding categorical variables.
- **Exploratory analysis:** Price histograms, box plots, correlation matrices, and geospatial visualizations to examine how rent varies across factors.
- **Predictive modelling:** Building and evaluating regression models to predict rent amounts.
- **Results and insights:** Interpretation of model coefficients and feature importances to understand the key drivers of rent.
- **Future work:** Suggestions for deploying the model as a simple pricing tool or incorporating additional features like proximity to transport or amenities.

## Repository Structure

```
.
├── data/          # Raw and processed datasets (CSV or parquet files)
├── notebooks/     # Jupyter notebooks for EDA, modeling, and visualization
├── src/           # Python scripts for data loading, cleaning, and modeling
├── images/        # Plots and figures used in the analysis
└── README.md      # Project overview and instructions
```

## Getting Started

To reproduce the analysis or run the notebooks locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/privsmathewz/manchester-rental-price-analysis.git
   cd manchester-rental-price-analysis
   ```

2. **Set up a virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Explore the notebooks**
   Open the notebooks in the `notebooks/` folder using Jupyter Notebook or JupyterLab to walk through the EDA and modeling steps.

## Contributing

Contributions are welcome! If you have ideas for additional analyses, improved modeling techniques, or new visualizations, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

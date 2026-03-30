# Manchester Rental and Affordability Dashboard

An interactive Streamlit dashboard analysing rental prices, yields, and affordability across Greater Manchester postcodes. Built as a portfolio project for MSc Data Science at Manchester Metropolitan University.

## Features

- Interactive filters by postcode, property type, and date range
- 4 KPI summary metrics (avg rent, avg price, avg yield, highest yield postcode)
- Affordability scoring by postcode (rent 60% + distance to city 40%)
- Best areas ranking for students vs professionals
- Rent and yield comparison charts by postcode
- Monthly trend analysis (Jan–Oct 2025)
- Price vs rent scatter analysis by property type
- Linear regression rent prediction model with MAE and R²

## How to Run Locally

```bash
git clone https://github.com/privsmathewz/manchester-rental-price-analysis
cd manchester-rental-price-analysis
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Project Structure

```
├── data/
│   └── sample_rental_data_small.csv   # Synthetic 2025 rental dataset (60 rows)
├── src/
│   ├── __init__.py
│   └── analysis_utils.py              # All data processing and modelling functions
├── streamlit_app.py                   # Main dashboard application
├── requirements.txt
└── README.md
```

## Data Sources

- **Synthetic dataset** representing plausible 2025 Manchester rental market conditions across postcodes M1, M3, M5, M13, M14 — portfolio prototype only
- Ward boundary methodology inspired by [Trafford Data Lab](https://www.trafforddatalab.io/)
- Open data approach inspired by [Open Data Manchester](https://www.opendatamanchester.org.uk/)
- Index methodology inspired by [GMODA Digital Exclusion Risk Index](https://www.gmca.gov.uk/)
- Public sector precedent: [GMCA Cost of Living Dashboard](https://www.gmca.gov.uk/our-work/economy/cost-living)
- Next version will integrate real **ONS Private Rental Market Summary Statistics** and **HM Land Registry UK HPI** data

## Built By

**Sajan Mathew**
MSc Data Science, Manchester Metropolitan University

- GitHub: [github.com/privsmathewz](https://github.com/privsmathewz)
- LinkedIn: [linkedin.com/in/sajan-mathew-ab0965257](https://linkedin.com/in/sajan-mathew-ab0965257)

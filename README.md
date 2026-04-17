# Manchester Rental Intelligence Platform

**Live dashboard:** https://manchester-homes.streamlit.app  
**Landing page:** https://madchesterhomes.netlify.app

---

## What it does

Manchester Rental Intelligence is a data product that aggregates synthetic rental market data across Greater Manchester, surfaces affordability and yield signals by postcode, and makes them actionable through interactive visualisations, ML-powered rent prediction, and persona-driven rankings.

---

## Stack

Python · Streamlit · Plotly · pandas · scikit-learn · React · Framer Motion · Netlify · Streamlit Cloud

---

## Project structure

```
manchester-rental-pricing-analysis-site/
├── streamlit_app.py          # App entry point — page config, filters, routing (~194 lines)
├── src/
│   ├── analysis_utils.py     # Data loading, aggregation, ML model training
│   ├── styles.py             # CSS loader (load_css)
│   ├── rankings.py           # Scoring: compute_rankings, compute_pulse, rec_reasons
│   ├── charts.py             # dark_layout, insight helpers
│   ├── predictor.py          # Predictor tab renderer
│   └── tabs/
│       ├── overview.py       # Overview tab renderer
│       ├── rankings.py       # Rankings tab renderer
│       ├── map.py            # Live Map tab renderer + POSTCODE_COORDS
│       ├── trends.py         # Trends tab renderer
│       └── about.py          # About/methodology tab renderer
├── data/
│   └── sample_rental_data_small.csv
├── landing/                  # React + Vite landing page
│   └── src/App.jsx
├── requirements.txt
└── README.md
```

---

## Data

The platform uses a **synthetic dataset** modelled on Greater Manchester rental market patterns (2021–2025).

| Column | Description |
|--------|-------------|
| `date` | Month (YYYY-MM, parsed as Period) |
| `postcode` | District: M1, M3, M5, M13, M14 |
| `property_type` | Studio, 1-bed, HMO |
| `avg_rent` | Average monthly rent (£) |
| `avg_price` | Average purchase price (£) |
| `yield_percent` | Gross rental yield (%) |
| `property_size_sqft` | Property size (sq ft) |
| `distance_to_city_center_km` | Distance to Manchester city centre (km) |
| `distance_to_university_km` | Distance to major universities (km) |

> Values are modelled approximations, not live market data.

---

## Personas

Each persona applies a weighted composite score across normalised postcode metrics.

| Persona | Weights |
|---------|---------|
| **Student** | 40% low rent · 40% low university distance · 20% low city distance |
| **Professional** | 50% low city distance · 30% low rent · 20% high yield |
| **Investor** | 60% high yield · 40% low avg price |
| **Explorer** | 25% each — yield · rent · city distance · university distance |

---

## Forecast methodology

The 6-month rent forecast uses Linear Regression fitted on historical monthly average rent values per postcode, extrapolating forward using engineered time features. This is a directional indicator only. Confidence intervals reflect training MAE and should not be used for investment decisions.

---

## Running locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The landing page (React + Vite):

```bash
cd landing
npm install
npm run dev
```

---

## Built by

**Sajan Mathew** · MSc Data Science · Manchester Metropolitan University  
Graduate Route visa — full UK right to work until June 2028  
[github.com/privsmathewz](https://github.com/privsmathewz) · [linkedin.com/in/sajanmathew](https://linkedin.com/in/sajanmathew)

# streamlit_app.py
# Manchester Rental Intelligence — Portfolio Edition
# Author: Sajan Mathew, MSc Data Science, MMU

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from src.analysis_utils import (
    load_data, filter_data, compute_kpis,
    compute_affordability_score, compute_best_areas,
    compute_rent_by_postcode, compute_yield_by_postcode,
    compute_monthly_trend, run_regression,
)

st.set_page_config(
    page_title="Manchester Homes",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# THEME / STYLES
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --bg:      #060810;
    --bg2:     #080d14;
    --panel:   rgba(255,255,255,0.025);
    --border:  rgba(255,255,255,0.06);
    --green:   #00ff88;
    --text:    #ffffff;
    --muted:   #5a5870;
    --dim:     #3a3850;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #080810;
    color: #d4d2e0 !important;
    -webkit-font-smoothing: antialiased;
}

.main { background: transparent; }
.block-container {
    max-width: 100% !important;
    padding: 0 1.8rem 2rem 1.8rem !important;
}

header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── NAVBAR ─────────────────────────────────────────────────────────────── */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    height: 60px;
    margin: 0 -1.8rem;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #060810;
    border-bottom: 1px solid rgba(0,255,136,0.15);
}
.nav-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    color: #00ff88;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.nav-stats {
    display: flex;
    gap: 32px;
}
.nav-stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #00ff88 !important;
    line-height: 1;
    text-align: center;
}
.nav-stat-label {
    font-size: 0.6rem;
    color: #5a5870 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    margin-top: 3px;
}

/* ── HERO ────────────────────────────────────────────────────────────────── */
.hero {
    background: linear-gradient(180deg, #080d14 0%, #060810 60%);
    padding: 48px 0 32px 0;
    position: relative;
    margin-bottom: 24px;
}
.hero-eyebrow {
    font-size: 0.65rem;
    color: #4a4860 !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.hero-headline {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.05;
    color: #ffffff !important;
    margin-bottom: 16px;
}
.hero-headline .accent { color: #00ff88 !important; }
.hero-sub {
    font-size: 0.92rem;
    color: #7a7a8a !important;
    line-height: 1.7;
    max-width: 480px;
}

/* ── FILTER PILLS ────────────────────────────────────────────────────────── */
.filter-shell {
    background: rgba(0,255,136,0.04);
    border: 1px solid rgba(0,255,136,0.1);
    border-radius: 14px;
    padding: 14px 18px;
    margin: 0 0 20px 0;
}
.filter-label {
    font-size: 0.65rem;
    color: #3a3850;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 700;
    margin-bottom: 10px;
}
.filter-summary {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.summary-pill {
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 5px;
    color: #00ff88 !important;
    font-size: 0.72rem;
    padding: 4px 10px;
    font-weight: 600;
}

/* ── EXPANDER ────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid rgba(0,255,136,0.15) !important;
    border-radius: 10px !important;
    margin: 16px 0 !important;
}
[data-testid="stExpander"]:hover {
    border-color: rgba(0,255,136,0.35) !important;
}
[data-testid="stExpander"] summary {
    color: #00ff88 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] > div > div {
    background: rgba(255,255,255,0.02) !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
    padding: 16px !important;
}

/* ── FILTER LABELS ───────────────────────────────────────────────────────── */
.stMultiSelect label,
.stDateInput label {
    color: #3a3850 !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-weight: 700 !important;
    margin-bottom: 6px !important;
}

/* ── MULTISELECT INPUT ───────────────────────────────────────────────────── */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div:hover {
    border-color: rgba(0,255,136,0.25) !important;
}

/* ── FILTER TAGS — NO RED, NO ORANGE ─────────────────────────────────────── */
[data-baseweb="tag"] {
    background: rgba(0,255,136,0.08) !important;
    border: 1px solid rgba(0,255,136,0.2) !important;
    border-radius: 5px !important;
    color: #00ff88 !important;
    font-size: 0.72rem !important;
    padding: 2px 8px !important;
    font-weight: 600 !important;
}
[data-baseweb="tag"] span { color: #00ff88 !important; }
[data-baseweb="tag"] button {
    color: rgba(0,255,136,0.5) !important;
    padding: 0 2px !important;
}
[data-baseweb="tag"] button:hover { color: #00ff88 !important; }
[data-baseweb="tag"] svg { fill: #00ff88 !important; }

/* ── DATE INPUT ──────────────────────────────────────────────────────────── */
.stDateInput input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    font-size: 0.82rem !important;
}

/* ── DROPDOWN POPOVER ────────────────────────────────────────────────────── */
[data-baseweb="popover"] > div {
    background: #0d0d18 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
[role="option"] {
    color: #5a5870 !important;
    font-size: 0.82rem !important;
    background: transparent !important;
}
[role="option"]:hover {
    background: rgba(0,255,136,0.06) !important;
    color: #00ff88 !important;
}

/* ── KPI CARDS ───────────────────────────────────────────────────────────── */
.kpi-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-top: 2px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 18px 20px 16px 20px;
    min-height: 110px;
}
.kpi-card.green {
    border-top: 2px solid #00ff88;
}
.kpi-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff !important;
    display: block;
    line-height: 1;
    margin-bottom: 8px;
}
.kpi-val.green { color: #00ff88 !important; }
.kpi-lbl {
    font-size: 0.65rem;
    color: #6a6880 !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    display: block;
    margin-bottom: 6px;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #5a5870 !important;
    line-height: 1.5;
    display: block;
}

/* ── INSIGHT CARDS ───────────────────────────────────────────────────────── */
.insight-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 16px;
    height: 100%;
}
.insight-title {
    font-size: 0.62rem;
    color: #5a5870 !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    margin-bottom: 8px;
}
.insight-big {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff !important;
    line-height: 1.3;
    margin-bottom: 8px;
}
.insight-copy {
    font-size: 0.83rem;
    color: #8a8a9a !important;
    line-height: 1.7;
}

/* ── SECTION HEADINGS ────────────────────────────────────────────────────── */
.sec {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff !important;
    margin: 24px 0 6px 0;
}
.sec-desc {
    font-size: 0.86rem;
    color: #7a7a8a !important;
    margin-bottom: 20px;
    line-height: 1.7;
    max-width: 800px;
}
.mini-label {
    font-size: 0.65rem;
    color: #3a3850;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    margin-bottom: 8px;
}

/* ── TABS ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 3px !important;
    width: 100% !important;
    display: flex !important;
}
.stTabs [data-baseweb="tab"] {
    flex: 1 !important;
    text-align: center !important;
    justify-content: center !important;
    color: #6a6880 !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    padding: 10px 0 !important;
}
.stTabs [aria-selected="true"] {
    background: #00ff88 !important;
    color: #060810 !important;
    font-weight: 700 !important;
}

/* ── INFO BOXES ──────────────────────────────────────────────────────────── */
.info-box {
    background: rgba(0,255,136,0.03);
    border-left: 3px solid #00ff88;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 14px 0 18px 0;
    color: #9a9aaa !important;
    line-height: 1.75;
    font-size: 0.86rem;
}
.info-box strong { color: #00ff88 !important; }

/* ── METRICS ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 16px;
}
[data-testid="stMetricValue"] {
    color: #00ff88 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] { color: #5a5870 !important; }

/* ── BUTTONS ─────────────────────────────────────────────────────────────── */
.stDownloadButton > button {
    background: transparent !important;
    color: #00ff88 !important;
    border: 1px solid rgba(0,255,136,0.28) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1rem !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,255,136,0.07) !important;
    border-color: #00ff88 !important;
}
.stCheckbox label { color: #5a5870 !important; }

/* ── LEGEND ──────────────────────────────────────────────────────────────── */
.legend {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    margin-bottom: 14px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #5a5870;
    font-size: 0.8rem;
}
.dot { width: 9px; height: 9px; border-radius: 50%; }

hr {
    border-color: rgba(255,255,255,0.05) !important;
    margin: 24px 0 !important;
}

/* ── FOOTER ──────────────────────────────────────────────────────────────── */
.footer {
    margin-top: 48px;
    padding: 28px 0 12px 0;
    border-top: 1px solid rgba(255,255,255,0.04);
    text-align: center;
    color: #5a5870 !important;
    font-size: 0.8rem;
    line-height: 2;
}
.footer a { color: #00ff88 !important; text-decoration: none; }
.footer-brand {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* ── GENERAL TEXT READABILITY ────────────────────────────────────────────── */
p, div, span, label { color: inherit; }
.stMarkdown p {
    color: #c4c2d0 !important;
    font-size: 0.9rem;
    line-height: 1.7;
}
/* ── DATAFRAME — premium dark table ─────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    border-collapse: collapse !important;
    width: 100% !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stDataFrame"] thead tr {
    background: rgba(0,255,136,0.04) !important;
    border-bottom: 1px solid rgba(0,255,136,0.12) !important;
}
[data-testid="stDataFrame"] thead th {
    color: #00ff88 !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    padding: 12px 16px !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stDataFrame"] tbody tr {
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    transition: background 0.15s !important;
}
[data-testid="stDataFrame"] tbody tr:hover {
    background: rgba(0,255,136,0.03) !important;
}
[data-testid="stDataFrame"] tbody td {
    color: #c4c2d0 !important;
    font-size: 0.84rem !important;
    padding: 11px 16px !important;
    border: none !important;
    background: transparent !important;
    font-weight: 400 !important;
}
[data-testid="stDataFrame"] tbody tr:first-child td {
    color: #ffffff !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(1) td:last-child {
    color: #00ff88 !important;
    font-weight: 700 !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(2) td:last-child {
    color: #00ff88 !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(3) td:last-child {
    color: #4a9eff !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] tbody tr td:first-child {
    color: #3a3850 !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}
[data-testid="stDataFrame"] ::-webkit-scrollbar {
    width: 4px !important;
    height: 4px !important;
}
[data-testid="stDataFrame"] ::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.02) !important;
}
[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {
    background: rgba(0,255,136,0.2) !important;
    border-radius: 4px !important;
}

/* ── MAP POLISH ──────────────────────────────────────────────────────────── */
.mapboxgl-map {
    border-radius: 10px !important;
}
[data-testid="stPlotlyChart"] {
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-testid="column"] {
    padding: 0 8px !important;
}
.element-container:has([data-testid="stPlotlyChart"]):hover {
    filter: brightness(1.05) !important;
    transition: filter 0.3s ease !important;
}

/* ── RESPONSIVE ──────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
    .hero-headline { font-size: 2.4rem; }
    .nav-stats { gap: 16px; }
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# CHART HELPER
# ──────────────────────────────────────────────────────────────────────────────
def chart(fig, title="", height=None):
    updates = dict(
        paper_bgcolor="#0d0d18",
        plot_bgcolor="#0d0d18",
        font=dict(color="#5a5870", family="Space Grotesk"),
        margin=dict(l=16, r=16, t=46 if title else 16, b=16),
        hoverlabel=dict(
            bgcolor="#12121f",
            bordercolor="#00ff88",
            font_color="#ffffff",
            font_family="Space Grotesk",
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.03)",
            zeroline=False,
            title_font=dict(color="#5a5870"),
            tickfont=dict(color="#5a5870"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.03)",
            zeroline=False,
            title_font=dict(color="#5a5870"),
            tickfont=dict(color="#5a5870"),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#5a5870"),
        ),
    )
    if title:
        updates["title"] = dict(
            text=title,
            font=dict(color="#ffffff", size=13, family="Syne"),
        )
    if height:
        updates["height"] = height
    fig.update_layout(**updates)
    return fig

# ──────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    df0 = load_data("data/sample_rental_data_small.csv")
    df0["date"] = pd.to_datetime(df0["date"])
    return df0

df_full = get_data()

# ──────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="nav-brand">MAN HOMES</div>
    <div class="nav-stats">
        <div>
            <div class="nav-stat-num">{df_full['postcode'].nunique()}</div>
            <div class="nav-stat-label">Areas</div>
        </div>
        <div>
            <div class="nav-stat-num">{len(df_full):,}</div>
            <div class="nav-stat-label">Data points</div>
        </div>
        <div>
            <div class="nav-stat-num">2021–2025</div>
            <div class="nav-stat-label">Coverage</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Greater Manchester · Rental Intelligence</div>
    <div class="hero-headline">FIND YOUR<br><span class="accent">PLACE.</span></div>
    <div class="hero-sub">
        Postcode-level rent patterns, affordability scores, yield comparisons,
        trend forecasting, and an ML rent estimator — in one decision-support dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FILTERS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<div class='filter-shell'>", unsafe_allow_html=True)
st.markdown("<div class='filter-label'>Filter the market view</div>", unsafe_allow_html=True)

with st.expander("ADJUST FILTERS", expanded=False):
    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        all_postcodes = sorted(df_full["postcode"].dropna().unique().tolist())
        selected_postcodes = st.multiselect(
            "Postcode area",
            all_postcodes,
            default=all_postcodes,
            help="M1 = city centre · M13/M14 = student areas · M20/M21 = family suburbs"
        )

    with fc2:
        all_types = sorted(df_full["property_type"].dropna().unique().tolist())
        selected_types = st.multiselect(
            "Property type",
            all_types,
            default=all_types,
            help="Studio = cheapest · 1-bed = common entry-level stock · HMO = shared housing"
        )

    with fc3:
        if "area_type" in df_full.columns:
            all_area_types = sorted(df_full["area_type"].dropna().unique().tolist())
            selected_area_types = st.multiselect(
                "Who is it for?",
                all_area_types,
                default=all_area_types,
            )
        else:
            selected_area_types = None

    with fc4:
        min_date = df_full["date"].min().date()
        max_date = df_full["date"].max().date()
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date   = pd.Timestamp(date_range[1])
else:
    start_date = pd.Timestamp(min_date)
    end_date   = pd.Timestamp(max_date)

df = filter_data(df_full, selected_postcodes, selected_types, (start_date, end_date))
if selected_area_types and "area_type" in df.columns:
    df = df[df["area_type"].isin(selected_area_types)]

if df.empty:
    st.warning("No data matches your filters — widen the selection and try again.")
    st.stop()

summary_bits = [
    f"{df['postcode'].nunique()} postcode areas",
    f"{df['property_type'].nunique()} property types",
    f"{len(df):,} filtered records",
    f"{start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}",
]
st.markdown(
    "<div class='filter-summary'>" +
    "".join([f"<div class='summary-pill'>{x}</div>" for x in summary_bits]) +
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────────────────────────────────────
kpis = compute_kpis(df)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div style='background:#1f2021; border-top:2px solid #00ff88;
         padding:24px 20px; border-radius:4px;
         transition: background 0.3s;'>
        <div style='display:flex; justify-content:space-between;
             align-items:flex-start; margin-bottom:16px;'>
            <span style='font-size:1.2rem;'>💷</span>
            <span style='font-size:0.65rem; font-weight:700;
                 color:#00ff88; background:rgba(0,255,136,0.1);
                 padding:2px 8px; letter-spacing:0.08em;'>
                 +LIVE
            </span>
        </div>
        <div style='font-size:0.6rem; color:#849585;
             text-transform:uppercase; letter-spacing:0.14em;
             font-weight:700; margin-bottom:8px;'>
             Avg Monthly Rent
        </div>
        <div style='font-family:Syne,sans-serif; font-size:2rem;
             font-weight:800; color:#f1ffef; line-height:1;
             margin-bottom:8px;'>
             £{kpis['avg_rent']:,.0f}
        </div>
        <div style='font-size:0.65rem; color:#849585;
             font-family:monospace; letter-spacing:0.08em;'>
             PCM / GREATER MANCHESTER
        </div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div style='background:#1f2021; border-top:2px solid #00ff88;
         padding:24px 20px; border-radius:4px;
         transition: background 0.3s;'>
        <div style='display:flex; justify-content:space-between;
             align-items:flex-start; margin-bottom:16px;'>
            <span style='font-size:1.2rem;'>🏠</span>
            <span style='font-size:0.65rem; font-weight:700;
                 color:#00ff88; background:rgba(0,255,136,0.1);
                 padding:2px 8px; letter-spacing:0.08em;'>
                 INDEX
            </span>
        </div>
        <div style='font-size:0.6rem; color:#849585;
             text-transform:uppercase; letter-spacing:0.14em;
             font-weight:700; margin-bottom:8px;'>
             Avg Property Price
        </div>
        <div style='font-family:Syne,sans-serif; font-size:2rem;
             font-weight:800; color:#f1ffef; line-height:1;
             margin-bottom:8px;'>
             £{kpis['avg_price']/1000:.0f}k
        </div>
        <div style='font-size:0.65rem; color:#849585;
             font-family:monospace; letter-spacing:0.08em;'>
             PURCHASE INDEX
        </div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div style='background:#1f2021; border-top:2px solid #00ff88;
         padding:24px 20px; border-radius:4px;
         transition: background 0.3s;'>
        <div style='display:flex; justify-content:space-between;
             align-items:flex-start; margin-bottom:16px;'>
            <span style='font-size:1.2rem;'>📈</span>
            <span style='font-size:0.65rem; font-weight:700;
                 color:#00ff88; background:rgba(0,255,136,0.1);
                 padding:2px 8px; letter-spacing:0.08em;'>
                 HIGH
            </span>
        </div>
        <div style='font-size:0.6rem; color:#849585;
             text-transform:uppercase; letter-spacing:0.14em;
             font-weight:700; margin-bottom:8px;'>
             Avg Gross Yield
        </div>
        <div style='font-family:Syne,sans-serif; font-size:2rem;
             font-weight:800; color:#00ff88; line-height:1;
             margin-bottom:8px;'>
             {kpis['avg_yield']:.1f}%
        </div>
        <div style='font-size:0.65rem; color:#849585;
             font-family:monospace; letter-spacing:0.08em;'>
             NET RENTAL RETURN
        </div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div style='background:#1f2021; border-top:2px solid #00ff88;
         padding:24px 20px; border-radius:4px;
         transition: background 0.3s;'>
        <div style='display:flex; justify-content:space-between;
             align-items:flex-start; margin-bottom:16px;'>
            <span style='font-size:1.2rem;'>⭐</span>
            <span style='font-size:0.65rem; font-weight:700;
                 color:#00ff88; background:rgba(0,255,136,0.1);
                 padding:2px 8px; letter-spacing:0.08em;'>
                 HOT
            </span>
        </div>
        <div style='font-size:0.6rem; color:#849585;
             text-transform:uppercase; letter-spacing:0.14em;
             font-weight:700; margin-bottom:8px;'>
             Top Yield Area
        </div>
        <div style='font-family:Syne,sans-serif; font-size:2rem;
             font-weight:800; color:#00ff88; line-height:1;
             margin-bottom:8px;'>
             {kpis['top_yield_postcode']}
        </div>
        <div style='font-size:0.65rem; color:#849585;
             font-family:monospace; letter-spacing:0.08em;'>
             BEST RETURN DISTRICT
        </div>
    </div>
    """, unsafe_allow_html=True)

# insights row
ins1, ins2, ins3 = st.columns(3)
rent_by_area      = compute_rent_by_postcode(df).sort_values("avg_rent")
cheapest_area     = rent_by_area.iloc[0]["postcode"]
most_expensive_area = rent_by_area.iloc[-1]["postcode"]

with ins1:
    st.markdown(f"""
    <div class='insight-card'>
        <div class='insight-title'>Market snapshot</div>
        <div class='insight-big'>{cheapest_area} to {most_expensive_area}</div>
        <div class='insight-copy'>
            The rent spread across selected areas shows clear neighbourhood
            segmentation rather than one uniform market.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ins2:
    st.markdown(f"""
    <div class='insight-card'>
        <div class='insight-title'>Portfolio story</div>
        <div class='insight-big'>Decision-support, not just charts</div>
        <div class='insight-copy'>
            This dashboard combines exploration, comparison, ranking, trend analysis,
            and a simple ML estimate in one product-style interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

with ins3:
    st.markdown(f"""
    <div class='insight-card'>
        <div class='insight-title'>Data note</div>
        <div class='insight-big'>Synthetic but realistic</div>
        <div class='insight-copy'>
            A controlled portfolio dataset — useful for demonstrating analytical
            thinking, UI design, and stakeholder-facing communication.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Export filtered data as CSV",
    data=csv,
    file_name="manchester_rentals_filtered.csv",
    mime="text/csv",
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "LIVE MAP",
    "RENT & YIELD",
    "RANKINGS",
    "TRENDS",
    "PREDICTOR",
])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1: MAP
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("""
    <p class='sec'>Interactive affordability map</p>
    <p class='sec-desc'>
        Explore postcode-level affordability spatially. Bubble size reflects the affordability score,
        while colour moves from premium / low-value areas toward stronger value zones.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='legend'>
        <div class='legend-item'><div class='dot' style='background:#00ff88;'></div>High affordability (70+)</div>
        <div class='legend-item'><div class='dot' style='background:#e8c547;'></div>Medium (40–70)</div>
        <div class='legend-item'><div class='dot' style='background:#c0392b;'></div>Low affordability (&lt;40)</div>
    </div>
    """, unsafe_allow_html=True)

    afford_df = compute_affordability_score(df)

    coords = {
        "M1":  (53.4808, -2.2426), "M2":  (53.4831, -2.2441),
        "M3":  (53.4851, -2.2534), "M4":  (53.4878, -2.2309),
        "M5":  (53.4740, -2.2785), "M6":  (53.4762, -2.2934),
        "M8":  (53.5042, -2.2312), "M11": (53.4749, -2.1712),
        "M12": (53.4598, -2.2051), "M13": (53.4613, -2.2181),
        "M14": (53.4479, -2.2202), "M15": (53.4659, -2.2496),
        "M16": (53.4516, -2.2708), "M20": (53.4121, -2.2290),
        "M21": (53.4359, -2.2681),
    }

    afford_df["lat"]       = afford_df["postcode"].map(lambda x: coords.get(x, (53.48, -2.24))[0])
    afford_df["lon"]       = afford_df["postcode"].map(lambda x: coords.get(x, (53.48, -2.24))[1])
    afford_df["bubble"]    = afford_df["affordability_score"].clip(lower=8) * 2.2
    afford_df["rent_fmt"]  = afford_df["avg_rent"].map(lambda x: f"£{x:,.0f}/mo")
    afford_df["score_fmt"] = afford_df["affordability_score"].map(lambda x: f"{x:.0f}/100")

    m1, m2 = st.columns([3, 1])

    with m1:
        fig_map = px.scatter_map(
            afford_df,
            lat="lat",
            lon="lon",
            size="bubble",
            color="affordability_score",
            color_continuous_scale=[
                [0.0, "#c0392b"],
                [0.35, "#c0392b"],
                [0.55, "#e8c547"],
                [0.75, "#00ff88"],
                [1.0,  "#00ff88"],
            ],
            hover_name="postcode",
            hover_data={
                "score_fmt": True,
                "rent_fmt": True,
                "avg_distance_to_city": ":.1f",
                "lat": False,
                "lon": False,
                "bubble": False,
                "affordability_score": False,
            },
            labels={
                "score_fmt": "Affordability",
                "rent_fmt": "Average rent",
                "avg_distance_to_city": "Distance to city (km)",
            },
            zoom=11,
            center={"lat": 53.475, "lon": -2.240},
            map_style="carto-darkmatter",
            height=600,
        )

        fig_map.update_layout(
            paper_bgcolor="#0d0d18",
            font=dict(color="#5a5870", family="Space Grotesk"),
            hoverlabel=dict(
                bgcolor="#12121f",
                bordercolor="#00ff88",
                font_color="#ffffff",
                font_family="Space Grotesk",
            ),
            coloraxis_colorbar=dict(
                title=dict(text="Score", font=dict(color="#5a5870")),
                tickfont=dict(color="#5a5870"),
                bgcolor="#0d0d18",
                bordercolor="rgba(255,255,255,0.06)",
            ),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with m2:
        st.markdown(
            "<p style='font-size:0.65rem; color:#3a3850;"
            " text-transform:uppercase; letter-spacing:0.1em;"
            " font-weight:700; margin-bottom:12px;'>"
            "AREA RANKING</p>",
            unsafe_allow_html=True
        )

        ranking_df = afford_df.sort_values(
            "affordability_score", ascending=False
        ).reset_index(drop=True)

        cards_html = "<div style='height:580px; overflow-y:auto; overflow-x:hidden; padding-right:6px;'>"

        for _, row in ranking_df.iterrows():
            score = float(row["affordability_score"])
            color = "#00ff88" if score >= 70 else "#e8c547" if score >= 40 else "#c0392b"
            bar_w = max(4, int(score))
            cards_html += f"""
            <div style='margin-bottom:6px; padding:8px 10px;
                border:1px solid rgba(255,255,255,0.06);
                background:rgba(255,255,255,0.015);
                border-radius:8px;'>
                <div style='display:flex; justify-content:space-between;
                     align-items:center; margin-bottom:5px;'>
                    <span style='font-size:0.8rem; color:#ffffff;
                         font-weight:700;'>{row['postcode']}</span>
                    <span style='font-size:0.72rem; color:{color};
                         font-weight:700;'>{score:.0f}/100</span>
                </div>
                <div style='background:rgba(255,255,255,0.04);
                     border-radius:999px; height:2px; overflow:hidden;'>
                    <div style='width:{bar_w}%; height:100%;
                         background:{color};'></div>
                </div>
                <div style='font-size:0.68rem; color:#5a5870; margin-top:4px;'>
                    Avg rent: £{row['avg_rent']:,.0f}/mo
                </div>
            </div>"""

        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2: RENT & YIELD
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("""
    <p class='sec'>Rent and yield comparison</p>
    <p class='sec-desc'>
        Compare what tenants pay and what investors might earn. This section is useful for showing
        both occupant affordability and investment attractiveness side by side.
    </p>
    """, unsafe_allow_html=True)

    rent_df  = compute_rent_by_postcode(df).sort_values("avg_rent", ascending=True)
    yield_df = compute_yield_by_postcode(df).sort_values("yield_percent", ascending=True)

    cr, cy = st.columns(2)

    with cr:
        st.markdown("""
        <div class='info-box'>
            <strong>Monthly rent</strong> reflects the average monthly cost paid by tenants in each postcode.
        </div>
        """, unsafe_allow_html=True)

        fig_r = px.bar(
            rent_df,
            x="postcode",
            y="avg_rent",
            color="avg_rent",
            color_continuous_scale=[[0, "#182033"], [0.55, "#2f5fa7"], [1, "#00ff88"]],
            text=rent_df["avg_rent"].map(lambda x: f"£{x:,.0f}"),
        )
        fig_r.update_traces(textposition="outside", textfont=dict(color="#ffffff", size=10))
        fig_r = chart(fig_r, "Average monthly rent by postcode", 390)
        fig_r.update_layout(coloraxis_showscale=False, yaxis_title="£ per month", xaxis_title="")
        st.plotly_chart(fig_r, use_container_width=True)

    with cy:
        st.markdown("""
        <div class='info-box'>
            <strong>Gross yield</strong> estimates annual rent as a percentage of property value.
        </div>
        """, unsafe_allow_html=True)

        fig_y = px.bar(
            yield_df,
            x="postcode",
            y="yield_percent",
            color="yield_percent",
            color_continuous_scale=[[0, "#24161a"], [0.55, "#8b5a20"], [1, "#00ff88"]],
            text=yield_df["yield_percent"].map(lambda x: f"{x:.1f}%"),
        )
        fig_y.update_traces(textposition="outside", textfont=dict(color="#ffffff", size=10))
        fig_y = chart(fig_y, "Gross yield by postcode", 390)
        fig_y.update_layout(coloraxis_showscale=False, yaxis_title="Yield %", xaxis_title="")
        st.plotly_chart(fig_y, use_container_width=True)

    st.markdown("""
    <p class='sec' style='margin-top:8px;'>Price versus rent positioning</p>
    <p class='sec-desc'>
        Each point represents a property observation. Larger markers indicate larger homes.
        This helps reveal whether higher prices are translating cleanly into higher rents.
    </p>
    """, unsafe_allow_html=True)

    fig_sc = px.scatter(
        df,
        x="avg_price",
        y="avg_rent",
        color="property_type",
        size="property_size_sqft",
        hover_data={"postcode": True, "avg_price": ":,.0f", "avg_rent": ":,.0f"},
        color_discrete_sequence=["#00ff88", "#63a6ff", "#e8c547", "#c0392b"],
    )
    fig_sc = chart(fig_sc, "Property price against monthly rent", 430)
    fig_sc.update_layout(
        xaxis_title="Property price (£)",
        yaxis_title="Monthly rent (£)",
        legend_title="Property type",
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 3: RANKINGS
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("""
    <p class='sec'>Area rankings by user profile</p>
    <p class='sec-desc'>
        Not every postcode is "best" for the same person. These rankings show how the same market can
        be reframed depending on whether the audience is student-led or professional-led.
    </p>
    """, unsafe_allow_html=True)

    best_df = compute_best_areas(df)

    cs, cp = st.columns(2)

    with cs:
        st.markdown("""
        <div style='background:rgba(0,255,136,0.04); border:1px solid rgba(0,255,136,0.12);
                    border-top:2px solid #00ff88; border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='font-family:Syne,sans-serif; font-size:0.95rem; font-weight:800; color:#00ff88;'>🎓 Best for students</div>
            <div style='font-size:0.8rem; color:#5a5870; margin-top:4px; line-height:1.6;'>
                Weighted on lower rent and shorter distance to university.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st_tbl = (
            best_df[["postcode", "avg_rent", "dist_to_uni", "student_score"]]
            .sort_values("student_score", ascending=False)
            .reset_index(drop=True)
        )
        st_tbl.index += 1
        st_tbl["avg_rent"]     = st_tbl["avg_rent"].map(lambda x: f"£{x:,.0f}/mo")
        st_tbl["dist_to_uni"]  = st_tbl["dist_to_uni"].map(lambda x: f"{x:.1f} km")
        st_tbl["student_score"] = st_tbl["student_score"].map(lambda x: f"{x:.0f}/100")
        st_tbl = st_tbl.rename(columns={
            "postcode": "Area",
            "avg_rent": "Monthly rent",
            "dist_to_uni": "To university",
            "student_score": "Score",
        })

        student_html = "<div style='background:#1f2021;" \
            "border-radius:6px;overflow:hidden;" \
            "border:1px solid rgba(255,255,255,0.06);'>" \
            "<table style='width:100%;border-collapse:collapse;" \
            "font-family:Space Grotesk,sans-serif;'>" \
            "<thead><tr style='border-bottom:1px solid " \
            "rgba(0,255,136,0.15);'>" \
            "<th style='padding:12px 16px;color:#00ff88;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>Area</th>" \
            "<th style='padding:12px 16px;color:#00ff88;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>Monthly Rent</th>" \
            "<th style='padding:12px 16px;color:#00ff88;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>To Uni</th>" \
            "<th style='padding:12px 16px;color:#00ff88;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:right;'>Score</th>" \
            "</tr></thead><tbody>"

        for i, (_, row) in enumerate(st_tbl.iterrows(), 1):
            bg = "rgba(255,255,255,0.015)" if i % 2 == 0 else "transparent"
            student_html += (
                "<tr style='background:" + bg + ";"
                "border-bottom:1px solid rgba(255,255,255,0.04);'>"
                "<td style='padding:13px 16px;color:#f1ffef;"
                "font-weight:700;font-size:0.88rem;'>"
                + str(row['Area']) +
                "</td>"
                "<td style='padding:13px 16px;color:#b9cbb9;"
                "font-size:0.84rem;font-family:monospace;'>"
                + str(row['Monthly rent']) +
                "</td>"
                "<td style='padding:13px 16px;color:#b9cbb9;"
                "font-size:0.84rem;'>"
                + str(row['To university']) +
                "</td>"
                "<td style='padding:13px 16px;color:#00ff88;"
                "font-weight:800;font-size:0.84rem;"
                "font-family:monospace;text-align:right;'>"
                + str(row['Score']) +
                "</td></tr>"
            )

        student_html += "</tbody></table></div>"
        st.markdown(student_html, unsafe_allow_html=True)

        selected_pc = st.selectbox(
            "Explore a postcode in detail",
            options=["Select..."] + sorted(df["postcode"].unique().tolist()),
            key="pc_detail"
        )

        if selected_pc != "Select...":
            pc = df[df["postcode"] == selected_pc]

            r = pc["avg_rent"].mean()
            p = pc["avg_price"].mean()
            y = pc["yield_percent"].mean()
            s = pc["property_size_sqft"].mean()
            dc = pc["distance_to_city_center_km"].mean()
            du = pc["distance_to_university_km"].mean()

            breakdown = ""
            for pt in sorted(pc["property_type"].unique()):
                subset = pc[pc["property_type"] == pt]
                if not subset.empty:
                    rent_val = subset["avg_rent"].mean()
                    pct = min(100, int(rent_val / pc["avg_rent"].max() * 100))
                    breakdown += (
                        "<div style='margin-bottom:10px;'>"
                        "<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
                        "<span style='font-size:0.72rem;color:#849585;"
                        "text-transform:uppercase;letter-spacing:0.08em;'>"
                        + pt +
                        "</span>"
                        "<span style='font-size:0.72rem;color:#00ff88;"
                        "font-weight:700;font-family:monospace;'>"
                        + f"£{rent_val:,.0f}" +
                        "</span></div>"
                        "<div style='background:rgba(255,255,255,0.06);"
                        "height:3px;border-radius:2px;'>"
                        "<div style='width:" + str(pct) + "%;height:100%;"
                        "background:#00ff88;border-radius:2px;'></div>"
                        "</div></div>"
                    )

            types_str = ", ".join(sorted(pc["property_type"].unique()))

            html = (
                "<div style='background:#1f2021;border:1px solid "
                "rgba(0,255,136,0.15);border-radius:8px;padding:28px;"
                "margin-top:16px;'>"

                "<div style='margin-bottom:24px;'>"
                "<div style='font-size:0.6rem;color:#00ff88;"
                "letter-spacing:0.2em;font-weight:700;"
                "text-transform:uppercase;margin-bottom:8px;'>"
                "HIGH DEMAND · POSTCODE: " + selected_pc +
                "</div>"
                "<div style='font-family:Syne,sans-serif;"
                "font-size:3rem;font-weight:800;color:#f1ffef;"
                "line-height:0.9;letter-spacing:-0.02em;'>"
                + selected_pc +
                "</div>"
                "<div style='font-size:0.85rem;color:#849585;"
                "margin-top:6px;letter-spacing:0.1em;'>"
                "GREATER MANCHESTER"
                "</div></div>"

                "<div style='display:grid;grid-template-columns:"
                "repeat(4,1fr);gap:1px;background:rgba(255,255,255,0.06);"
                "border-radius:4px;overflow:hidden;margin-bottom:24px;'>"

                "<div style='background:#1b1c1d;padding:16px 14px;'>"
                "<div style='font-size:0.55rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:6px;'>Avg Rent</div>"
                "<div style='font-family:Syne,sans-serif;font-size:1.4rem;"
                "font-weight:800;color:#f1ffef;line-height:1;'>"
                + f"£{r:,.0f}" +
                "</div><div style='font-size:0.6rem;color:#00ff88;"
                "margin-top:4px;font-family:monospace;'>PCM</div></div>"

                "<div style='background:#1b1c1d;padding:16px 14px;'>"
                "<div style='font-size:0.55rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:6px;'>Yield</div>"
                "<div style='font-family:Syne,sans-serif;font-size:1.4rem;"
                "font-weight:800;color:#00ff88;line-height:1;'>"
                + f"{y:.1f}%" +
                "</div><div style='font-size:0.6rem;color:#849585;"
                "margin-top:4px;font-family:monospace;'>GROSS</div></div>"

                "<div style='background:#1b1c1d;padding:16px 14px;'>"
                "<div style='font-size:0.55rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:6px;'>Avg Size</div>"
                "<div style='font-family:Syne,sans-serif;font-size:1.4rem;"
                "font-weight:800;color:#f1ffef;line-height:1;'>"
                + f"{s:.0f}" +
                "</div><div style='font-size:0.6rem;color:#849585;"
                "margin-top:4px;font-family:monospace;'>SQ FT</div></div>"

                "<div style='background:#1b1c1d;padding:16px 14px;'>"
                "<div style='font-size:0.55rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:6px;'>Avg Price</div>"
                "<div style='font-family:Syne,sans-serif;font-size:1.4rem;"
                "font-weight:800;color:#f1ffef;line-height:1;'>"
                + f"£{p/1000:.0f}k" +
                "</div><div style='font-size:0.6rem;color:#849585;"
                "margin-top:4px;font-family:monospace;'>PURCHASE</div></div>"

                "</div>"

                "<div style='display:grid;grid-template-columns:1fr 1fr;"
                "gap:16px;'>"

                "<div style='background:#121315;border-radius:4px;"
                "padding:16px;'>"
                "<div style='font-size:0.6rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:12px;font-weight:700;'>"
                "Rental Breakdown</div>"
                + breakdown +
                "</div>"

                "<div style='background:#121315;border-radius:4px;"
                "padding:16px;'>"
                "<div style='font-size:0.6rem;color:#849585;"
                "text-transform:uppercase;letter-spacing:0.14em;"
                "margin-bottom:12px;font-weight:700;'>"
                "Location Intel</div>"

                "<div style='display:flex;justify-content:space-between;"
                "padding:8px 0;border-bottom:1px solid "
                "rgba(255,255,255,0.04);'>"
                "<span style='font-size:0.75rem;color:#849585;'>"
                "Dist. to City</span>"
                "<span style='font-size:0.75rem;color:#f1ffef;"
                "font-weight:700;font-family:monospace;'>"
                + f"{dc:.1f} km" +
                "</span></div>"

                "<div style='display:flex;justify-content:space-between;"
                "padding:8px 0;border-bottom:1px solid "
                "rgba(255,255,255,0.04);'>"
                "<span style='font-size:0.75rem;color:#849585;'>"
                "Dist. to Uni</span>"
                "<span style='font-size:0.75rem;color:#f1ffef;"
                "font-weight:700;font-family:monospace;'>"
                + f"{du:.1f} km" +
                "</span></div>"

                "<div style='display:flex;justify-content:space-between;"
                "padding:8px 0;border-bottom:1px solid "
                "rgba(255,255,255,0.04);'>"
                "<span style='font-size:0.75rem;color:#849585;'>"
                "Avg Yield</span>"
                "<span style='font-size:0.75rem;color:#00ff88;"
                "font-weight:700;font-family:monospace;'>"
                + f"{y:.2f}%" +
                "</span></div>"

                "<div style='display:flex;justify-content:space-between;"
                "padding:8px 0;'>"
                "<span style='font-size:0.75rem;color:#849585;'>"
                "Property Types</span>"
                "<span style='font-size:0.75rem;color:#f1ffef;"
                "font-weight:700;font-family:monospace;'>"
                + types_str +
                "</span></div>"

                "</div></div></div>"
            )

            st.markdown(html, unsafe_allow_html=True)

    with cp:
        st.markdown("""
        <div style='background:rgba(99,166,255,0.04); border:1px solid rgba(99,166,255,0.12);
                    border-top:2px solid #63a6ff; border-radius:10px; padding:14px; margin-bottom:14px;'>
            <div style='font-family:Syne,sans-serif; font-size:0.95rem; font-weight:800; color:#63a6ff;'>💼 Best for professionals</div>
            <div style='font-size:0.8rem; color:#5a5870; margin-top:4px; line-height:1.6;'>
                Weighted on city-centre access and stronger rental yield potential.
            </div>
        </div>
        """, unsafe_allow_html=True)

        pr_tbl = (
            best_df[["postcode", "dist_to_city", "avg_yield", "professional_score"]]
            .sort_values("professional_score", ascending=False)
            .reset_index(drop=True)
        )
        pr_tbl.index += 1
        pr_tbl["dist_to_city"]       = pr_tbl["dist_to_city"].map(lambda x: f"{x:.1f} km")
        pr_tbl["avg_yield"]          = pr_tbl["avg_yield"].map(lambda x: f"{x:.1f}%")
        pr_tbl["professional_score"] = pr_tbl["professional_score"].map(lambda x: f"{x:.0f}/100")
        pr_tbl = pr_tbl.rename(columns={
            "postcode": "Area",
            "dist_to_city": "To city centre",
            "avg_yield": "Yield",
            "professional_score": "Score",
        })

        prof_html = "<div style='background:#1f2021;" \
            "border-radius:6px;overflow:hidden;" \
            "border:1px solid rgba(255,255,255,0.06);'>" \
            "<table style='width:100%;border-collapse:collapse;" \
            "font-family:Space Grotesk,sans-serif;'>" \
            "<thead><tr style='border-bottom:1px solid " \
            "rgba(74,158,255,0.15);'>" \
            "<th style='padding:12px 16px;color:#4a9eff;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>Area</th>" \
            "<th style='padding:12px 16px;color:#4a9eff;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>To City</th>" \
            "<th style='padding:12px 16px;color:#4a9eff;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:left;'>Yield</th>" \
            "<th style='padding:12px 16px;color:#4a9eff;" \
            "font-size:0.6rem;font-weight:700;" \
            "text-transform:uppercase;letter-spacing:0.14em;" \
            "text-align:right;'>Score</th>" \
            "</tr></thead><tbody>"

        for i, (_, row) in enumerate(pr_tbl.iterrows(), 1):
            bg = "rgba(255,255,255,0.015)" if i % 2 == 0 else "transparent"
            prof_html += (
                "<tr style='background:" + bg + ";"
                "border-bottom:1px solid rgba(255,255,255,0.04);'>"
                "<td style='padding:13px 16px;color:#f1ffef;"
                "font-weight:700;font-size:0.88rem;'>"
                + str(row['Area']) +
                "</td>"
                "<td style='padding:13px 16px;color:#b9cbb9;"
                "font-size:0.84rem;'>"
                + str(row['To city centre']) +
                "</td>"
                "<td style='padding:13px 16px;color:#b9cbb9;"
                "font-size:0.84rem;font-family:monospace;'>"
                + str(row['Yield']) +
                "</td>"
                "<td style='padding:13px 16px;color:#4a9eff;"
                "font-weight:800;font-size:0.84rem;"
                "font-family:monospace;text-align:right;'>"
                + str(row['Score']) +
                "</td></tr>"
            )

        prof_html += "</tbody></table></div>"
        st.markdown(prof_html, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    cs2, cp2 = st.columns(2)

    with cs2:
        stud_sorted = best_df.sort_values("student_score", ascending=False)
        fig_s = px.bar(
            stud_sorted,
            x="postcode",
            y="student_score",
            color="student_score",
            color_continuous_scale=[[0, "#14201b"], [1, "#00ff88"]],
            text=stud_sorted["student_score"].map(lambda x: f"{x:.0f}"),
        )
        fig_s.update_traces(textposition="outside", textfont=dict(color="#ffffff", size=10))
        fig_s = chart(fig_s, "Student suitability score", 330)
        fig_s.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Score")
        st.plotly_chart(fig_s, use_container_width=True)

    with cp2:
        prof_sorted = best_df.sort_values("professional_score", ascending=False)
        fig_p = px.bar(
            prof_sorted,
            x="postcode",
            y="professional_score",
            color="professional_score",
            color_continuous_scale=[[0, "#141d2c"], [1, "#63a6ff"]],
            text=prof_sorted["professional_score"].map(lambda x: f"{x:.0f}"),
        )
        fig_p.update_traces(textposition="outside", textfont=dict(color="#ffffff", size=10))
        fig_p = chart(fig_p, "Professional suitability score", 330)
        fig_p.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Score")
        st.plotly_chart(fig_p, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 4: TRENDS
# ──────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("""
    <p class='sec'>Rent trend and six-month forecast</p>
    <p class='sec-desc'>
        This view tracks average monthly rent over time and extends it using a simple linear trend.
        It is intentionally lightweight: good for directional portfolio storytelling rather than formal forecasting.
    </p>
    <div class='info-box'>
        <strong>Interpret carefully:</strong> the forecast is a straight-line extension of the historical trend.
        Real-world rents respond to supply, demand, seasonality, local policy, and macroeconomic factors not modelled here.
    </div>
    """, unsafe_allow_html=True)

    trend_df = compute_monthly_trend(df).sort_values("date").copy()
    trend_df["date_str"] = trend_df["date"].dt.strftime("%b %Y")
    trend_df["n"]        = np.arange(len(trend_df))

    fig_t = go.Figure()

    fig_t.add_trace(go.Scatter(
        x=trend_df["date_str"],
        y=trend_df["avg_rent"],
        mode="lines+markers",
        name="Actual",
        line=dict(color="#00ff88", width=2.5),
        marker=dict(size=7, color="#00ff88", line=dict(color="#0d0d18", width=2)),
    ))

    if len(trend_df) >= 3:
        mdl = LinearRegression()
        mdl.fit(trend_df["n"].values.reshape(-1, 1), trend_df["avg_rent"].values)

        fut_n       = np.arange(len(trend_df), len(trend_df) + 6)
        fut_y       = mdl.predict(fut_n.reshape(-1, 1))
        last        = pd.Timestamp(trend_df["date"].max())
        fut_dates_dt = pd.date_range(last + pd.DateOffset(months=1), periods=6, freq="MS")
        fut_dates   = fut_dates_dt.strftime("%b %Y").tolist()

        line_x = [trend_df["date_str"].iloc[-1]] + fut_dates
        line_y = [trend_df["avg_rent"].iloc[-1]] + fut_y.tolist()

        fig_t.add_trace(go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines+markers",
            name="Forecast",
            line=dict(color="#63a6ff", width=2.2, dash="dash"),
            marker=dict(size=5, color="#63a6ff"),
        ))

        upper = [v * 1.04 for v in fut_y]
        lower = [v * 0.96 for v in fut_y]

        fig_t.add_trace(go.Scatter(
            x=fut_dates + fut_dates[::-1],
            y=upper + lower[::-1],
            fill="toself",
            fillcolor="rgba(99,166,255,0.10)",
            line=dict(color="rgba(0,0,0,0)"),
            name="±4% band",
            hoverinfo="skip",
            showlegend=True,
        ))

    fig_t.update_layout(
        paper_bgcolor="#0d0d18",
        plot_bgcolor="#0d0d18",
        font=dict(color="#5a5870", family="Space Grotesk"),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.03)",
            tickangle=-40,
            title="Month",
            title_font=dict(color="#5a5870"),
            tickfont=dict(color="#5a5870"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.03)",
            title="Average monthly rent (£)",
            title_font=dict(color="#5a5870"),
            tickfont=dict(color="#5a5870"),
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#5a5870")),
        margin=dict(l=16, r=16, t=16, b=16),
        hoverlabel=dict(
            bgcolor="#12121f",
            bordercolor="#00ff88",
            font_color="#ffffff",
            font_family="Space Grotesk",
        ),
        height=470,
    )
    st.plotly_chart(fig_t, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 5: MODEL
# ──────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("""
    <p class='sec'>Rent predictor</p>
    <p class='sec-desc'>
        This machine learning view estimates expected rent from property characteristics in the currently
        filtered market. It is simple, transparent, and useful for explaining predictive logic to non-technical viewers.
    </p>
    <div class='info-box'>
        <strong>Plain-English explanation:</strong> the model learns patterns from historical examples —
        for example, larger homes or better-connected postcodes often command higher rents — and then
        uses those patterns to estimate likely rent for similar properties.
    </div>
    """, unsafe_allow_html=True)

    run_m = st.checkbox("▶ Train and run the model", value=False)

    if run_m:
        if len(df) < 10:
            st.warning("Not enough data to train the model reliably — widen the filters and try again.")
        else:
            with st.spinner("Training model on filtered data…"):
                res = run_regression(df)

            m1, m2 = st.columns(2)
            m1.metric(
                "Average prediction error (MAE)",
                f"£{res['mae']:,.0f}",
                help="Typical £ difference between the prediction and the actual rent.",
            )
            m2.metric(
                "Model fit (R²)",
                f"{res['r2']:.3f} / 1.000",
                help="Closer to 1 means the model explains more of the variation in rent.",
            )

            st.markdown("""
            <div class='info-box' style='margin-top:16px;'>
                <strong>How to read the results:</strong><br>
                A lower MAE is better because the model is missing the true rent by fewer pounds on average.
                A higher R² suggests stronger pattern capture. Since this is a synthetic dataset, treat the output
                as a demonstration of methodology and communication rather than a market-grade production model.
            </div>
            """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    <div class='footer-brand'>Manchester Rental Intelligence</div>
    Built by <span style='color:#00ff88; font-weight:700;'>Sajan Mathew</span> · MSc Data Science · Manchester Metropolitan University<br>
    Synthetic 2021–2025 dataset · Portfolio concept inspired by spatial analytics, housing dashboards, and modern product-style design<br>
    <a href='https://github.com/privsmathewz'>GitHub</a> ·
    <a href='https://linkedin.com/in/sajan-mathew-ab0965257'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple

from analysis_utils import load_data, prepare_features, train_regression_model
from styles import load_css
from rankings import compute_rankings, compute_pulse, rec_reasons
from charts import dark_layout, insight
from predictor import render_predictor
from tabs.overview import render_overview
from tabs.rankings import render_rankings
from tabs.map import render_map
from tabs.trends import render_trends
from tabs.about import render_about

st.set_page_config(
    page_title="Manchester Rental Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(load_css(), unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
PERSONA_TYPES: Dict[str, List[str]] = {
    'Student':      ['HMO', '1-bed'],
    'Professional': ['1-bed'],
    'Investor':     ['Studio', '1-bed', 'HMO'],
    'Explorer':     ['Studio', '1-bed', 'HMO'],
}
PERSONA_COLOUR: Dict[str, str] = {
    'Student':      '#4f9cf9',
    'Professional': '#f97316',
    'Investor':     '#a855f7',
    'Explorer':     '#00ff88',
}


@st.cache_data
def load_dataset() -> pd.DataFrame:
    return load_data('data/sample_rental_data_small.csv')


@st.cache_resource
def get_model():
    df = load_data('data/sample_rental_data_small.csv')
    X, y, preprocessor = prepare_features(df)
    model, metrics = train_regression_model(X, y)
    return model, metrics, preprocessor


# ── Data ───────────────────────────────────────────────────────────────────────
data = load_dataset()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">GREATER MANCHESTER · LIVE RENTAL INTELLIGENCE</div>
  <div class="hero-headline">FIND YOUR PLACE.</div>
  <p class="hero-sub">Live rental intelligence across Greater Manchester.
  Compare postcodes by affordability, yield, demand, and 6-month forecast trend.</p>
</div>
""", unsafe_allow_html=True)

# ── Top Filter Bar ─────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="topbar-wrap">', unsafe_allow_html=True)
    col_p, col_pc, col_type, col_date = st.columns([1.5, 2, 2, 2])
    with col_p:
        st.markdown('<div class="sidebar-lbl">PERSONA</div>', unsafe_allow_html=True)
        persona = st.radio(
            "persona",
            options=['Student', 'Professional', 'Investor', 'Explorer'],
            horizontal=True,
            label_visibility='collapsed',
            key='persona',
        )
        pc_hex = PERSONA_COLOUR[persona]
        r, g_c, b = int(pc_hex[1:3], 16), int(pc_hex[3:5], 16), int(pc_hex[5:7], 16)
        st.markdown(
            f'<div class="persona-badge" style="background:rgba({r},{g_c},{b},0.12);'
            f'border-color:{pc_hex};color:{pc_hex};">Active: {persona}</div>',
            unsafe_allow_html=True,
        )
    with col_pc:
        all_postcodes = sorted(data['postcode'].unique())
        selected_postcodes = st.multiselect(
            "Postcodes", options=all_postcodes, default=all_postcodes,
        )
    with col_type:
        all_types = sorted(data['property_type'].unique())
        def_types = [t for t in PERSONA_TYPES[persona] if t in all_types]
        selected_types = st.multiselect(
            "Property types", options=all_types,
            default=def_types if def_types else all_types,
            key=f'types_{persona}',
        )
    with col_date:
        min_date = data['date'].min().to_timestamp().date()
        max_date = data['date'].max().to_timestamp().date()
        date_range = st.slider(
            "Date range", min_value=min_date, max_value=max_date,
            value=(min_date, max_date), format="MMM YYYY",
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Filter ─────────────────────────────────────────────────────────────────────
mask = (
    data['postcode'].isin(selected_postcodes)
    & data['property_type'].isin(selected_types)
    & (data['date'] >= pd.Period(date_range[0].strftime('%Y-%m'), freq='M'))
    & (data['date'] <= pd.Period(date_range[1].strftime('%Y-%m'), freq='M'))
)
filtered = data[mask].copy()

if filtered.empty:
    st.warning("No data matches your current filters. Try adjusting postcodes, property types, or date range.")
    st.stop()

model, metrics, preprocessor = get_model()
pulse    = compute_pulse(data)
ranked   = compute_rankings(filtered, persona)

t = pulse['trend']
trend_class = 'pulse-up' if t[0] == 'Rising' else 'pulse-flat'

# ── Market Pulse ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pulse-grid">
  <div class="pulse-card">
    <div class="pulse-label">BEST FOR STUDENTS</div>
    <div class="pulse-value">{pulse['student']}</div>
    <div class="pulse-sub">Top-ranked student zone</div>
  </div>
  <div class="pulse-card">
    <div class="pulse-label">BEST YIELD</div>
    <div class="pulse-value">{pulse['yield_']}</div>
    <div class="pulse-sub">Highest gross yield</div>
  </div>
  <div class="pulse-card">
    <div class="pulse-label">BEST VALUE</div>
    <div class="pulse-value">{pulse['value']}</div>
    <div class="pulse-sub">Lowest average rent</div>
  </div>
  <div class="pulse-card">
    <div class="pulse-label">MARKET TREND</div>
    <div class="pulse-value {trend_class}">{t[0]}</div>
    <div class="pulse-sub">{t[1]}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
avg_rent_f, avg_yield_f = filtered['avg_rent'].mean(), filtered['yield_percent'].mean()
avg_rent_all, avg_yield_all = data['avg_rent'].mean(), data['yield_percent'].mean()
_yld_by_pc = filtered.groupby('postcode')['yield_percent'].mean()
top_yield_pc, top_yield_val, n_pc = _yld_by_pc.idxmax(), _yld_by_pc.max(), filtered['postcode'].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Monthly Rent",   f"£{avg_rent_f:,.0f}",
          delta=f"{'↑' if avg_rent_f >= avg_rent_all else '↓'} vs £{avg_rent_all:,.0f} market")
c2.metric("Avg Gross Yield",    f"{avg_yield_f:.1f}%",
          delta=f"{'↑' if avg_yield_f >= avg_yield_all else '↓'} vs {avg_yield_all:.1f}% market")
c3.metric("Top Yield Postcode", top_yield_pc, delta=f"{top_yield_val:.1f}% gross")
c4.metric("Postcodes in View",  str(n_pc),    delta=f"{len(filtered):,} data points")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_ov, tab_rank, tab_map, tab_pred, tab_trend, tab_about = st.tabs(
    ["Overview", "Rankings", "Live Map", "Predictor", "Trends", "About"]
)
with tab_ov:    render_overview(filtered)
with tab_rank:  render_rankings(ranked, filtered, data, persona)
with tab_map:   render_map(filtered, ranked)
with tab_pred:  render_predictor(filtered, data, model, metrics, preprocessor)
with tab_trend: render_trends(filtered)
with tab_about: render_about()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
  <div class="footer-col">Manchester Rental Intelligence — Built by Sajan Mathew</div>
  <div class="footer-col footer-mid">manchester-homes.streamlit.app</div>
  <div class="footer-col">
    <a href="https://github.com/privsmathewz" target="_blank">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/sajanmathew" target="_blank">LinkedIn</a>
  </div>
</div>
""", unsafe_allow_html=True)

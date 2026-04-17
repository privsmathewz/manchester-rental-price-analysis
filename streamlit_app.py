import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple

from analysis_utils import (
    load_data,
    compute_average_rent_by_postcode,
    compute_average_yield_by_postcode,
    compute_monthly_trend,
    prepare_features,
    train_regression_model,
)

st.set_page_config(
    page_title="Manchester Rental Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
  --bg:          #060810;
  --bg-2:        #090c17;
  --bg-card:     rgba(255,255,255,0.03);
  --green:       #00ff88;
  --green-dim:   rgba(0,255,136,0.12);
  --green-glow:  rgba(0,255,136,0.35);
  --green-line:  rgba(0,255,136,0.6);
  --border:      rgba(255,255,255,0.06);
  --text:        #dde2ef;
  --text-dim:    rgba(221,226,239,0.45);
  --radius:      14px;
}

@keyframes fadeInUp {
  from { opacity:0; transform:translateY(18px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 0 rgba(0,255,136,0); }
  50%     { box-shadow: 0 0 28px rgba(0,255,136,0.14); }
}
@keyframes borderShimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}

.stApp {
  background: var(--bg) !important;
  font-family: 'Space Grotesk', sans-serif !important;
  color: var(--text) !important;
}

.main .block-container {
  padding: 2.5rem 3.5rem 4rem !important;
  max-width: 1480px !important;
}

h1 {
  font-family: 'Syne', sans-serif !important;
  font-size: clamp(2.2rem,4vw,3.6rem) !important;
  font-weight: 800 !important;
  background: linear-gradient(118deg,#ffffff 20%,#b0ffd8 55%,var(--green) 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}

h2 {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.3rem !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  padding-left: 1rem !important;
  border-left: 3px solid var(--green) !important;
  margin-top: 2rem !important;
  margin-bottom: 1rem !important;
}

h3 {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  color: #ffffff !important;
}

p, li, label, .stMarkdown {
  font-family: 'Space Grotesk', sans-serif !important;
  color: var(--text) !important;
  line-height: 1.65 !important;
  font-size: 14px !important;
}

[data-testid="stMetric"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 20px !important;
  transition: transform 0.28s ease, box-shadow 0.28s ease !important;
  min-height: 110px !important;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-3px) !important;
  border-color: rgba(0,255,136,0.22) !important;
  box-shadow: 0 0 24px var(--green-glow) !important;
}
[data-testid="stMetricLabel"] > div {
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: #6b7280 !important;
}
[data-testid="stMetricValue"] > div {
  font-family: 'Syne', sans-serif !important;
  font-size: 28px !important;
  font-weight: 700 !important;
  color: var(--green) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  padding: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  color: var(--text-dim) !important;
  background: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  padding: 0.8rem 1.6rem !important;
  margin-bottom: -1px !important;
  border-radius: 6px 6px 0 0 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--green) !important;
  border-bottom: 2px solid var(--green) !important;
  background: var(--green-dim) !important;
}

[data-testid="stSidebar"] {
  background: var(--bg-2) !important;
  border-right: 1px solid var(--border) !important;
}

[data-baseweb="select"] > div {
  background: rgba(255,255,255,0.04) !important;
  border-color: var(--border) !important;
  border-radius: 8px !important;
}

.stButton > button {
  font-family: 'Space Grotesk', sans-serif !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  border: 1px solid var(--border) !important;
  background: var(--bg-card) !important;
  color: var(--text) !important;
  transition: all 0.25s ease !important;
}
.stButton > button:hover {
  border-color: var(--green) !important;
  color: var(--green) !important;
  box-shadow: 0 0 14px var(--green-dim) !important;
}

hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--green); }

.hero-wrap {
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%);
  border-radius: 16px;
  padding: 48px 40px 36px;
  margin-bottom: 8px;
  border: 1px solid rgba(255,255,255,0.05);
}
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 0.2em;
  color: #00ff88;
  text-transform: uppercase;
  margin-bottom: 14px;
  font-weight: 600;
}
.hero-headline {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.8rem,5.5vw,4.5rem);
  font-weight: 800;
  background: linear-gradient(118deg,#ffffff 20%,#b0ffd8 55%,#00ff88 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.0;
  margin-bottom: 16px;
  letter-spacing: -0.03em;
}
.hero-sub {
  font-size: 16px;
  color: #c4c9e2;
  max-width: 680px;
  line-height: 1.65;
  margin: 0;
}

.pulse-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin: 20px 0 28px;
}
.pulse-card {
  background: #1a1a2e;
  border: 1px solid #2a2a5a;
  border-radius: 12px;
  padding: 18px 20px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.pulse-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00ff88, transparent);
}
.pulse-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,255,136,0.1);
}
.pulse-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #00ff88;
  text-transform: uppercase;
  margin-bottom: 7px;
}
.pulse-value {
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 3px;
  word-break: break-word;
}
.pulse-sub { font-size: 11px; color: #6b7280; }
.pulse-up   { color: #00ff88 !important; }
.pulse-flat { color: #f59e0b !important; }

.section-wrap {
  background: #0d0d1a;
  border: 1px solid #1e1e3a;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.insight {
  background: #111128;
  border-left: 3px solid #00ff88;
  border-radius: 0 8px 8px 0;
  padding: 12px 16px;
  margin: 10px 0 18px;
  font-size: 14px;
  color: #dde2ef;
  line-height: 1.6;
}
.insight-icon { color: #00ff88; margin-right: 6px; }

.rec-card {
  background: linear-gradient(135deg, #0d0d1a 0%, #0f1a0f 100%);
  border: 1px solid #00ff88;
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: 0 0 40px rgba(0,255,136,0.07);
}
.rec-postcode {
  font-family: 'Syne', sans-serif;
  font-size: 58px;
  font-weight: 800;
  color: #00ff88;
  line-height: 1;
  margin-bottom: 2px;
}
.rec-title {
  font-size: 12px;
  letter-spacing: 0.12em;
  color: #6b7280;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.rec-reason {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 14px;
  color: #dde2ef;
  line-height: 1.55;
}
.rec-reason:last-child { border-bottom: none; }
.rec-bullet { color: #00ff88; font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.rec-badge {
  display: inline-block;
  background: rgba(0,255,136,0.1);
  border: 1px solid rgba(0,255,136,0.3);
  color: #00ff88;
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}

.rank-row {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: background 0.2s;
}
.rank-row:hover { background: rgba(0,255,136,0.03); }
.rank-row-1 { border-color: rgba(0,255,136,0.25) !important; }
.rank-num {
  font-family: 'Syne', sans-serif;
  font-size: 26px;
  font-weight: 800;
  color: rgba(221,226,239,0.13);
  width: 32px;
  flex-shrink: 0;
  text-align: center;
}
.rank-num-1 { color: #00ff88 !important; }
.rank-pc {
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  min-width: 52px;
}
.rank-stats { display: flex; gap: 20px; flex: 1; flex-wrap: wrap; }
.rank-stat { display: flex; flex-direction: column; }
.rank-stat-lbl { font-size: 10px; color: #6b7280; letter-spacing: 0.1em; text-transform: uppercase; }
.rank-stat-val { font-size: 13px; font-weight: 600; color: #dde2ef; }
.rank-score-badge {
  background: rgba(0,255,136,0.1);
  color: #00ff88;
  border: 1px solid rgba(0,255,136,0.25);
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 11px;
  font-weight: 700;
}

.pred-in-card {
  background: #0d0d1a;
  border: 1px solid #00ff88;
  border-radius: 16px;
  padding: 24px 28px;
}
.pred-in-title {
  font-family: 'Syne', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #00ff88;
  text-transform: uppercase;
  margin-bottom: 20px;
}
.pred-out-card {
  background: linear-gradient(135deg, #0a1a10 0%, #0d0d1a 100%);
  border: 1px solid #00ff88;
  border-radius: 16px;
  padding: 32px 28px;
  text-align: center;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.pred-out-label { font-size: 11px; letter-spacing: 0.18em; color: #6b7280; text-transform: uppercase; margin-bottom: 8px; }
.pred-out-value { font-family: 'Syne', sans-serif; font-size: 60px; font-weight: 800; color: #00ff88; line-height: 1; margin-bottom: 6px; }
.pred-out-range { font-size: 14px; color: #a0aec0; margin-bottom: 16px; }
.pred-out-cmp { background: rgba(0,255,136,0.08); border-radius: 8px; padding: 10px 16px; font-size: 14px; color: #00ff88; margin-bottom: 16px; }
.pred-out-note { font-size: 11px; color: #6b7280; line-height: 1.65; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.05); }
.pred-out-warn { font-size: 11px; color: #f59e0b; margin-top: 6px; }
.pred-empty { color: rgba(221,226,239,0.25); font-size: 14px; text-align: center; padding: 40px 20px; }
.pred-btn button {
  background: #00ff88 !important;
  color: #000 !important;
  border: none !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  width: 100% !important;
  border-radius: 8px !important;
  padding: 0.65rem 1.5rem !important;
}
.pred-btn button:hover { background: #00cc6a !important; box-shadow: 0 0 20px rgba(0,255,136,0.3) !important; }

.map-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
}
.map-card:hover { background: rgba(0,255,136,0.04); }
.map-card-pc { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #fff; }
.map-card-stats { font-size: 12px; color: #a0aec0; margin-top: 4px; }
.map-rank-badge {
  float: right;
  background: rgba(0,255,136,0.1);
  border: 1px solid rgba(0,255,136,0.25);
  color: #00ff88;
  border-radius: 6px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 700;
}

.sidebar-logo { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; color: #00ff88; padding: 4px 0 12px; }
.sidebar-lbl { font-size: 10px; font-weight: 700; letter-spacing: 0.18em; color: rgba(221,226,239,0.3); text-transform: uppercase; margin-bottom: 6px; }
.persona-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; border: 1px solid; font-size: 12px; font-weight: 600; margin-top: 8px; }
.sidebar-footer { font-size: 11px; color: rgba(221,226,239,0.25); line-height: 1.65; padding-top: 8px; }

.page-footer {
  border-top: 1px solid #00ff88;
  margin-top: 60px;
  padding: 20px 0 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}
.footer-col { font-size: 13px; color: #6b7280; }
.footer-col a { color: #6b7280; text-decoration: none; }
.footer-col a:hover { color: #00ff88; }
.footer-mid { font-weight: 600; }

@media (max-width: 768px) {
  .main .block-container { padding: 1.5rem 1rem 3rem !important; }
  .pulse-grid { grid-template-columns: repeat(2,1fr); }
  .hero-wrap  { padding: 28px 18px 22px; }
  .hero-headline { font-size: 2.4rem; }
  .rec-postcode  { font-size: 38px; }
  .pred-out-value { font-size: 40px; }
  .rank-stats { flex-direction: column; gap: 6px; }
  .page-footer { flex-direction: column; text-align: center; }
  .pred-in-card, .pred-out-card { padding: 18px; }
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.topbar-wrap {
  background: #0d0d1a;
  border: 1px solid #1e1e3a;
  border-radius: 12px;
  padding: 16px 20px 8px;
  margin: 16px 0 20px;
}
</style>
""", unsafe_allow_html=True)


POSTCODE_COORDS: Dict[str, Tuple[float, float]] = {
    'M1':  (53.476, -2.230),
    'M3':  (53.484, -2.249),
    'M5':  (53.473, -2.273),
    'M13': (53.461, -2.209),
    'M14': (53.449, -2.220),
}
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


def _norm(s: pd.Series) -> pd.Series:
    mn, mx = s.min(), s.max()
    return pd.Series([0.5] * len(s), index=s.index) if mx == mn else (s - mn) / (mx - mn)


def _norm_inv(s: pd.Series) -> pd.Series:
    return 1 - _norm(s)


def compute_rankings(df: pd.DataFrame, persona: str) -> pd.DataFrame:
    g = df.groupby('postcode').agg(
        avg_rent=('avg_rent', 'mean'),
        avg_price=('avg_price', 'mean'),
        yield_pct=('yield_percent', 'mean'),
        dist_city=('distance_to_city_center_km', 'mean'),
        dist_uni=('distance_to_university_km', 'mean'),
    ).reset_index()
    if persona == 'Student':
        g['score'] = (_norm_inv(g['avg_rent']) * 0.40
                      + _norm_inv(g['dist_uni']) * 0.40
                      + _norm_inv(g['dist_city']) * 0.20)
    elif persona == 'Professional':
        g['score'] = (_norm_inv(g['dist_city']) * 0.50
                      + _norm_inv(g['avg_rent']) * 0.30
                      + _norm(g['yield_pct']) * 0.20)
    elif persona == 'Investor':
        g['score'] = (_norm(g['yield_pct']) * 0.60
                      + _norm_inv(g['avg_price']) * 0.40)
    else:
        g['score'] = (_norm(g['yield_pct']) * 0.25
                      + _norm_inv(g['avg_rent']) * 0.25
                      + _norm_inv(g['dist_city']) * 0.25
                      + _norm_inv(g['dist_uni']) * 0.25)
    g['rank'] = g['score'].rank(ascending=False).astype(int)
    return g.sort_values('rank').reset_index(drop=True)


def compute_pulse(df: pd.DataFrame) -> Dict:
    hmo = df[df['property_type'] == 'HMO'] if 'HMO' in df['property_type'].values else df
    sg = hmo.groupby('postcode').agg(
        r=('avg_rent', 'mean'), u=('distance_to_university_km', 'mean')
    ).reset_index()
    sg['s'] = _norm_inv(sg['r']) * 0.5 + _norm_inv(sg['u']) * 0.5
    best_student = sg.loc[sg['s'].idxmax(), 'postcode']
    yg = df.groupby('postcode')['yield_percent'].mean().reset_index()
    byr = yg.loc[yg['yield_percent'].idxmax()]
    best_yield = f"{byr['postcode']} ({byr['yield_percent']:.1f}%)"
    rg = df.groupby('postcode')['avg_rent'].mean().reset_index()
    bvr = rg.loc[rg['avg_rent'].idxmin()]
    best_value = f"{bvr['postcode']} (£{bvr['avg_rent']:.0f}/mo)"
    monthly = compute_monthly_trend(df).sort_values('date')
    if len(monthly) >= 2:
        v = monthly.tail(2)['avg_rent_mean'].values
        rising = v[-1] > v[-2]
        pct = abs((v[-1] - v[-2]) / v[-2] * 100) if v[-2] else 0
        trend = ('Rising', f'+{pct:.1f}%') if rising else ('Stable', f'{pct:.1f}% change')
    else:
        trend = ('Stable', '')
    return dict(student=best_student, yield_=best_yield, value=best_value, trend=trend)


def rec_reasons(pc: str, ranked: pd.DataFrame, full: pd.DataFrame, persona: str) -> List[str]:
    row = ranked[ranked['postcode'] == pc].iloc[0]
    mar = full['avg_rent'].mean()
    may = full['yield_percent'].mean()
    out = []
    if row['avg_rent'] < mar * 0.96:
        pct = (mar - row['avg_rent']) / mar * 100
        out.append(f"Average rent £{row['avg_rent']:.0f}/mo — {pct:.0f}% below the market average")
    if row['yield_pct'] > may * 1.02:
        out.append(f"Above-average gross yield at {row['yield_pct']:.1f}% — strong return profile")
    if persona in ('Student', 'Explorer') and row['dist_uni'] <= ranked['dist_uni'].quantile(0.4):
        out.append(f"Good university access at {row['dist_uni']:.1f}km — ideal for student demand")
    if persona in ('Professional', 'Explorer') and row['dist_city'] == ranked['dist_city'].min():
        out.append(f"Closest to city centre at {row['dist_city']:.1f}km — high professional demand")
    if persona == 'Investor' and row['avg_price'] < ranked['avg_price'].median():
        out.append(f"Lower acquisition cost vs peers at £{row['avg_price']:,.0f} — stronger capital efficiency")
    if not out:
        out.append(f"Strongest composite score across rent, yield, and location for {persona} profile")
        out.append(f"Yield {row['yield_pct']:.1f}% · Avg rent £{row['avg_rent']:.0f}/mo · City {row['dist_city']:.1f}km")
    return out[:3]


def insight(text: str) -> None:
    st.markdown(
        f'<div class="insight"><span class="insight-icon">◈</span>{text}</div>',
        unsafe_allow_html=True,
    )


def dark_layout(fig: go.Figure, title: str = '', height: int = 370) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color='#dde2ef'), x=0, xanchor='left'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,13,26,0.8)',
        font=dict(family='Space Grotesk, sans-serif', color='#dde2ef', size=12),
        height=height,
        margin=dict(l=40, r=30, t=50, b=40),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.08)', font=dict(size=11)),
    )
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)',
                     tickfont=dict(size=11, color='#a0aec0'))
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.08)',
                     tickfont=dict(size=11, color='#a0aec0'))
    return fig


# ── Data ──────────────────────────────────────────────────────────────────────
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
            "Date range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="MMM YYYY",
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
    st.warning("No data for current filters — adjust postcodes, types, or date range.")
    st.stop()

model, metrics, preprocessor = get_model()
pulse = compute_pulse(data)
ranked = compute_rankings(filtered, persona)

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
avg_rent_f   = filtered['avg_rent'].mean()
avg_yield_f  = filtered['yield_percent'].mean()
avg_rent_all = data['avg_rent'].mean()
avg_yield_all= data['yield_percent'].mean()
top_yield_pc = filtered.groupby('postcode')['yield_percent'].mean().idxmax()
top_yield_val= filtered.groupby('postcode')['yield_percent'].mean().max()
n_pc = filtered['postcode'].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Monthly Rent",    f"£{avg_rent_f:,.0f}",
          delta=f"{'↑' if avg_rent_f >= avg_rent_all else '↓'} vs £{avg_rent_all:,.0f} market")
c2.metric("Avg Gross Yield",     f"{avg_yield_f:.1f}%",
          delta=f"{'↑' if avg_yield_f >= avg_yield_all else '↓'} vs {avg_yield_all:.1f}% market")
c3.metric("Top Yield Postcode",  top_yield_pc, delta=f"{top_yield_val:.1f}% gross")
c4.metric("Postcodes in View",   str(n_pc),    delta=f"{len(filtered):,} data points")


# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_ov, tab_rank, tab_map, tab_pred, tab_trend = st.tabs([
    "Overview", "Rankings", "Live Map", "Predictor", "Trends",
])


# ═══════════════════════════════ OVERVIEW ═════════════════════════════════════
with tab_ov:
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Average Rent by Postcode")
    avg_rent_df = compute_average_rent_by_postcode(filtered)
    top_pc  = avg_rent_df.iloc[0]['postcode']
    bot_pc  = avg_rent_df.iloc[-1]['postcode']
    gap     = avg_rent_df.iloc[0]['avg_rent_mean'] - avg_rent_df.iloc[-1]['avg_rent_mean']
    insight(f"{top_pc} commands the highest average rent at £{avg_rent_df.iloc[0]['avg_rent_mean']:,.0f}/mo, "
            f"while {bot_pc} offers the best affordability at £{avg_rent_df.iloc[-1]['avg_rent_mean']:,.0f}/mo "
            f"— a £{gap:,.0f}/mo gap.")
    fig_rent = px.bar(avg_rent_df, x='postcode', y='avg_rent_mean',
                      color='avg_rent_mean',
                      color_continuous_scale=[(0,'#2a2a5a'),(0.5,'#4f9cf9'),(1,'#00ff88')],
                      labels={'avg_rent_mean':'Avg Rent (£)','postcode':'Postcode'},
                      custom_data=['postcode','avg_rent_mean'])
    fig_rent.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Avg Rent: £%{customdata[1]:,.0f}/mo<extra></extra>',
                           marker_line_width=0)
    fig_rent.update_coloraxes(showscale=False)
    dark_layout(fig_rent)
    st.plotly_chart(fig_rent, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Gross Yield by Postcode")
    avg_yield_df = compute_average_yield_by_postcode(filtered)
    hy_pc  = avg_yield_df.iloc[0]['postcode']
    hy_val = avg_yield_df.iloc[0]['yield_percent_mean']
    ly_pc  = avg_yield_df.iloc[-1]['postcode']
    insight(f"{hy_pc} leads return potential at {hy_val:.1f}% gross yield — "
            f"investors targeting capital efficiency should prioritise this zone over {ly_pc}.")
    fig_yield = px.bar(avg_yield_df, x='postcode', y='yield_percent_mean',
                       color='yield_percent_mean',
                       color_continuous_scale=[(0,'#1a1a3e'),(0.5,'#a855f7'),(1,'#00ff88')],
                       labels={'yield_percent_mean':'Avg Yield (%)','postcode':'Postcode'},
                       custom_data=['postcode','yield_percent_mean'])
    fig_yield.update_traces(hovertemplate='<b>%{customdata[0]}</b><br>Yield: %{customdata[1]:.2f}%<extra></extra>',
                            marker_line_width=0)
    fig_yield.update_coloraxes(showscale=False)
    dark_layout(fig_yield)
    st.plotly_chart(fig_yield, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Rent Distribution")
        insight("Spread shows how rent varies within each postcode across property types.")
        fig_box = px.box(filtered, x='postcode', y='avg_rent', color='postcode',
                         color_discrete_sequence=['#4f9cf9','#00ff88','#a855f7','#f97316','#f43f5e'],
                         labels={'avg_rent':'Avg Rent (£)','postcode':'Postcode'})
        fig_box.update_traces(hovertemplate='<b>%{x}</b><br>Rent: £%{y:,.0f}/mo<extra></extra>')
        dark_layout(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Yield vs Avg Price")
        insight("Higher-yielding postcodes are often lower-price entry points — ideal for investors.")
        agg = filtered.groupby('postcode').agg(
            avg_price=('avg_price','mean'), yield_pct=('yield_percent','mean'), avg_rent=('avg_rent','mean')
        ).reset_index()
        fig_scatter = px.scatter(agg, x='avg_price', y='yield_pct', text='postcode',
                                 size='avg_rent', size_max=28, color='yield_pct',
                                 color_continuous_scale=[(0,'#2a2a5a'),(1,'#00ff88')],
                                 labels={'avg_price':'Avg Price (£)','yield_pct':'Yield (%)'},
                                 custom_data=['postcode','avg_price','yield_pct','avg_rent'])
        fig_scatter.update_traces(textposition='top center', textfont=dict(size=11, color='#dde2ef'),
                                  hovertemplate='<b>%{customdata[0]}</b><br>Price: £%{customdata[1]:,.0f}'
                                                '<br>Yield: %{customdata[2]:.1f}%<br>Rent: £%{customdata[3]:,.0f}/mo<extra></extra>')
        fig_scatter.update_coloraxes(showscale=False)
        dark_layout(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════ RANKINGS ═════════════════════════════════════
with tab_rank:
    st.markdown(f'<div class="rec-badge">Viewing as: {persona}</div>', unsafe_allow_html=True)

    top_row     = ranked.iloc[0]
    top_pc_name = top_row['postcode']
    reasons     = rec_reasons(top_pc_name, ranked, data, persona)
    reasons_html = ''.join(
        f'<div class="rec-reason"><span class="rec-bullet">▸</span>{r}</div>' for r in reasons
    )
    st.markdown(f"""
    <div class="rec-card">
      <div class="rec-postcode">{top_pc_name} 🏆</div>
      <div class="rec-title">RECOMMENDED FOR {persona.upper()}</div>
      {reasons_html}
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"Full Rankings — {persona}")
    insight(f"Rankings weighted for {persona} priorities. {top_pc_name} scores highest; "
            f"adjust persona in the sidebar to re-rank.")

    for _, row in ranked.iterrows():
        rk        = int(row['rank'])
        row_class = 'rank-row-1' if rk == 1 else ''
        num_class = 'rank-num-1' if rk == 1 else ''
        trophy    = ' 🏆' if rk == 1 else ''
        st.markdown(f"""
        <div class="rank-row {row_class}">
          <div class="rank-num {num_class}">{rk}</div>
          <div class="rank-pc">{row['postcode']}{trophy}</div>
          <div class="rank-stats">
            <div class="rank-stat"><div class="rank-stat-lbl">Avg Rent</div><div class="rank-stat-val">£{row['avg_rent']:,.0f}/mo</div></div>
            <div class="rank-stat"><div class="rank-stat-lbl">Yield</div><div class="rank-stat-val">{row['yield_pct']:.1f}%</div></div>
            <div class="rank-stat"><div class="rank-stat-lbl">City</div><div class="rank-stat-val">{row['dist_city']:.1f}km</div></div>
            <div class="rank-stat"><div class="rank-stat-lbl">Uni</div><div class="rank-stat-val">{row['dist_uni']:.1f}km</div></div>
          </div>
          <div class="rank-score-badge">{row['score']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        pc_data   = filtered[filtered['postcode'] == row['postcode']]
        why_parts = rec_reasons(row['postcode'], ranked, data, persona)
        with st.expander(f"Why {row['postcode']} ranked #{rk}"):
            for wp in why_parts:
                st.markdown(f"**▸** {wp}")
            st.caption(f"Avg price: £{row['avg_price']:,.0f} · Score: {row['score']:.3f} · Based on {len(pc_data)} data points")


# ═══════════════════════════════ MAP ══════════════════════════════════════════
with tab_map:
    map_agg = filtered.groupby('postcode').agg(
        avg_rent=('avg_rent','mean'), avg_price=('avg_price','mean'),
        yield_pct=('yield_percent','mean'), dist_city=('distance_to_city_center_km','mean'),
        dist_uni=('distance_to_university_km','mean'),
    ).reset_index()
    map_agg = map_agg.merge(ranked[['postcode','rank','score']], on='postcode', how='left')
    map_agg['lat'] = map_agg['postcode'].map(lambda x: POSTCODE_COORDS.get(x,(53.47,-2.24))[0])
    map_agg['lon'] = map_agg['postcode'].map(lambda x: POSTCODE_COORDS.get(x,(53.47,-2.24))[1])

    top_yield_map = map_agg.loc[map_agg['yield_pct'].idxmax()]
    insight(f"{top_yield_map['postcode']} shows the strongest rental yield this period "
            f"at {top_yield_map['yield_pct']:.1f}% — "
            f"avg rent £{top_yield_map['avg_rent']:,.0f}/mo at {top_yield_map['dist_city']:.1f}km from city.")

    fig_map = px.scatter_mapbox(
        map_agg, lat='lat', lon='lon', size='avg_rent', color='yield_pct',
        color_continuous_scale=[(0,'#2a2a5a'),(0.4,'#4f9cf9'),(1,'#00ff88')],
        hover_name='postcode', custom_data=['avg_rent','yield_pct','dist_city','rank'],
        zoom=11.2, center={'lat':53.469,'lon':-2.240},
        mapbox_style='carto-darkmatter', size_max=35, height=500,
    )
    fig_map.update_traces(hovertemplate=(
        '<b>%{hovertext}</b><br>'
        'Avg Rent: £%{customdata[0]:,.0f}/mo<br>'
        'Yield: %{customdata[1]:.1f}%<br>'
        'City Distance: %{customdata[2]:.1f}km<br>'
        'Rank: #%{customdata[3]}<extra></extra>'
    ))
    fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0),
                          coloraxis_colorbar=dict(
                              title=dict(text='Yield %', font=dict(color='#dde2ef', size=11)),
                              tickfont=dict(color='#dde2ef', size=11)))
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Postcode Breakdown")
    map_cols = st.columns(len(map_agg))
    for i, (_, row) in enumerate(map_agg.sort_values('rank').iterrows()):
        with map_cols[i]:
            st.markdown(f"""
            <div class="map-card">
              <span class="map-rank-badge">#{int(row['rank'])}</span>
              <div class="map-card-pc">{row['postcode']}</div>
              <div class="map-card-stats">£{row['avg_rent']:,.0f}/mo · {row['yield_pct']:.1f}% yield<br>
              City {row['dist_city']:.1f}km · Uni {row['dist_uni']:.1f}km</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════ PREDICTOR ════════════════════════════════════
with tab_pred:
    st.subheader("Rent Predictor")
    insight("Enter property details to estimate monthly rent. Model trained on Manchester synthetic data 2021–2025 using Linear Regression.")

    col_in, col_out = st.columns([1,1], gap='large')

    with col_in:
        st.markdown('<div class="pred-in-card">', unsafe_allow_html=True)
        st.markdown('<div class="pred-in-title">Property Details</div>', unsafe_allow_html=True)

        pred_pc        = st.selectbox('Postcode', options=sorted(data['postcode'].unique()), key='pred_pc')
        pred_type      = st.selectbox('Property Type', options=sorted(data['property_type'].unique()), key='pred_type')
        pred_size      = st.slider('Property Size (sqft)',
                                   int(data['property_size_sqft'].min()),
                                   int(data['property_size_sqft'].max()),
                                   int(data['property_size_sqft'].median()), step=50, key='pred_size')
        pred_dist_city = st.slider('Distance to City Centre (km)', 0.5, 10.0,
                                   float(data['distance_to_city_center_km'].median()), step=0.1, key='pred_dist_city')
        pred_dist_uni  = st.slider('Distance to University (km)', 0.5, 8.0,
                                   float(data['distance_to_university_km'].median()), step=0.1, key='pred_dist_uni')

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="pred-btn">', unsafe_allow_html=True)
        predict_clicked = st.button('Predict Rent', key='predict_btn', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if predict_clicked:
            sub = data[(data['postcode'] == pred_pc) & (data['property_type'] == pred_type)]
            if sub.empty:
                sub = data[data['postcode'] == pred_pc]
            med_price   = float(sub['avg_price'].median())
            med_yield   = float(sub['yield_percent'].median())
            avg_rent_pc = float(sub['avg_rent'].mean())

            X_new = pd.DataFrame(
                [[pred_pc, pred_type, med_price, med_yield, pred_size, pred_dist_city, pred_dist_uni]],
                columns=['postcode','property_type','avg_price','yield_percent',
                         'property_size_sqft','distance_to_city_center_km','distance_to_university_km'],
            )
            X_proc     = preprocessor.transform(X_new)
            prediction = float(model.predict(X_proc)[0])
            mae        = metrics['mae']
            r2         = metrics['r2']
            low, high  = prediction - mae, prediction + mae
            pct        = ((prediction - avg_rent_pc) / avg_rent_pc * 100) if avg_rent_pc else 0
            direction  = 'above' if pct > 0 else 'below'
            out_of_range = (pred_size < data['property_size_sqft'].min() * 0.9
                            or pred_size > data['property_size_sqft'].max() * 1.1)

            st.session_state['pred_result'] = dict(
                prediction=prediction, low=low, high=high, mae=mae, r2=r2,
                pct=abs(pct), direction=direction, pc=pred_pc, out_of_range=out_of_range,
            )

    with col_out:
        if 'pred_result' in st.session_state:
            pr       = st.session_state['pred_result']
            warn_html = ('<div class="pred-out-warn">⚠ Property size is outside typical training range — '
                         'estimate may be less reliable.</div>' if pr['out_of_range'] else '')
            st.markdown(f"""
            <div class="pred-out-card">
              <div class="pred-out-label">PREDICTED MONTHLY RENT</div>
              <div class="pred-out-value">£{pr['prediction']:,.0f}</div>
              <div class="pred-out-range">Range: £{pr['low']:,.0f} – £{pr['high']:,.0f}</div>
              <div class="pred-out-cmp">{pr['pct']:.0f}% {pr['direction']} {pr['pc']} average</div>
              <div class="pred-out-note">
                Linear Regression model trained on Manchester synthetic data 2021–2025.<br>
                R² = {pr['r2']:.3f} &nbsp;·&nbsp; MAE = £{pr['mae']:.0f}{warn_html}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="pred-out-card"><div class="pred-empty">Fill in the property details '
                        'and click <strong>Predict Rent</strong> to see your estimate.</div></div>',
                        unsafe_allow_html=True)


# ═══════════════════════════════ TRENDS ═══════════════════════════════════════
with tab_trend:
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Monthly Rent Trend")
    monthly = compute_monthly_trend(filtered).sort_values('date')
    monthly['date_str'] = monthly['date'].astype(str)
    if len(monthly) >= 2:
        first_v   = monthly.iloc[0]['avg_rent_mean']
        last_v    = monthly.iloc[-1]['avg_rent_mean']
        delta_pct = (last_v - first_v) / first_v * 100 if first_v else 0
        dir_str   = 'risen' if delta_pct > 0 else 'fallen'
        insight(f"Average rent has {dir_str} by £{abs(last_v - first_v):.0f} ({abs(delta_pct):.1f}%) "
                f"from {monthly.iloc[0]['date_str']} to {monthly.iloc[-1]['date_str']}, "
                f"reflecting {'upward rent pressure' if delta_pct > 0 else 'softening demand'}.")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly['date_str'], y=monthly['avg_rent_mean'], mode='lines+markers',
        line=dict(color='#00ff88', width=2.5),
        marker=dict(size=6, color='#00ff88', line=dict(color='#0d0d1a', width=2)),
        fill='tozeroy', fillcolor='rgba(0,255,136,0.06)',
        hovertemplate='%{x}<br>Avg Rent: £%{y:,.0f}<extra></extra>', name='Avg Rent',
    ))
    dark_layout(fig_trend)
    fig_trend.update_xaxes(tickangle=45)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Rent Trend by Postcode")
    monthly_pc = filtered.groupby(['date','postcode'])['avg_rent'].mean().reset_index()
    monthly_pc['date_str'] = monthly_pc['date'].astype(str)
    colours = ['#00ff88','#4f9cf9','#a855f7','#f97316','#f43f5e']
    fig_pc_trend = go.Figure()
    for i, pc in enumerate(sorted(monthly_pc['postcode'].unique())):
        sub = monthly_pc[monthly_pc['postcode'] == pc].sort_values('date_str')
        fig_pc_trend.add_trace(go.Scatter(
            x=sub['date_str'], y=sub['avg_rent'], mode='lines+markers', name=pc,
            line=dict(color=colours[i % len(colours)], width=2), marker=dict(size=5),
            hovertemplate=f'<b>{pc}</b><br>%{{x}}<br>£%{{y:,.0f}}/mo<extra></extra>',
        ))
    insight("Per-postcode trend reveals where rents are accelerating fastest. "
            "Diverging lines signal emerging affordability gaps across the city.")
    dark_layout(fig_pc_trend, height=390)
    fig_pc_trend.update_xaxes(tickangle=45)
    st.plotly_chart(fig_pc_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Price vs Rent")
        insight("Steeper slope = stronger yield. Postcodes above the trend line offer better value.")
        fig_pvr = px.scatter(filtered, x='avg_price', y='avg_rent', color='postcode',
                             symbol='property_type',
                             color_discrete_sequence=['#00ff88','#4f9cf9','#a855f7','#f97316','#f43f5e'],
                             labels={'avg_price':'Avg Price (£)','avg_rent':'Avg Rent (£)','postcode':'Postcode'},
                             custom_data=['postcode','property_type','avg_price','avg_rent'])
        fig_pvr.update_traces(marker=dict(size=7, opacity=0.75),
                              hovertemplate='<b>%{customdata[0]}</b> %{customdata[1]}<br>'
                                            'Price: £%{customdata[2]:,.0f}<br>'
                                            'Rent: £%{customdata[3]:,.0f}/mo<extra></extra>')
        dark_layout(fig_pvr, height=340)
        st.plotly_chart(fig_pvr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Yield Over Time")
        insight("Yield compression signals rising prices outpacing rent growth — watch this metric closely.")
        monthly_yield = filtered.groupby('date')['yield_percent'].mean().reset_index()
        monthly_yield['date_str'] = monthly_yield['date'].astype(str)
        fig_yield_t = go.Figure()
        fig_yield_t.add_trace(go.Scatter(
            x=monthly_yield['date_str'], y=monthly_yield['yield_percent'], mode='lines+markers',
            line=dict(color='#a855f7', width=2.5), marker=dict(size=5, color='#a855f7'),
            fill='tozeroy', fillcolor='rgba(168,85,247,0.06)',
            hovertemplate='%{x}<br>Yield: %{y:.2f}%<extra></extra>',
        ))
        dark_layout(fig_yield_t, height=340)
        fig_yield_t.update_xaxes(tickangle=45)
        st.plotly_chart(fig_yield_t, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


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

from __future__ import annotations

import pandas as pd
from typing import Dict, List

from analysis_utils import compute_monthly_trend


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

    if len(g) < 2:
        g['score'] = 1.0
        g['rank'] = 1
        return g

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

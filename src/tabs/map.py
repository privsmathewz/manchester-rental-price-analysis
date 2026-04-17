from __future__ import annotations

from typing import Tuple, Dict

import pandas as pd
import plotly.express as px
import streamlit as st

from charts import insight

POSTCODE_COORDS: Dict[str, Tuple[float, float]] = {
    'M1':  (53.476, -2.230),
    'M3':  (53.484, -2.249),
    'M5':  (53.473, -2.273),
    'M13': (53.461, -2.209),
    'M14': (53.449, -2.220),
}


def render_map(filtered: pd.DataFrame, ranked: pd.DataFrame) -> None:
    map_agg = filtered.groupby('postcode').agg(
        avg_rent=('avg_rent', 'mean'),
        avg_price=('avg_price', 'mean'),
        yield_pct=('yield_percent', 'mean'),
        dist_city=('distance_to_city_center_km', 'mean'),
        dist_uni=('distance_to_university_km', 'mean'),
    ).reset_index()
    map_agg = map_agg.merge(ranked[['postcode', 'rank', 'score']], on='postcode', how='left')
    map_agg['lat'] = map_agg['postcode'].map(
        lambda x: POSTCODE_COORDS.get(x, (53.47, -2.24))[0]
    )
    map_agg['lon'] = map_agg['postcode'].map(
        lambda x: POSTCODE_COORDS.get(x, (53.47, -2.24))[1]
    )

    top_yield_map = map_agg.loc[map_agg['yield_pct'].idxmax()]
    insight(
        f"{top_yield_map['postcode']} shows the strongest rental yield this period "
        f"at {top_yield_map['yield_pct']:.1f}% — "
        f"avg rent £{top_yield_map['avg_rent']:,.0f}/mo at {top_yield_map['dist_city']:.1f}km from city."
    )

    fig_map = px.scatter_mapbox(
        map_agg, lat='lat', lon='lon',
        size='avg_rent', color='yield_pct',
        color_continuous_scale=[(0, '#2a2a5a'), (0.4, '#4f9cf9'), (1, '#00ff88')],
        hover_name='postcode',
        custom_data=['avg_rent', 'yield_pct', 'dist_city', 'rank'],
        zoom=11.2,
        center={'lat': 53.469, 'lon': -2.240},
        mapbox_style='carto-darkmatter',
        size_max=35,
        height=500,
    )
    fig_map.update_traces(hovertemplate=(
        '<b>%{hovertext}</b><br>'
        'Avg Rent: £%{customdata[0]:,.0f}/mo<br>'
        'Yield: %{customdata[1]:.1f}%<br>'
        'City Distance: %{customdata[2]:.1f}km<br>'
        'Rank: #%{customdata[3]}<extra></extra>'
    ))
    fig_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            title=dict(text='Yield %', font=dict(color='#dde2ef', size=11)),
            tickfont=dict(color='#dde2ef', size=11),
        ),
    )
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

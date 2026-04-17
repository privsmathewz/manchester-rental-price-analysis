from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis_utils import compute_monthly_trend
from charts import dark_layout, insight


def render_trends(filtered: pd.DataFrame) -> None:
    # ── Monthly trend ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Monthly Rent Trend")
    monthly = compute_monthly_trend(filtered).sort_values('date')
    monthly['date_str'] = monthly['date'].astype(str)

    if len(monthly) >= 2:
        first_v = monthly.iloc[0]['avg_rent_mean']
        last_v = monthly.iloc[-1]['avg_rent_mean']
        delta_pct = (last_v - first_v) / first_v * 100 if first_v else 0
        dir_str = 'risen' if delta_pct > 0 else 'fallen'
        insight(
            f"Average rent has {dir_str} by £{abs(last_v - first_v):.0f} ({abs(delta_pct):.1f}%) "
            f"from {monthly.iloc[0]['date_str']} to {monthly.iloc[-1]['date_str']}, "
            f"reflecting {'upward rent pressure' if delta_pct > 0 else 'softening demand'}."
        )

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly['date_str'], y=monthly['avg_rent_mean'],
        mode='lines+markers',
        line=dict(color='#00ff88', width=2.5),
        marker=dict(size=6, color='#00ff88', line=dict(color='#0d0d1a', width=2)),
        fill='tozeroy', fillcolor='rgba(0,255,136,0.06)',
        hovertemplate='%{x}<br>Avg Rent: £%{y:,.0f}<extra></extra>',
        name='Avg Rent',
    ))
    dark_layout(fig_trend)
    fig_trend.update_xaxes(tickangle=45)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Trend by postcode ─────────────────────────────────────────────────────
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Rent Trend by Postcode")
    monthly_pc = filtered.groupby(['date', 'postcode'])['avg_rent'].mean().reset_index()
    monthly_pc['date_str'] = monthly_pc['date'].astype(str)
    colours = ['#00ff88', '#4f9cf9', '#a855f7', '#f97316', '#f43f5e']

    fig_pc_trend = go.Figure()
    for i, pc in enumerate(sorted(monthly_pc['postcode'].unique())):
        sub = monthly_pc[monthly_pc['postcode'] == pc].sort_values('date_str')
        fig_pc_trend.add_trace(go.Scatter(
            x=sub['date_str'], y=sub['avg_rent'],
            mode='lines+markers', name=pc,
            line=dict(color=colours[i % len(colours)], width=2),
            marker=dict(size=5),
            hovertemplate=f'<b>{pc}</b><br>%{{x}}<br>£%{{y:,.0f}}/mo<extra></extra>',
        ))

    insight(
        "Per-postcode trend reveals where rents are accelerating fastest. "
        "Diverging lines signal emerging affordability gaps across the city."
    )
    dark_layout(fig_pc_trend, height=390)
    fig_pc_trend.update_xaxes(tickangle=45)
    st.plotly_chart(fig_pc_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Price vs Rent")
        insight("Steeper slope = stronger yield. Postcodes above the trend line offer better value.")
        fig_pvr = px.scatter(
            filtered, x='avg_price', y='avg_rent', color='postcode',
            symbol='property_type',
            color_discrete_sequence=['#00ff88', '#4f9cf9', '#a855f7', '#f97316', '#f43f5e'],
            labels={
                'avg_price': 'Avg Price (£)', 'avg_rent': 'Avg Rent (£)', 'postcode': 'Postcode',
            },
            custom_data=['postcode', 'property_type', 'avg_price', 'avg_rent'],
        )
        fig_pvr.update_traces(
            marker=dict(size=7, opacity=0.75),
            hovertemplate=(
                '<b>%{customdata[0]}</b> %{customdata[1]}<br>'
                'Price: £%{customdata[2]:,.0f}<br>'
                'Rent: £%{customdata[3]:,.0f}/mo<extra></extra>'
            ),
        )
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
            x=monthly_yield['date_str'], y=monthly_yield['yield_percent'],
            mode='lines+markers',
            line=dict(color='#a855f7', width=2.5),
            marker=dict(size=5, color='#a855f7'),
            fill='tozeroy', fillcolor='rgba(168,85,247,0.06)',
            hovertemplate='%{x}<br>Yield: %{y:.2f}%<extra></extra>',
        ))
        dark_layout(fig_yield_t, height=340)
        fig_yield_t.update_xaxes(tickangle=45)
        st.plotly_chart(fig_yield_t, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

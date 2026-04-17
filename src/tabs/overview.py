from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis_utils import compute_average_rent_by_postcode, compute_average_yield_by_postcode
from charts import dark_layout, insight


def render_overview(filtered: pd.DataFrame) -> None:
    # ── Rent by postcode ──────────────────────────────────────────────────────
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Average Rent by Postcode")
    avg_rent_df = compute_average_rent_by_postcode(filtered)

    if avg_rent_df.empty or len(avg_rent_df) < 2:
        st.info("Not enough data to display this chart. Adjust your filters.")
    else:
        top_pc = avg_rent_df.iloc[0]['postcode']
        bot_pc = avg_rent_df.iloc[-1]['postcode']
        gap = avg_rent_df.iloc[0]['avg_rent_mean'] - avg_rent_df.iloc[-1]['avg_rent_mean']
        insight(
            f"{top_pc} commands the highest average rent at £{avg_rent_df.iloc[0]['avg_rent_mean']:,.0f}/mo, "
            f"while {bot_pc} offers the best affordability at £{avg_rent_df.iloc[-1]['avg_rent_mean']:,.0f}/mo "
            f"— a £{gap:,.0f}/mo gap."
        )
        fig_rent = px.bar(
            avg_rent_df, x='postcode', y='avg_rent_mean',
            color='avg_rent_mean',
            color_continuous_scale=[(0, '#2a2a5a'), (0.5, '#4f9cf9'), (1, '#00ff88')],
            labels={'avg_rent_mean': 'Avg Rent (£)', 'postcode': 'Postcode'},
            custom_data=['postcode', 'avg_rent_mean'],
        )
        fig_rent.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Avg Rent: £%{customdata[1]:,.0f}/mo<extra></extra>',
            marker_line_width=0,
        )
        fig_rent.update_coloraxes(showscale=False)
        dark_layout(fig_rent)
        st.plotly_chart(fig_rent, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Yield by postcode ─────────────────────────────────────────────────────
    st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
    st.subheader("Gross Yield by Postcode")
    avg_yield_df = compute_average_yield_by_postcode(filtered)

    if avg_yield_df.empty or len(avg_yield_df) < 2:
        st.info("Not enough data to display this chart. Adjust your filters.")
    else:
        hy_pc = avg_yield_df.iloc[0]['postcode']
        hy_val = avg_yield_df.iloc[0]['yield_percent_mean']
        ly_pc = avg_yield_df.iloc[-1]['postcode']
        insight(
            f"{hy_pc} leads return potential at {hy_val:.1f}% gross yield — "
            f"investors targeting capital efficiency should prioritise this zone over {ly_pc}."
        )
        fig_yield = px.bar(
            avg_yield_df, x='postcode', y='yield_percent_mean',
            color='yield_percent_mean',
            color_continuous_scale=[(0, '#1a1a3e'), (0.5, '#a855f7'), (1, '#00ff88')],
            labels={'yield_percent_mean': 'Avg Yield (%)', 'postcode': 'Postcode'},
            custom_data=['postcode', 'yield_percent_mean'],
        )
        fig_yield.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Yield: %{customdata[1]:.2f}%<extra></extra>',
            marker_line_width=0,
        )
        fig_yield.update_coloraxes(showscale=False)
        dark_layout(fig_yield)
        st.plotly_chart(fig_yield, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Rent Distribution")
        insight("Spread shows how rent varies within each postcode across property types.")
        fig_box = px.box(
            filtered, x='postcode', y='avg_rent', color='postcode',
            color_discrete_sequence=['#4f9cf9', '#00ff88', '#a855f7', '#f97316', '#f43f5e'],
            labels={'avg_rent': 'Avg Rent (£)', 'postcode': 'Postcode'},
        )
        fig_box.update_traces(hovertemplate='<b>%{x}</b><br>Rent: £%{y:,.0f}/mo<extra></extra>')
        dark_layout(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-wrap">', unsafe_allow_html=True)
        st.subheader("Yield vs Avg Price")
        insight("Higher-yielding postcodes are often lower-price entry points — ideal for investors.")
        agg = filtered.groupby('postcode').agg(
            avg_price=('avg_price', 'mean'),
            yield_pct=('yield_percent', 'mean'),
            avg_rent=('avg_rent', 'mean'),
        ).reset_index()
        fig_scatter = px.scatter(
            agg, x='avg_price', y='yield_pct', text='postcode',
            size='avg_rent', size_max=28, color='yield_pct',
            color_continuous_scale=[(0, '#2a2a5a'), (1, '#00ff88')],
            labels={'avg_price': 'Avg Price (£)', 'yield_pct': 'Yield (%)'},
            custom_data=['postcode', 'avg_price', 'yield_pct', 'avg_rent'],
        )
        fig_scatter.update_traces(
            textposition='top center',
            textfont=dict(size=11, color='#dde2ef'),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>Price: £%{customdata[1]:,.0f}'
                '<br>Yield: %{customdata[2]:.1f}%<br>Rent: £%{customdata[3]:,.0f}/mo<extra></extra>'
            ),
        )
        fig_scatter.update_coloraxes(showscale=False)
        dark_layout(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

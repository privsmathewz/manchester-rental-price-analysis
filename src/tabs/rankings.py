from __future__ import annotations

import pandas as pd
import streamlit as st

from charts import insight
from rankings import rec_reasons


def render_rankings(
    ranked: pd.DataFrame,
    filtered: pd.DataFrame,
    data: pd.DataFrame,
    persona: str,
) -> None:
    st.markdown(f'<div class="rec-badge">Viewing as: {persona}</div>', unsafe_allow_html=True)

    top_row = ranked.iloc[0]
    top_pc_name = top_row['postcode']
    reasons = rec_reasons(top_pc_name, ranked, data, persona)
    reasons_html = ''.join(
        f'<div class="rec-reason"><span class="rec-bullet">▸</span>{r}</div>'
        for r in reasons
    )
    st.markdown(f"""
    <div class="rec-card">
      <div class="rec-postcode">{top_pc_name} 🏆</div>
      <div class="rec-title">RECOMMENDED FOR {persona.upper()}</div>
      {reasons_html}
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"Full Rankings — {persona}")
    insight(
        f"Rankings weighted for {persona} priorities. {top_pc_name} scores highest; "
        f"adjust persona in the filter bar to re-rank."
    )

    for _, row in ranked.iterrows():
        rk = int(row['rank'])
        row_class = 'rank-row-1' if rk == 1 else ''
        num_class = 'rank-num-1' if rk == 1 else ''
        trophy = ' 🏆' if rk == 1 else ''
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

        pc_data = filtered[filtered['postcode'] == row['postcode']]
        why_parts = rec_reasons(row['postcode'], ranked, data, persona)
        with st.expander(f"Why {row['postcode']} ranked #{rk}"):
            for wp in why_parts:
                st.markdown(f"**▸** {wp}")
            st.caption(
                f"Avg price: £{row['avg_price']:,.0f} · "
                f"Score: {row['score']:.3f} · "
                f"Based on {len(pc_data)} data points"
            )

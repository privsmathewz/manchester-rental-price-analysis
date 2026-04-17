from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go


def insight(text: str) -> None:
    st.markdown(
        f'<div class="insight"><span class="insight-icon">◈</span>{text}</div>',
        unsafe_allow_html=True,
    )


def dark_layout(fig: go.Figure, title: str = '', height: int = 370) -> go.Figure:
    try:
        fig.update_layout(
            title=dict(text=title, font=dict(size=13, color='#dde2ef'), x=0, xanchor='left'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(13,13,26,0.8)',
            font=dict(family='Space Grotesk, sans-serif', color='#dde2ef', size=12),
            height=height,
            margin=dict(l=40, r=30, t=50, b=40),
            legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.08)', font=dict(size=11)),
        )
        fig.update_xaxes(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.08)',
            tickfont=dict(size=11, color='#a0aec0'),
        )
        fig.update_yaxes(
            gridcolor='rgba(255,255,255,0.05)',
            linecolor='rgba(255,255,255,0.08)',
            tickfont=dict(size=11, color='#a0aec0'),
        )
    except Exception:
        pass
    return fig

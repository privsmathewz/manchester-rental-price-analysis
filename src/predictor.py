from __future__ import annotations

import pandas as pd
import streamlit as st

from charts import insight


def render_predictor(
    filtered: pd.DataFrame,
    data: pd.DataFrame,
    model,
    metrics: dict,
    preprocessor,
) -> None:
    st.subheader("Rent Predictor")
    insight(
        "Enter property details to estimate monthly rent. "
        "Model trained on Manchester synthetic data 2021–2025 using Linear Regression."
    )

    col_in, col_out = st.columns([1, 1], gap='large')

    with col_in:
        st.markdown('<div class="pred-in-card">', unsafe_allow_html=True)
        st.markdown('<div class="pred-in-title">Property Details</div>', unsafe_allow_html=True)

        pred_pc = st.selectbox(
            'Postcode', options=sorted(data['postcode'].unique()), key='pred_pc'
        )
        pred_type = st.selectbox(
            'Property Type', options=sorted(data['property_type'].unique()), key='pred_type'
        )
        pred_size = st.slider(
            'Property Size (sqft)',
            int(data['property_size_sqft'].min()),
            int(data['property_size_sqft'].max()),
            int(data['property_size_sqft'].median()),
            step=50,
            key='pred_size',
        )
        pred_dist_city = st.slider(
            'Distance to City Centre (km)', 0.5, 10.0,
            float(data['distance_to_city_center_km'].median()),
            step=0.1, key='pred_dist_city',
        )
        pred_dist_uni = st.slider(
            'Distance to University (km)', 0.5, 8.0,
            float(data['distance_to_university_km'].median()),
            step=0.1, key='pred_dist_uni',
        )

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="pred-btn">', unsafe_allow_html=True)
        predict_clicked = st.button('Predict Rent', key='predict_btn', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if predict_clicked:
            sub = data[(data['postcode'] == pred_pc) & (data['property_type'] == pred_type)]
            if sub.empty:
                sub = data[data['postcode'] == pred_pc]

            med_price = float(sub['avg_price'].median())
            med_yield = float(sub['yield_percent'].median())
            avg_rent_pc = float(sub['avg_rent'].mean())

            X_new = pd.DataFrame(
                [[pred_pc, pred_type, med_price, med_yield, pred_size, pred_dist_city, pred_dist_uni]],
                columns=[
                    'postcode', 'property_type', 'avg_price', 'yield_percent',
                    'property_size_sqft', 'distance_to_city_center_km', 'distance_to_university_km',
                ],
            )

            try:
                X_proc = preprocessor.transform(X_new)
                prediction = float(model.predict(X_proc)[0])
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                st.stop()

            mae = metrics['mae']
            r2 = metrics['r2']
            low, high = prediction - mae, prediction + mae
            pct = ((prediction - avg_rent_pc) / avg_rent_pc * 100) if avg_rent_pc else 0
            direction = 'above' if pct > 0 else 'below'
            out_of_range = (
                pred_size < data['property_size_sqft'].min() * 0.9
                or pred_size > data['property_size_sqft'].max() * 1.1
            )

            st.session_state['pred_result'] = dict(
                prediction=prediction, low=low, high=high, mae=mae, r2=r2,
                pct=abs(pct), direction=direction, pc=pred_pc, out_of_range=out_of_range,
            )

    with col_out:
        if 'pred_result' in st.session_state:
            pr = st.session_state['pred_result']
            warn_html = (
                '<div class="pred-out-warn">⚠ Property size is outside typical training range — '
                'estimate may be less reliable.</div>'
                if pr['out_of_range'] else ''
            )
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
            st.markdown(
                '<div class="pred-out-card"><div class="pred-empty">Fill in the property details '
                'and click <strong>Predict Rent</strong> to see your estimate.</div></div>',
                unsafe_allow_html=True,
            )

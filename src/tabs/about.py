import streamlit as st


def render_about() -> None:
    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">About this platform</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="about-body">
Manchester Rental Intelligence is a portfolio analytics platform built by Sajan Mathew as part of an
MSc Data Science at Manchester Metropolitan University. It demonstrates end-to-end data product
development: from synthetic data generation through Python analytics, machine learning, and
interactive dashboard deployment.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">Data source</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="about-body">
This platform uses a synthetic dataset modelled on Greater Manchester rental market patterns (2021–2025).
It covers five postcode districts: M1, M3, M5, M13, and M14. Data includes monthly average rent,
average property price, gross yield, property size, and distance metrics.<br><br>
<strong style="color:#f59e0b;">⚠ Portfolio demonstration only. Values are modelled approximations,
not live market data.</strong>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">Persona scoring methodology</div>', unsafe_allow_html=True)
    st.markdown("""
<table class="about-table">
  <thead>
    <tr>
      <th>Persona</th>
      <th>Weight 1</th>
      <th>Weight 2</th>
      <th>Weight 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="green">Student</td>
      <td>40% — low rent</td>
      <td>40% — low university distance</td>
      <td>20% — low city distance</td>
    </tr>
    <tr>
      <td class="green">Professional</td>
      <td>50% — low city distance</td>
      <td>30% — low rent</td>
      <td>20% — high yield</td>
    </tr>
    <tr>
      <td class="green">Investor</td>
      <td>60% — high yield</td>
      <td>40% — low avg price</td>
      <td>—</td>
    </tr>
    <tr>
      <td class="green">Explorer</td>
      <td>25% — high yield</td>
      <td>25% — low rent</td>
      <td>25% city + 25% university distance</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)
    st.markdown("""
<div class="about-body" style="margin-top:12px;">
Each postcode is scored by normalising each metric to [0, 1] and computing a weighted average.
The normalisation ensures fair comparison across postcodes regardless of absolute values.
Scores of 0–1 are shown in the Rankings tab for full transparency.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">Forecast methodology</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="about-body">
The 6-month rent forecast uses Linear Regression fitted on historical monthly average rent values per
postcode. The model extrapolates forward using engineered time features. This is a directional
indicator only. Confidence intervals reflect training MAE and should not be used for investment decisions.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">Model performance</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="about-body">
The rent predictor uses a Linear Regression model trained on all available data. R² and MAE values are
shown inline at prediction time. The model performs well within the training data range and degrades
outside it. An out-of-range warning is shown when inputs exceed training bounds.
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-label">Built by</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="about-body">
<strong style="color:#ffffff;">Sajan Mathew</strong><br>
MSc Data Science · Manchester Metropolitan University<br>
Graduate Route visa — full UK right to work until June 2028<br><br>
<a href="https://github.com/privsmathewz" target="_blank" style="color:#00ff88;text-decoration:none;">
  github.com/privsmathewz
</a>
&nbsp;·&nbsp;
<a href="https://linkedin.com/in/sajanmathew" target="_blank" style="color:#00ff88;text-decoration:none;">
  linkedin.com/in/sajanmathew
</a>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

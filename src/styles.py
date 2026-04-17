def load_css() -> str:
    return """
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
  flex-wrap: wrap !important;
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
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
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

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.topbar-wrap {
  background: #0d0d1a;
  border: 1px solid #1e1e3a;
  border-radius: 12px;
  padding: 16px 20px 8px;
  margin: 16px 0 20px;
}

/* About tab */
.about-section {
  background: #0d0d1a;
  border: 1px solid #1e1e3a;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
}
.about-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: #00ff88;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.about-body {
  font-size: 14px;
  color: #c4c9e2;
  line-height: 1.75;
}
.about-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
  font-size: 13px;
}
.about-table th {
  color: #6b7280;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.about-table td {
  padding: 10px 12px;
  color: #dde2ef;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  vertical-align: top;
}
.about-table tr:last-child td { border-bottom: none; }
.about-table .green { color: #00ff88; font-weight: 700; }

/* ── Mobile responsive ─────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .main .block-container {
    padding: 1rem !important;
  }

  /* Top filter bar: stack vertically */
  .topbar-wrap {
    padding: 12px !important;
  }
  [data-testid="column"] {
    min-width: 100% !important;
    flex: 0 0 100% !important;
    width: 100% !important;
  }

  /* Pulse grid: 2x2 */
  .pulse-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }

  /* Hero */
  .hero-wrap  { padding: 28px 18px 22px !important; }
  .hero-headline { font-size: 2.4rem !important; }

  /* KPI metrics: 2 per row */
  [data-testid="stMetric"] {
    min-width: 45% !important;
  }

  /* Predictor columns: stack */
  .pred-in-card, .pred-out-card { padding: 18px !important; }
  .pred-out-value { font-size: 40px !important; }

  /* Map height */
  .js-plotly-plot { max-height: 350px !important; }

  /* Rankings */
  .rec-postcode { font-size: 38px !important; }
  .rank-stats { flex-direction: column; gap: 6px; }

  /* Footer */
  .page-footer { flex-direction: column; text-align: center; }

  /* Section padding */
  .section-wrap { padding: 16px !important; }
  .about-section { padding: 16px !important; }
}

@media (max-width: 480px) {
  /* Pulse grid: single column */
  .pulse-grid {
    grid-template-columns: 1fr !important;
  }

  /* Hero headline */
  .hero-headline { font-size: 1.8rem !important; }

  /* KPI: single column */
  [data-testid="stMetric"] {
    min-width: 100% !important;
  }

  /* Footer: single column */
  .page-footer {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
}
</style>
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
from datetime import datetime

# ---------------------------------------------------------
# SETUP PATH & KONFIGURASI HALAMAN
# ---------------------------------------------------------
CHELSEA_LOGO_URL = "https://ssl.gstatic.com/onebox/media/sports/logos/optimized/fhBITrIlbQxhVB6IjxUO6Q_64x64.png"

st.set_page_config(
    page_title="Rifaldi W Analytics — Chelsea FC 2024/25",
    page_icon="dashboard/assets/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
SCRIPTS_DIR = BASE_DIR / "scripts"

sys.path.append(str(SCRIPTS_DIR))

try:
    import analyze_data
    df_clean = analyze_data.load_clean_data()
    df_clean = analyze_data.metrics(df_clean)
except Exception as e:
    st.error(f"Error loading processed data: {e}")
    st.stop()

def load_raw_csv(filename):
    filepath = RAW_DIR / filename
    if filepath.exists():
        return pd.read_csv(filepath)
    return pd.DataFrame()

df_info = load_raw_csv("premier_player_info.csv")
df_stats = load_raw_csv("player_stats_2024_2025_season.csv")
df_club_stats = load_raw_csv("2024_season_club_stats.csv")

if not df_info.empty and not df_stats.empty:
    df_league = pd.merge(df_info, df_stats, on="player_name", how="inner")
    df_league = analyze_data.metrics(df_league)
    df_league['player_position'] = df_league['player_position'].replace('Attacker', 'Forward')
else:
    df_league = pd.DataFrame()

gws = [4, 8, 14, 20, 32, 38]
gw_data_list = []
for gw in gws:
    df_gw = load_raw_csv(f"2024_gameweek_{gw}.csv")
    if not df_gw.empty:
        df_gw['gameweek'] = gw
        gw_data_list.append(df_gw)

if gw_data_list:
    df_all_gws = pd.concat(gw_data_list, ignore_index=True)
    df_gw38 = df_all_gws[df_all_gws['gameweek'] == 38].copy()
else:
    df_all_gws = pd.DataFrame()
    df_gw38 = pd.DataFrame()

# ──────────────────────────────────────────────────────────────
# PLOTLY THEME — Dark premium Opta-style
# ──────────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = go.layout.Template()
PLOTLY_TEMPLATE.layout = go.Layout(
    font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#e0e0e0"),
    title=dict(font=dict(size=18, color="#ffffff"), x=0, xanchor="left"),
    paper_bgcolor="#0f1117",
    plot_bgcolor="#0f1117",
    hovermode="closest",
    hoverlabel=dict(
        bgcolor="#1e2235",
        font=dict(color="#ffffff", size=13),
        bordercolor="#2d3361",
        align="left"
    ),
    colorway=["#034694", "#00b4d8", "#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#ff6b9d", "#c084fc"],
    xaxis=dict(
        gridcolor="#1e2235",
        tickfont=dict(color="#9ca3af"),
        title=dict(font=dict(color="#d1d5db")),
        zerolinecolor="#2d3361",
        showspikes=True,
        spikecolor="#2d3361",
        spikethickness=1
    ),
    yaxis=dict(
        gridcolor="#1e2235",
        tickfont=dict(color="#9ca3af"),
        title=dict(font=dict(color="#d1d5db")),
        zerolinecolor="#2d3361",
        showspikes=True,
        spikecolor="#2d3361",
        spikethickness=1
    ),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        font=dict(color="#d1d5db"),
        bgcolor="rgba(15,17,23,0.8)",
        bordercolor="#2d3361"
    )
)
px.defaults.template = PLOTLY_TEMPLATE

# ──────────────────────────────────────────────────────────────
# PREMIUM CSS — Opta / FotMob inspired dark glassmorphism
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ───── IMPORTS ───── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ───── RESET ───── */
* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
.stApp { background-color: #0a0b12 !important; }

/* ───── SCROLLBAR ───── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2d3361; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #034694; }

/* ───── KEYFRAMES ───── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-40px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(40px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes countUp {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 8px rgba(3, 70, 148, 0.3); }
    50% { box-shadow: 0 0 20px rgba(3, 70, 148, 0.6); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(3, 70, 148, 0.3); }
    50% { border-color: rgba(0, 180, 216, 0.6); }
}

/* ───── GLASS CARD BASE ───── */
.glass-card {
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.85) 0%, rgba(15, 17, 23, 0.9) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(45, 51, 97, 0.5);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    animation: fadeInUp 0.6s ease-out both;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(3, 70, 148, 0.05) 0%, transparent 50%);
    pointer-events: none;
    border-radius: 16px;
}
.glass-card:hover {
    border-color: rgba(3, 70, 148, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(3, 70, 148, 0.15);
}
.glass-card .card-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    margin-bottom: 8px;
    font-weight: 600;
}
.glass-card .card-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.glass-card .card-sub {
    font-size: 0.85rem;
    color: #9ca3af;
    margin-top: 4px;
}

/* ───── HERO HEADER ───── */
.hero-section {
    background: linear-gradient(135deg, #0a0b12 0%, #0f1117 30%, #0d1b3e 70%, #0a0b12 100%);
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
    padding: 32px 40px;
    border-radius: 20px;
    margin-bottom: 32px;
    border: 1px solid rgba(3, 70, 148, 0.2);
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(3, 70, 148, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(0, 180, 216, 0.05) 0%, transparent 50%);
    pointer-events: none;
}
.hero-content { display: flex; align-items: center; gap: 20px; position: relative; z-index: 1; }
.hero-logo { width: 64px; height: 64px; filter: drop-shadow(0 0 20px rgba(3, 70, 148, 0.5)); animation: float 3s ease-in-out infinite; }
.hero-title { margin: 0; font-size: 1.8rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; }
.hero-title span { background: linear-gradient(135deg, #034694, #00b4d8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { color: #6b7280; font-size: 0.95rem; margin: 4px 0 0 0; letter-spacing: 0.02em; }

/* ───── KPI BADGE ───── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-item {
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.8), rgba(15, 17, 23, 0.9));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(45, 51, 97, 0.4);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    animation: fadeInScale 0.5s ease-out both;
    position: relative;
    overflow: hidden;
}
.kpi-item:nth-child(1) { animation-delay: 0.1s; }
.kpi-item:nth-child(2) { animation-delay: 0.2s; }
.kpi-item:nth-child(3) { animation-delay: 0.3s; }
.kpi-item:nth-child(4) { animation-delay: 0.4s; }
.kpi-item:hover {
    border-color: rgba(3, 70, 148, 0.7);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(3, 70, 148, 0.2);
}
.kpi-item .kpi-icon { font-size: 1.5rem; margin-bottom: 8px; }
.kpi-item .kpi-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280; font-weight: 600; }
.kpi-item .kpi-value {
    font-size: 1.6rem; font-weight: 800; color: #ffffff;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 4px 0;
}
.kpi-item .kpi-trend { font-size: 0.8rem; color: #34d399; font-weight: 600; }

/* ───── TABLE ───── */
.premium-table { width: 100%; border-collapse: separate; border-spacing: 0; font-family: 'Inter', sans-serif; }
.premium-table thead th {
    color: #6b7280;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 12px 10px;
    border-bottom: 1px solid rgba(45, 51, 97, 0.5);
    text-align: center;
    background: rgba(15, 17, 23, 0.6);
}
.premium-table thead th:first-child { text-align: left; padding-left: 16px; border-radius: 10px 0 0 0; }
.premium-table thead th:last-child { border-radius: 0 10px 0 0; }
.premium-table tbody tr {
    transition: all 0.2s ease;
    animation: fadeInUp 0.4s ease-out both;
}
.premium-table tbody tr:nth-child(1) { animation-delay: 0.05s; }
.premium-table tbody tr:nth-child(2) { animation-delay: 0.1s; }
.premium-table tbody tr:nth-child(3) { animation-delay: 0.15s; }
.premium-table tbody tr:nth-child(4) { animation-delay: 0.2s; }
.premium-table tbody tr:nth-child(5) { animation-delay: 0.25s; }
.premium-table tbody tr:nth-child(6) { animation-delay: 0.3s; }
.premium-table tbody tr:nth-child(7) { animation-delay: 0.35s; }
.premium-table tbody tr:nth-child(8) { animation-delay: 0.4s; }
.premium-table tbody tr:nth-child(9) { animation-delay: 0.45s; }
.premium-table tbody tr:nth-child(10) { animation-delay: 0.5s; }
.premium-table tbody td {
    padding: 12px 10px;
    border-bottom: 1px solid rgba(45, 51, 97, 0.2);
    text-align: center;
    font-size: 0.9rem;
    color: #d1d5db;
}
.premium-table tbody td:first-child { text-align: left; padding-left: 16px; }
.premium-table tbody tr:last-child td:first-child { border-radius: 0 0 0 10px; }
.premium-table tbody tr:last-child td:last-child { border-radius: 0 0 10px 0; }
.premium-table tbody tr:hover { background: rgba(3, 70, 148, 0.1); }
.premium-table .club-cell { display: flex; align-items: center; gap: 12px; }
.premium-table .pos-badge {
    width: 26px; height: 26px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700;
    background: rgba(45, 51, 97, 0.4);
    color: #9ca3af;
}
.premium-table .pos-1 { background: #fbbf24; color: #0f1117; }
.premium-table .pos-2 { background: #9ca3af; color: #0f1117; }
.premium-table .pos-3 { background: #d97706; color: #fff; }
.premium-table .pos-4 { background: #034694; color: #fff; }
.premium-table .club-logo { width: 22px; height: 22px; object-fit: contain; }
.premium-table .chelsea-row { background: rgba(3, 70, 148, 0.12) !important; }
.premium-table .chelsea-row td { color: #93c5fd; font-weight: 600; }

/* ───── METRIC CARDS ───── */
.metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.metric-card {
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.7), rgba(15, 17, 23, 0.8));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(45, 51, 97, 0.3);
    border-radius: 12px;
    padding: 18px;
    transition: all 0.3s ease;
    animation: fadeInUp 0.5s ease-out both;
}
.metric-card:hover { border-color: rgba(3, 70, 148, 0.5); }
.metric-header {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(45, 51, 97, 0.3);
}
.metric-row {
    display: flex; justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(45, 51, 97, 0.1);
    font-size: 0.88rem;
}
.metric-row:last-child { border-bottom: none; }
.metric-label { color: #9ca3af; font-weight: 400; }
.metric-value { color: #e0e0e0; font-weight: 600; }

/* ───── ANALYTIC INSIGHT ───── */
.analytic-desc {
    background: linear-gradient(135deg, rgba(3, 70, 148, 0.12), rgba(0, 180, 216, 0.05));
    border-left: 3px solid #034694;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-top: 14px;
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.6;
    animation: fadeInUp 0.5s ease-out 0.2s both;
    backdrop-filter: blur(8px);
}
.analytic-desc b { color: #93c5fd; }

/* ───── SECTION TITLES ───── */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin: 24px 0 16px 0;
    letter-spacing: -0.01em;
    position: relative;
    padding-left: 16px;
}
.section-title::before {
    content: '';
    position: absolute;
    left: 0; top: 2px; bottom: 2px;
    width: 4px;
    background: linear-gradient(180deg, #034694, #00b4d8);
    border-radius: 2px;
}

/* ───── INSIGHT REPORT ───── */
.report-card {
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.8), rgba(15, 17, 23, 0.95));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(45, 51, 97, 0.4);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
    animation: fadeInUp 0.6s ease-out both;
}
.report-card h2 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(45, 51, 97, 0.4);
}
.report-card h4 { color: #d1d5db; margin-bottom: 8px; font-size: 1rem; font-weight: 600; }
.report-card p { color: #9ca3af; line-height: 1.7; font-size: 0.95rem; }
.report-card ul { padding-left: 20px; }
.report-card li { color: #9ca3af; line-height: 1.7; font-size: 0.95rem; margin-bottom: 12px; }
.tag-keep { background: rgba(52, 211, 153, 0.15); color: #34d399; padding: 2px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }
.tag-sell { background: rgba(251, 191, 36, 0.15); color: #fbbf24; padding: 2px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }
.tag-urgent { background: rgba(248, 113, 113, 0.15); color: #f87171; padding: 2px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }
.tag-loan { background: rgba(148, 163, 184, 0.15); color: #94a3b8; padding: 2px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; }

/* ───── SQUAD PROFILES ───── */
.player-card {
    display: flex; align-items: center;
    margin-bottom: 10px;
    padding: 14px;
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.6), rgba(15, 17, 23, 0.7));
    border: 1px solid rgba(45, 51, 97, 0.3);
    border-radius: 10px;
    transition: all 0.3s ease;
    animation: fadeInUp 0.4s ease-out both;
}
.player-card:hover {
    border-color: rgba(3, 70, 148, 0.5);
    transform: translateX(4px);
    background: linear-gradient(135deg, rgba(30, 34, 53, 0.8), rgba(3, 70, 148, 0.1));
}
.player-card img {
    width: 50px; height: 65px;
    border-radius: 6px;
    margin-right: 14px;
    object-fit: cover;
    border: 1px solid rgba(45, 51, 97, 0.3);
}
.player-card .pname { font-size: 1rem; font-weight: 600; color: #e0e0e0; }
.player-card .pmeta { font-size: 0.82rem; color: #6b7280; margin-top: 2px; }
.player-card .pmins { font-size: 0.78rem; color: #034694; font-weight: 600; margin-top: 3px; }

/* ───── TABS ───── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: rgba(15, 17, 23, 0.8);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(45, 51, 97, 0.3);
    margin-bottom: 24px;
}
.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 10px;
    padding: 6px 20px;
    color: #6b7280;
    font-size: 0.85rem;
    font-weight: 500;
    transition: all 0.2s ease;
    letter-spacing: 0.01em;
}
.stTabs [data-baseweb="tab"]:hover { color: #93c5fd; background: rgba(3, 70, 148, 0.08); }
.stTabs [aria-selected="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, #034694, #0058b0) !important;
    box-shadow: 0 4px 16px rgba(3, 70, 148, 0.3);
}

/* ───── FOOTER ───── */
.footer-glass {
    position: fixed;
    bottom: 0; left: 0; width: 100%;
    background: rgba(15, 17, 23, 0.9);
    backdrop-filter: blur(16px);
    border-top: 1px solid rgba(45, 51, 97, 0.3);
    color: #6b7280;
    text-align: center;
    padding: 10px 0;
    font-size: 0.8rem;
    font-weight: 500;
    z-index: 100;
}

/* ───── ANIMATED PROGRESS BAR ───── */
.progress-bar-bg {
    width: 100%; height: 4px;
    background: rgba(45, 51, 97, 0.3);
    border-radius: 2px;
    margin-top: 6px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #034694, #00b4d8);
    animation: shimmer 2s ease-in-out infinite;
    background-size: 200% 100%;
}

/* ───── STREAMLiT OVERRIDES ───── */
[id="root"] > div:first-child { background: transparent !important; }
.stApp > header { background: transparent !important; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 4rem !important; max-width: 1400px !important; }
[data-testid="stMetric"] {
    background: transparent !important;
    padding: 0 !important;
}
[data-testid="stMetric"] > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stMetricLabel"] { display: none; }
[data-testid="stMetricValue"] { display: none; }

/* ───── DATA EDITOR ───── */
[data-testid="stDataFrame"] { background: transparent !important; }
[data-testid="stDataFrame"] thead th {
    background: rgba(15, 17, 23, 0.6) !important;
    color: #6b7280 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stDataFrame"] tbody td {
    background: transparent !important;
    color: #d1d5db !important;
    border-bottom: 1px solid rgba(45, 51, 97, 0.15) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(3, 70, 148, 0.08) !important;
}

/* ───── PLOTLY OVERRIDE ───── */
.js-plotly-plot { background: transparent !important; }
.plot-container { background: transparent !important; }

/* ───── DIVIDER ───── */
.premium-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(45, 51, 97, 0.6), transparent);
    margin: 28px 0;
}

</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# HEADER — Premium Hero
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-content">
        <img class="hero-logo" src="{CHELSEA_LOGO_URL}">
        <div>
            <h1 class="hero-title">Rifaldi W <span>Analytics</span></h1>
            <p class="hero-subtitle">Chelsea FC — 2024/2025 Premier League Season Review • Data-Driven Performance Analysis</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# NAVIGATION TABS
# ──────────────────────────────────────────────────────────────
tab_overview, tab_stats, tab_squad, tab_analytics = st.tabs(["📊 Overview", "📈 Statistics", "👥 Squad", "🧠 Analytics"])

# ══════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 20px;">Key performance indicators for the 2024/2025 season</p>', unsafe_allow_html=True)

    # KPI Grid
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-item">
            <div class="kpi-icon">🏟️</div>
            <div class="kpi-label">Games Played</div>
            <div class="kpi-value">38</div>
            <div class="kpi-trend">Full season</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-icon">⚽</div>
            <div class="kpi-label">Goals</div>
            <div class="kpi-value">64</div>
            <div class="kpi-trend">+12 vs last season</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-icon">🛡️</div>
            <div class="kpi-label">Goals Conceded</div>
            <div class="kpi-value">43</div>
            <div class="kpi-trend">-5 vs last season</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-icon">🏆</div>
            <div class="kpi-label">League Finish</div>
            <div class="kpi-value">4th</div>
            <div class="kpi-trend">UCL Qualifier</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # League Table
    st.markdown('<div class="section-title">Premier League Table — Final Standings</div>', unsafe_allow_html=True)

    if not df_gw38.empty:
        df_gw38.loc[df_gw38['name'] == 'Chelsea', 'badge_url'] = CHELSEA_LOGO_URL
        table_rows = ""
        for _, row in df_gw38.sort_values('position').iterrows():
            row_class = "chelsea-row" if row['name'] == 'Chelsea' else ""
            pos_class = f"pos-{min(int(row['position']), 4)}" if row['name'] == 'Chelsea' else ""
            if int(row['position']) > 4:
                pos_class = ""
            table_rows += f"""
            <tr class="{row_class}">
                <td>
                    <div class="club-cell">
                        <span class="pos-badge {pos_class}">{int(row['position'])}</span>
                        <img class="club-logo" src="{row['badge_url']}" onerror="this.style.display='none'">
                        <span style="font-weight:{'600' if row['name'] == 'Chelsea' else '400'}">{row['name']}</span>
                    </div>
                </td>
                <td>{int(row['games_played'])}</td>
                <td>{int(row['games_won'])}</td>
                <td>{int(row['games_drawn'])}</td>
                <td>{int(row['games_lost'])}</td>
                <td>{int(row['goals_for'])}</td>
                <td>{int(row['goals_against'])}</td>
                <td style="font-weight:600;">{int(row['goal_difference']):+d}</td>
                <td style="font-weight:700; color:#ffffff; font-size:1.05rem;">{int(row['points'])}</td>
            </tr>"""

        st.markdown(f"""
        <div class="glass-card" style="padding: 0; overflow: hidden;">
            <table class="premium-table">
                <thead>
                    <tr><th>Club</th><th>MP</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th></tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Team Metrics — Premium Cards
    st.markdown('<div class="section-title">Team Overall Metrics</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div class="metric-card" style="animation-delay: 0.1s;">
            <div class="metric-header">⚔️ Attacking</div>
            <div class="metric-row"><span class="metric-label">Goals</span><span class="metric-value">64</span></div>
            <div class="metric-row"><span class="metric-label">XG (Expected Goals)</span><span class="metric-value">69.19</span></div>
            <div class="metric-row"><span class="metric-label">Shots</span><span class="metric-value">436</span></div>
            <div class="metric-row"><span class="metric-label">Shots On Target</span><span class="metric-value">218</span></div>
            <div class="metric-row"><span class="metric-label">Shots On Target (Inside Box)</span><span class="metric-value">206</span></div>
            <div class="metric-row"><span class="metric-label">Shots On Target (Outside Box)</span><span class="metric-value">121</span></div>
            <div class="metric-row"><span class="metric-label">Touches in Opp. Box</span><span class="metric-value">1,196</span></div>
            <div class="metric-row"><span class="metric-label">Penalties (Scored)</span><span class="metric-value">5 (4)</span></div>
            <div class="metric-row"><span class="metric-label">Free Kicks Scored</span><span class="metric-value">17 (2)</span></div>
            <div class="metric-row"><span class="metric-label">Hit Woodwork</span><span class="metric-value">21</span></div>
            <div class="metric-row"><span class="metric-label">Crosses (Completed)</span><span class="metric-value">463 (22%)</span></div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:64%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card" style="animation-delay: 0.2s;">
            <div class="metric-header">🎯 Possession</div>
            <div class="metric-row"><span class="metric-label">Passes</span><span class="metric-value">19,796</span></div>
            <div class="metric-row"><span class="metric-label">Long Passes (Completed)</span><span class="metric-value">1,788 (46%)</span></div>
            <div class="metric-row"><span class="metric-label">Corners Taken</span><span class="metric-value">236</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="metric-card" style="animation-delay: 0.3s;">
            <div class="metric-header">🛡️ Defending</div>
            <div class="metric-row"><span class="metric-label">Interceptions</span><span class="metric-value">272</span></div>
            <div class="metric-row"><span class="metric-label">Blocks</span><span class="metric-value">103</span></div>
            <div class="metric-row"><span class="metric-label">Clearances</span><span class="metric-value">654</span></div>
            <div class="metric-row"><span class="metric-label">Penalties Saved</span><span class="metric-value">1 (17%)</span></div>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:60%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card" style="animation-delay: 0.4s;">
            <div class="metric-header">💪 Physical</div>
            <div class="metric-row"><span class="metric-label">Dribbles (Completed)</span><span class="metric-value">662 (49%)</span></div>
            <div class="metric-row"><span class="metric-label">Duels Won</span><span class="metric-value">1,760</span></div>
            <div class="metric-row"><span class="metric-label">Aerial Duels Won</span><span class="metric-value">409</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card" style="animation-delay: 0.45s;">
            <div class="metric-header">⚠️ Discipline</div>
            <div class="metric-row"><span class="metric-label">Red Cards</span><span class="metric-value">2</span></div>
            <div class="metric-row"><span class="metric-label">Yellow Cards</span><span class="metric-value">99</span></div>
            <div class="metric-row"><span class="metric-label">Fouls</span><span class="metric-value">436</span></div>
            <div class="metric-row"><span class="metric-label">Offsides</span><span class="metric-value">65</span></div>
            <div class="metric-row"><span class="metric-label">Own Goals</span><span class="metric-value">3</span></div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TAB 2: STATISTICS
# ══════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown('<div class="section-title">Top Chelsea Players 2024/2025</div>', unsafe_allow_html=True)

    top_scorer = df_clean.sort_values(by='Goals', ascending=False).iloc[0]
    top_assist = df_clean.sort_values(by='Assists', ascending=False).iloc[0]

    col_g, col_a = st.columns(2)
    with col_g:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.1s;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">⚽</div>
            <div class="card-title">Top Scorer</div>
            <div class="card-value">{top_scorer['player_name']}</div>
            <div class="card-sub">{int(top_scorer['Goals'])} Goals this season</div>
        </div>
        """, unsafe_allow_html=True)
    with col_a:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; animation-delay: 0.2s;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🎯</div>
            <div class="card-title">Top Assists</div>
            <div class="card-value">{top_assist['player_name']}</div>
            <div class="card-sub">{int(top_assist['Assists'])} Assists this season</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🏆 Top Overall Stats (by xGI)</div>', unsafe_allow_html=True)
    df_xgi = analyze_data.top_stats(df_clean, top_n=10)
    # Restyle the dataframe
    st.dataframe(df_xgi, use_container_width=True)

    st.markdown('<div class="section-title">🔥 Top Attackers</div>', unsafe_allow_html=True)
    st.dataframe(analyze_data.top_attackers(df_clean, top_n=10), use_container_width=True)

    st.markdown('<div class="section-title">🧱 Top Defenders</div>', unsafe_allow_html=True)
    st.dataframe(analyze_data.top_defenders(df_clean, top_n=10), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 3: SQUAD
# ══════════════════════════════════════════════════════════════
with tab_squad:
    st.markdown('<div class="section-title">First Team Squad & Tactical Setup</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 20px;">Predicted XI — 4-2-3-1 Formation</p>', unsafe_allow_html=True)

    df_clean['Minutes Played'] = df_clean.apply(
        lambda x: (x['Appearances'] * 90) if (x['player_position'] == 'Goalkeeper' and (pd.isna(x.get('Minutes Played', 0)) or x.get('Minutes Played', 0) == 0)) else x.get('Minutes Played', 0),
        axis=1
    )

    df_active = df_clean[df_clean['Minutes Played'] > 0].copy()
    if 'Date of Birth' in df_active.columns:
        df_active['DOB'] = pd.to_datetime(df_active['Date of Birth'], format='%d/%m/%Y', errors='coerce')
        df_active['Age'] = datetime.now().year - df_active['DOB'].dt.year
    else:
        df_active['Age'] = pd.NA

    df_active['player_position'] = df_active['player_position'].replace('Attacker', 'Forward')

    def get_p(name):
        res = df_active[df_active['player_name'] == name]
        if not res.empty:
            img = res.iloc[0]['player_image_url']
            short_name = name.split()[-1] if len(name.split()) > 1 else name
            return short_name, img if pd.notna(img) else "https://resources.premierleague.com/premierleague25/photos/players/110x140/placeholder.png"
        return name, "https://resources.premierleague.com/premierleague25/photos/players/110x140/placeholder.png"

    n_st, i_st = get_p("Nicolas Jackson")
    n_lw, i_lw = get_p("Pedro Neto")
    n_am, i_am = get_p("Cole Palmer")
    n_rw, i_rw = get_p("Noni Madueke")
    n_cm1, i_cm1 = get_p("Enzo Fernández")
    n_cm2, i_cm2 = get_p("Moisés Caicedo")
    n_lb, i_lb = get_p("Marc Cucurella")
    n_cb1, i_cb1 = get_p("Levi Colwill")
    n_cb2, i_cb2 = get_p("Wesley Fofana")
    n_rb, i_rb = get_p("Malo Gusto")
    n_gk, i_gk = get_p("Robert Sánchez")

    xi_names = ["Nicolas Jackson", "Pedro Neto", "Cole Palmer", "Noni Madueke", "Enzo Fernández", "Moisés Caicedo", "Marc Cucurella", "Levi Colwill", "Wesley Fofana", "Malo Gusto", "Robert Sánchez"]
    df_subs = df_active[~df_active['player_name'].isin(xi_names)].sort_values(by='Minutes Played', ascending=False)

    subs_html = ""
    for _, row in df_subs.iterrows():
        img = row['player_image_url'] if pd.notna(row['player_image_url']) else "https://resources.premierleague.com/premierleague25/photos/players/110x140/placeholder.png"
        subs_html += f"""
        <div class="sub-row">
            <img src="{img}">
            <div class="sub-details">
                <div class="sub-name">{row['player_name']}</div>
                <div class="sub-stat">{row['player_position']} • {int(row['Minutes Played'])} mins</div>
            </div>
        </div>
        """

    tactics_iframe = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; background: transparent; }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        @keyframes pulseGlow {{ 0%,100% {{ box-shadow: 0 0 8px rgba(3,70,148,0.3); }} 50% {{ box-shadow: 0 0 24px rgba(3,70,148,0.6); }} }}
        @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
        @keyframes shimmer {{ 0% {{ background-position: -200% 0; }} 100% {{ background-position: 200% 0; }} }}
        .tactics-box {{ display: flex; gap: 20px; background: linear-gradient(135deg, rgba(30,34,53,0.85), rgba(15,17,23,0.95)); backdrop-filter: blur(20px); border-radius: 16px; padding: 20px; border: 1px solid rgba(45,51,97,0.4); animation: fadeInUp 0.6s ease-out; box-sizing: border-box; }}
        .field {{ flex: 2; background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 30%, #388e3c 70%, #1b5e20 100%); border: 2px solid rgba(255,255,255,0.15); border-radius: 8px; height: 540px; position: relative; display: flex; flex-direction: column; justify-content: space-evenly; padding: 10px 0; overflow: hidden; box-sizing: border-box; }}
        .field::before {{ content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent, transparent 8%, rgba(255,255,255,0.03) 8%, rgba(255,255,255,0.03) 16%); pointer-events: none; }}
        .field-lines {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; }}
        .center-circle {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100px; height: 100px; border: 2px solid rgba(255,255,255,0.25); border-radius: 50%; box-sizing: border-box; }}
        .center-circle::after {{ content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 6px; height: 6px; background: rgba(255,255,255,0.3); border-radius: 50%; }}
        .halfway-line {{ position: absolute; top: 50%; width: 100%; height: 1.5px; background: rgba(255,255,255,0.2); }}
        .pen-area-top {{ position: absolute; top: 0; left: 22%; width: 56%; height: 14%; border: 2px solid rgba(255,255,255,0.2); border-top: none; box-sizing: border-box; border-radius: 0 0 6px 6px; }}
        .pen-area-bot {{ position: absolute; bottom: 0; left: 22%; width: 56%; height: 14%; border: 2px solid rgba(255,255,255,0.2); border-bottom: none; box-sizing: border-box; border-radius: 6px 6px 0 0; }}
        .tactics-row {{ display: flex; justify-content: center; align-items: center; gap: 20px; z-index: 10; position: relative; }}
        .player-icon {{ text-align: center; color: white; width: 76px; animation: fadeInUp 0.5s ease-out both; }}
        .player-icon:nth-child(1) {{ animation-delay: 0.1s; }}
        .player-icon:nth-child(2) {{ animation-delay: 0.2s; }}
        .player-icon:nth-child(3) {{ animation-delay: 0.3s; }}
        .player-icon:nth-child(4) {{ animation-delay: 0.4s; }}
        .player-icon img {{ width: 48px; height: 48px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.8); object-fit: cover; background: #111; box-shadow: 0 4px 12px rgba(0,0,0,0.5), 0 0 0 3px rgba(3,70,148,0.3); transition: all 0.3s ease; animation: pulseGlow 3s ease-in-out infinite; }}
        .player-icon:hover img {{ transform: scale(1.15); border-color: #034694; }}
        .player-icon div {{ font-size: 11px; font-weight: 600; text-shadow: 0 1px 4px #000; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .bench {{ flex: 1; background: rgba(15,17,23,0.6); border: 1px solid rgba(45,51,97,0.3); border-radius: 10px; padding: 16px; height: 540px; overflow-y: auto; box-sizing: border-box; }}
        .bench h4 {{ margin-top: 0; color: #e0e0e0; border-bottom: 1px solid rgba(45,51,97,0.4); padding-bottom: 12px; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }}
        .sub-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; padding: 8px; background: rgba(30,34,53,0.4); border-radius: 8px; border: 1px solid rgba(45,51,97,0.2); transition: all 0.2s ease; animation: fadeInUp 0.3s ease-out both; }}
        .sub-row:hover {{ background: rgba(3,70,148,0.12); border-color: rgba(3,70,148,0.4); transform: translateX(3px); }}
        .sub-row img {{ width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(45,51,97,0.4); }}
        .sub-details {{ display: flex; flex-direction: column; }}
        .sub-name {{ font-weight: 600; font-size: 13px; color: #e0e0e0; }}
        .sub-stat {{ font-size: 11px; color: #6b7280; }}
        .bench::-webkit-scrollbar {{ width: 4px; }}
        .bench::-webkit-scrollbar-track {{ background: transparent; }}
        .bench::-webkit-scrollbar-thumb {{ background: rgba(45,51,97,0.5); border-radius: 2px; }}
    </style>
    <div class="tactics-box">
        <div class="field">
            <div class="field-lines">
                <div class="center-circle"></div>
                <div class="halfway-line"></div>
                <div class="pen-area-top"></div>
                <div class="pen-area-bot"></div>
            </div>
            <div class="tactics-row" style="animation-delay:0s;"><div class="player-icon"><img src="{i_st}"><div>{n_st}</div></div></div>
            <div class="tactics-row" style="gap:40px;">
                <div class="player-icon"><img src="{i_lw}"><div>{n_lw}</div></div>
                <div class="player-icon"><img src="{i_am}"><div>{n_am}</div></div>
                <div class="player-icon"><img src="{i_rw}"><div>{n_rw}</div></div>
            </div>
            <div class="tactics-row" style="gap:60px;">
                <div class="player-icon"><img src="{i_cm1}"><div>{n_cm1}</div></div>
                <div class="player-icon"><img src="{i_cm2}"><div>{n_cm2}</div></div>
            </div>
            <div class="tactics-row" style="gap:16px;">
                <div class="player-icon"><img src="{i_lb}"><div>{n_lb}</div></div>
                <div class="player-icon"><img src="{i_cb1}"><div>{n_cb1}</div></div>
                <div class="player-icon"><img src="{i_cb2}"><div>{n_cb2}</div></div>
                <div class="player-icon"><img src="{i_rb}"><div>{n_rb}</div></div>
            </div>
            <div class="tactics-row" style="animation-delay:0s;"><div class="player-icon"><img src="{i_gk}"><div>{n_gk}</div></div></div>
        </div>
        <div class="bench">
            <h4>🧑‍🤝‍🧑 Substitutes</h4>
            {subs_html}
        </div>
    </div>
    """
    components.html(tactics_iframe, height=580, scrolling=False)

    # Full Squad Profiles
    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Full Squad Profiles</div>', unsafe_allow_html=True)

    col_sq_left, col_sq_right = st.columns(2)

    def render_player_cards(df, positions, section_title):
        st.markdown(f"<h4 style='color: #d1d5db; margin: 20px 0 12px 0; font-size: 0.95rem; font-weight: 600; border-bottom: 1px solid rgba(45,51,97,0.3); padding-bottom: 6px;'>{section_title}</h4>", unsafe_allow_html=True)
        df_f = df[df['player_position'].isin(positions)].sort_values(by='Minutes Played', ascending=False)
        for i, (_, row) in enumerate(df_f.iterrows()):
            img_url = row['player_image_url'] if pd.notna(row['player_image_url']) else "https://resources.premierleague.com/premierleague25/photos/players/110x140/placeholder.png"
            age_str = f"{int(row['Age'])} yrs" if pd.notna(row['Age']) else "N/A"
            st.markdown(f"""
            <div class="player-card" style="animation-delay: {0.05 * i}s;">
                <img src="{img_url}" onerror="this.src='https://resources.premierleague.com/premierleague25/photos/players/110x140/placeholder.png'">
                <div>
                    <div class="pname">{row['player_name']}</div>
                    <div class="pmeta">{age_str} • {row['Nationality']}</div>
                    <div class="pmins">⏱️ {int(row['Minutes Played'])} mins played</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_sq_left:
        render_player_cards(df_active, ['Forward'], "Forwards")
        render_player_cards(df_active, ['Goalkeeper'], "Goalkeepers")
    with col_sq_right:
        render_player_cards(df_active, ['Midfielder'], "Midfielders")
        render_player_cards(df_active, ['Defender'], "Defenders")

# ══════════════════════════════════════════════════════════════
# TAB 4: ANALYTICS
# ══════════════════════════════════════════════════════════════
with tab_analytics:
    st.markdown('<div class="section-title">Visual Performance Analytics — 10 Key Benchmarking Metrics</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 24px;">Data-driven insights comparing Chelsea against Premier League benchmarks</p>', unsafe_allow_html=True)

    # ROW 1
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">1. Perjalanan Klasemen — Trend Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_all_gws.empty:
            df_trend = df_all_gws[df_all_gws['name'].isin(['Chelsea', 'Arsenal', 'Liverpool', 'Manchester City'])]
            fig1 = px.line(df_trend, x="gameweek", y="position", color="name", markers=True)
            fig1.update_yaxes(autorange="reversed", dtick=1, title_text="Position")
            fig1.update_xaxes(title_text="Gameweek")
            for d in fig1.data:
                if d.name == 'Chelsea':
                    d.line.width = 4; d.line.color = '#034694'
                else:
                    d.line.dash = 'dot'; d.line.width = 1.5
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>📈 <b>Insight:</b> Chelsea berhasil menjaga momentum stabil untuk mengamankan tiket zona Liga Champions sejak GW 20.</div>""", unsafe_allow_html=True)

    with col_a2:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">2. Analisis Momentum Gol</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_all_gws.empty:
            df_ct = df_all_gws[df_all_gws['name'] == 'Chelsea'].sort_values('gameweek')
            fig2 = go.Figure(data=[
                go.Bar(name='Goals Scored', x=df_ct['gameweek'], y=df_ct['goals_for'], marker_color='#034694', marker_line=dict(color='#0058b0', width=1)),
                go.Bar(name='Goals Conceded', x=df_ct['gameweek'], y=df_ct['goals_against'], marker_color='#ff4b4b', marker_line=dict(color='#ff6b6b', width=1))
            ])
            fig2.update_layout(barmode='group', xaxis_title="Gameweek", yaxis_title="Goals")
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>⚖️ <b>Insight:</b> Rasio produktivitas gol meningkat tajam di paruh kedua musim pertandingan.</div>""", unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # ROW 2
    col_a3, col_a4 = st.columns(2)
    with col_a3:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">3. Efektivitas Taktis Serangan Klub — League Benchmark</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_club_stats.empty:
            fig3 = px.scatter(df_club_stats, x="XG", y="Goals", text="club_name", size="Passes", color="Goals",
                             color_continuous_scale="Blues")
            fig3.add_shape(type='line', x0=30, y0=30, x1=90, y1=90, line=dict(color='rgba(255,255,255,0.2)', dash='dash', width=1))
            fig3.update_traces(textposition='top center', textfont=dict(size=10))
            fig3.update_layout(xaxis_title="Expected Goals (xG)", yaxis_title="Actual Goals")
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>🎯 <b>Klub Benchmark:</b> Kualitas xG Chelsea (69.19) sejajar dengan klub papan atas, namun defisit konversi (-5.19) mengindikasikan inefisiensi lini depan.</div>""", unsafe_allow_html=True)

    with col_a4:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">4. Distribusi Keterlibatan Gol Skuad</div>
        </div>
        """, unsafe_allow_html=True)
        df_contrib = df_clean[df_clean['GA'] > 0]
        if not df_contrib.empty:
            colors_pie = ['#034694', '#00b4d8', '#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff', '#c084fc', '#ff6b9d']
            fig4 = px.pie(df_contrib, values='GA', names='player_name', hole=0.45, color_discrete_sequence=colors_pie)
            fig4.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(size=11, color='#fff'),
                              marker=dict(line=dict(color='#0f1117', width=2)))
            fig4.update_layout(showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>🍕 <b>Insight:</b> Cole Palmer menyumbang porsi dominan (26.4%) dari total kontribusi gol — menandakan dependensi taktis yang tinggi.</div>""", unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # ROW 3
    col_a5, col_a6 = st.columns(2)
    with col_a5:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">5. Profiling Ancaman Pemain — xG90 vs xA90</div>
        </div>
        """, unsafe_allow_html=True)
        df_threat = df_clean[df_clean['Minutes Played'] > 500]
        if not df_threat.empty:
            fig5 = px.scatter(df_threat, x="xA90", y="xG90", text="player_name", color="xGI90", size="Minutes Played",
                             color_continuous_scale="Blues")
            fig5.add_hline(y=df_threat['xG90'].mean(), line_dash="dot", line_color="rgba(255,255,255,0.2)")
            fig5.add_vline(x=df_threat['xA90'].mean(), line_dash="dot", line_color="rgba(255,255,255,0.2)")
            fig5.update_traces(textposition='bottom center', textfont=dict(size=10))
            fig5.update_layout(xaxis_title="xA per 90", yaxis_title="xG per 90")
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>⚔️ <b>Insight:</b> Kuadran kanan atas menunjukkan Cole Palmer berada di kelas elit sebagai pencipta sekaligus penyelesai peluang terbaik.</div>""", unsafe_allow_html=True)

    with col_a6:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">6. Konversi Gol Individu — Over/Under xG Performance</div>
        </div>
        """, unsafe_allow_html=True)
        df_fin = df_clean[df_clean['Minutes Played'] > 300].copy()
        if not df_fin.empty:
            df_fin['xG_Diff'] = df_fin['Goals'] - df_fin['XG']
            fig6 = px.bar(df_fin.sort_values('xG_Diff'), x='xG_Diff', y='player_name', orientation='h', color='xG_Diff',
                         color_continuous_scale='RdBu', range_color=[-3, 3])
            fig6.update_layout(xaxis_title="Goals - xG Differential", yaxis_title=None, height=400)
            fig6.update_yaxes(tickfont=dict(size=10))
            st.plotly_chart(fig6, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>📉 <b>Insight:</b> Noni Madueke dan Nicolas Jackson mencatatkan angka minus terbesar, menegaskan masalah penyelesaian akhir peluang matang.</div>""", unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # ROW 4
    col_a7, col_a8 = st.columns(2)
    with col_a7:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">7. Komparasi Kreativitas Sayap — League Winger Benchmark</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_league.empty:
            df_wingers = df_league[(df_league['player_position'] == 'Forward') & (df_league['Minutes Played'] > 500)].copy()
            df_wingers['Is_Chelsea'] = df_wingers['player_club'].apply(lambda x: 'Chelsea' if x == 'Chelsea' else 'Other PL')
            fig7 = px.scatter(df_wingers, x='Dribble90', y='xA90', color='Is_Chelsea', size='Minutes Played', text='player_name',
                             color_discrete_map={'Chelsea': '#034694', 'Other PL': '#4b5563'})
            fig7.update_traces(textposition='top center', textfont=dict(size=9))
            fig7.update_layout(xaxis_title="Dribbles per 90", yaxis_title="xA per 90")
            st.plotly_chart(fig7, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>🏃‍♂️ <b>Moneyball Benchmark:</b> Pemain sayap Chelsea memiliki volume dribel tinggi, namun efisiensi konversi xA90 masih kalah bernilai dibanding penyerang sayap tim papan tengah lainnya.</div>""", unsafe_allow_html=True)

    with col_a8:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">8. Efisiensi Umpan Silang Klub — Cross Volume vs Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_club_stats.empty:
            fig8 = px.scatter(df_club_stats, x='crosses', y='cross_accuracy', text='club_name', size='Goals', color='cross_accuracy',
                             color_continuous_scale='Blues')
            fig8.add_hline(y=df_club_stats['cross_accuracy'].mean(), line_dash="dash", line_color="rgba(255,255,255,0.3)")
            fig8.update_traces(textposition='top center', textfont=dict(size=9))
            fig8.update_layout(xaxis_title="Total Crosses", yaxis_title="Cross Accuracy (%)")
            st.plotly_chart(fig8, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>📐 <b>Klub Benchmark:</b> Chelsea melepas 463 crosses dengan akurasi 22% — tepat di rata-rata liga, menunjukkan skema serangan sayap yang cukup standar.</div>""", unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # ROW 5
    col_a9, col_a10 = st.columns(2)
    with col_a9:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">9. Gelandang Pengangkut Air — Elite Defensive Midfielder Benchmark</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_league.empty:
            df_dms = df_league[(df_league['player_position'] == 'Midfielder') & (df_league['Minutes Played'] > 800)].copy()
            df_dms['Is_Chelsea'] = df_dms['player_club'].apply(lambda x: 'Chelsea' if x == 'Chelsea' else 'Other PL')
            fig9 = px.scatter(df_dms, x='Interceptions90', y='Tackles90', color='Is_Chelsea', text='player_name', size='Duels Won',
                             color_discrete_map={'Chelsea': '#034694', 'Other PL': '#4b5563'})
            fig9.update_traces(textposition='top left', textfont=dict(size=9))
            fig9.update_layout(xaxis_title="Interceptions per 90", yaxis_title="Tackles per 90")
            st.plotly_chart(fig9, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>🛡️ <b>Pemain Benchmark:</b> Moisés Caicedo terbukti berada di kuadran elit Premier League untuk volume pemutusan serangan lawan — salah satu gelandang bertahan paling efektif di Eropa.</div>""", unsafe_allow_html=True)

    with col_a10:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 16px;">
            <div class="card-title">10. Indeks Kedisiplinan — League Aggression</div>
        </div>
        """, unsafe_allow_html=True)
        if not df_league.empty:
            df_agg = df_league.sort_values(by='Fouls', ascending=False).head(25)
            fig10 = px.bar(df_agg, x='player_name', y='Fouls', color='player_club',
                          title=None, color_discrete_sequence=px.colors.qualitative.Set2)
            fig10.update_layout(xaxis_title=None, yaxis_title="Total Fouls", xaxis_tickangle=-45)
            st.plotly_chart(fig10, use_container_width=True)
            st.markdown("""<div class='analytic-desc'>🟨 <b>Pemain Benchmark:</b> Lini tengah Chelsea (Caicedo) tercatat masuk daftar teratas pemain dengan pelanggaran terbanyak — konsekuensi intensitas pressing tinggi.</div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # KESIMPULAN STRATEGIS — GRAND FINALE
    # ══════════════════════════════════════════════════════════
    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="report-card">
        <h2>📋 Laporan Evaluasi Skuad & Strategi Rekrutmen Berbasis Moneyball 24/25</h2>
        <div style="margin-bottom: 20px;">
            <h4>1. Evaluasi Taktikal & Rekomendasi Formasi Berdasarkan Data</h4>
            <p>Data volume operan (19.796 umpan) dan kontribusi progresi bola dari Colwill dan Enzo membuktikan bahwa taktik <b>4-2-3-1 Berbasis Penguasaan Bola (Possession)</b> adalah fondasi terbaik tim. Masalah utama terletak pada beban kreativitas sepertiga akhir yang 100% bertumpu pada Cole Palmer. Rekomendasi taktis untuk musim depan adalah menerapkan skema hibrida <b>4-3-3 Inverted Winger</b>, yang memberikan kebebasan bagi gelandang bertahan untuk naik melakukan <i>counter-pressing</i> tinggi demi memaksimalkan konversi peluang.</p>
        </div>
        <div style="margin-bottom: 20px;">
            <h4>2. Analisis Efisiensi & Konversi Peluang Klub</h4>
            <p>Metrik komparatif klub pada <b>Analisis 3 & 6</b> membuktikan adanya inefisiensi masif di lini depan. Skuad Chelsea menghasilkan xG setara dengan penantang gelar juara, namun defisit konversi aktual (-5.19) membuat tim kehilangan poin penting. Dalam kacamata <i>Moneyball</i>, kita tidak boleh mempertahankan pemain berharga pasar tinggi yang terus-menerus membuang nilai probabilitas gol (xG) mereka tanpa adanya grafik pertumbuhan performa.</p>
        </div>
        <div>
            <h4>3. Strategi Bursa Transfer Berbasis Konsep Moneyball</h4>
            <p>Esensi utama <i>Moneyball</i> adalah memaksimalkan efisiensi anggaran dengan mengategorikan pemain secara objektif berdasarkan kontribusi statistik murni dan nilai pasar:</p>
            <ul>
                <li><span class="tag-keep">PERTAHANKAN</span> <b>Cole Palmer</b> (xGI90 0.75), <b>Moisés Caicedo</b> (Gelandang bertahan elit), <b>Enzo Fernández</b> (Distributor utama), dan <b>Nicolas Jackson</b> (Magnet xG, pergerakan tanpa bola membuka ruang).</li>
                <li><span class="tag-sell">DIJUAL DEMI PROFIT</span> <b>Noni Madueke</b> — defisit konversi terbesar (-2.64 xG), nilai pasar sedang puncak.<br>🔄 <i>Target pengganti:</i> <b>Bryan Mbeumo</b> (Brentford) atau <b>Simon Adingra</b> (Brighton) — efisiensi xGI90 stabil dengan harga kompetitif.</li>
                <li><span class="tag-urgent">JUAL SEGERA</span> <b>Kiernan Dewsbury-Hall</b> (xGI90 0.16) → ganti <b>Adam Wharton</b> atau <b>Alex Iwobi</b>. <b>Badiashile & Chalobah</b> (surplus, skor defensif rendah) → ganti <b>Ethan Pinnock</b> atau <b>Murillo</b>.</li>
                <li><span class="tag-loan">PINJAMKAN</span> <b>Mykhailo Mudryk</b>, <b>Marc Guiu</b>, <b>Tyrique George</b> — bakat mentah tinggi tapi minim menit bermain. Pinjam ke klub Premier League tekanan rendah atau Bundesliga untuk matangkan potensi.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="footer-glass">
        Dashboard Portofolio Data Analyst • Rifaldi W Analytics • © 2024/2025
    </div>
""", unsafe_allow_html=True)

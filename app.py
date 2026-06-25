import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MacroLens",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; font-size: 2.5rem; }
    h2 { color: #00d4ff; }
    h3 { color: #ffffff; }
    p { color: #cccccc; }
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e, #252d40);
        border: 1px solid #00d4ff33;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .hawkish { color: #ff4d4d; font-size: 1.5rem; font-weight: bold; }
    .dovish { color: #00d4ff; font-size: 1.5rem; font-weight: bold; }
    .neutral { color: #ffaa00; font-size: 1.5rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    with open("fomc_data.json") as f:
        fomc = json.load(f)
    fed_df = pd.read_csv("fed_rate.csv")
    return fomc, fed_df

try:
    fomc_data, fed_df = load_data()
except:
    st.error("Data not found. Please run: python3 analyzer.py")
    st.stop()

st.markdown("# 🔭 MacroLens")
st.markdown("### Federal Reserve Policy Sentiment Analyzer")
st.markdown("*Tracking hawkish vs dovish signals in FOMC transcripts and correlating them with interest rate decisions*")
st.divider()

dates = [d["date"] for d in fomc_data]
scores = [d["sentiment"] for d in fomc_data]
avg_score = round(sum(scores) / len(scores), 3)
latest_score = scores[-1]
latest_rate = fed_df["fed_rate"].iloc[-1]

if latest_score > 0.05:
    stance = "🦅 Hawkish"
    stance_class = "hawkish"
    stance_desc = "Fed leaning toward raising rates"
elif latest_score < -0.05:
    stance = "🕊️ Dovish"
    stance_class = "dovish"
    stance_desc = "Fed leaning toward cutting rates"
else:
    stance = "⚖️ Neutral"
    stance_class = "neutral"
    stance_desc = "Fed in wait and see mode"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#888; margin:0">Latest Sentiment</p>
        <p class="{stance_class}">{latest_score}</p>
        <p style="color:#888; font-size:0.8rem; margin:0">{stance_desc}</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#888; margin:0">Current Stance</p>
        <p class="{stance_class}">{stance}</p>
        <p style="color:#888; font-size:0.8rem; margin:0">Based on latest FOMC</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#888; margin:0">Fed Funds Rate</p>
        <p class="neutral">{latest_rate}%</p>
        <p style="color:#888; font-size:0.8rem; margin:0">Most recent reading</p>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#888; margin:0">FOMC Meetings</p>
        <p class="neutral">{len(fomc_data)}</p>
        <p style="color:#888; font-size:0.8rem; margin:0">Analyzed in 2024</p>
    </div>""", unsafe_allow_html=True)

st.divider()

fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("FOMC Sentiment Score Over Time", "Federal Funds Rate Over Time"),
    vertical_spacing=0.15
)

colors = ["#ff4d4d" if s > 0 else "#00d4ff" for s in scores]
fig.add_trace(
    go.Bar(
        x=dates,
        y=scores,
        marker_color=colors,
        name="Sentiment Score",
        hovertemplate="<b>%{x}</b><br>Sentiment: %{y}<extra></extra>"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=fed_df["date"],
        y=fed_df["fed_rate"],
        line=dict(color="#ffaa00", width=2),
        name="Fed Funds Rate",
        hovertemplate="<b>%{x}</b><br>Rate: %{y}%<extra></extra>"
    ),
    row=2, col=1
)

fig.update_layout(
    height=600,
    paper_bgcolor="#0e1117",
    plot_bgcolor="#1a1f2e",
    font=dict(color="#cccccc"),
    showlegend=False,
    margin=dict(t=60, b=20)
)
fig.update_xaxes(gridcolor="#333", zeroline=False)
fig.update_yaxes(gridcolor="#333", zeroline=True, zerolinecolor="#555")

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### 📋 FOMC Meeting Breakdown")

for item in reversed(fomc_data):
    score = item["sentiment"]
    if score > 0.05:
        label = "🦅 Hawkish"
        color = "#ff4d4d"
    elif score < -0.05:
        label = "🕊️ Dovish"
        color = "#00d4ff"
    else:
        label = "⚖️ Neutral"
        color = "#ffaa00"

    top_words = ", ".join([w[0] for w in item["top_words"][:5]])

    with st.expander(f"{item['date']}  —  {label}  —  Score: {score}"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Sentiment Score:** <span style='color:{color}'>{score}</span>", unsafe_allow_html=True)
            st.markdown(f"**Policy Stance:** <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Top Keywords:** {top_words}")
            st.markdown(f"**Transcript Length:** {item['text_length']:,} characters")

st.divider()
st.markdown("""
<p style='text-align:center; color:#555; font-size:0.8rem'>
MacroLens — Built by Diya Shah | Rutgers University, BS Data Science & BA Economics<br>
Data: Federal Reserve FOMC Transcripts + FRED API
</p>
""", unsafe_allow_html=True)

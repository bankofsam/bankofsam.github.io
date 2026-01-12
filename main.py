import json
import base64
from pathlib import Path
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# 1. Full width with Streamlit chrome hidden
st.set_page_config(page_title="Bank of Sam — SAMBUCKS", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root { --bankofsam-bg: #06140b; }
html, body, .stApp { background: var(--bankofsam-bg) !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"], header, footer { display: none !important; }
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe[title="st.iframe"] { display: block; margin: 0; background: transparent; }
</style>
""", unsafe_allow_html=True)

# 2. Data Setup
def load_sam_data_url():
    p = Path(__file__).parent / "sam.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAmMB4hQq9XcAAAAASUVORK5CYII="

sam_data_url = load_sam_data_url()

def load_feed():
    return {
        "stories": [
            {"title":"Alex Coin completely valueless", "body":"DO NOT INVEST IN ALEX COIN"},
            {"title":"Robo hedger toggles on", "body":"Latency improved to probably fine"},
            {"title":"Balance sheet very green", "body":"Analysts upgrade outlook to moonish"},
            {"title":"Checking flood of deposits", "body":"Customers embrace new high-yield fling"},
            {"title":"ATM queues shrink overnight", "body":"Bank credits speed boosts to app"},
            {"title":"Loan approvals go brrr", "body":"Underwriting says 'we like the vibes'"},
        ],
        "names": ["Sam A", "Jamie Q", "Taylor Q", "Jordan K", "Avery P", "Riley M", "Casey D", "Morgan L"]
    }

feed = load_feed()
rng = np.random.default_rng(7)
tickers = [f"SAM{i:02d}" for i in range(1, 11)]
start_prices = np.round(rng.uniform(4, 250, len(tickers)), 2).tolist()
vols = np.round(rng.uniform(0.2, 2.0, len(tickers)), 2).tolist()

payload = {
    "theme": "green", "logo": sam_data_url, "tickers": tickers,
    "prices": start_prices, "vols": vols, "stories": feed["stories"], "names": feed["names"]
}

# 3. The HTML (Restoring the animations and adding the centered pop-up)
HTML = f"""
<!DOCTYPE html>
<html>
<head>
<style>
:root {{
  --g1: #0b2f1a; --g2: #0e5a2f; --g3: #16a34a;
  --panel: rgba(255,255,255,0.06); --panel2: rgba(0,0,0,0.3);
  --border: rgba(255,255,255,0.12); --text: #eaf6ec;
  --muted: #b6d6bf; --up: #19e57a; --down: #ff5b4d; --accent: #b4ff6b;
}}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:#06140b; color:var(--text); font-family: Verdana, Arial, sans-serif; }}
.wrap {{ width: 1120px; margin: 0 auto; }}

.topbar {{ background: linear-gradient(180deg, var(--g3), var(--g2) 60%, var(--g1)); border-bottom: 3px solid #000; padding: 10px 0; }}
.brand {{ display:flex; align-items:center; gap:14px; padding:0 12px; }}
.brand img {{ height:44px; border:2px solid rgba(255,255,255,0.2); }}
.navbar {{ background: rgba(0,0,0,0.4); display:flex; gap:18px; padding:6px 10px; font-size:13px; border-bottom:1px solid #000; }}
.navbtn {{ padding:5px 10px; border:1px solid rgba(255,255,255,0.25); background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(0,0,0,0.3)); cursor:pointer; }}

.grid {{ display:grid; grid-template-columns: 260px 1fr 320px; gap:14px; margin-top:12px; }}
.panel {{ background: linear-gradient(180deg, var(--panel), var(--panel2)); border:1px solid var(--border); }}
.hdr {{ padding:6px 10px; background: rgba(255,255,255,0.1); font-weight:700; border-bottom: 1px solid #000; }}

.table {{ width:100%; border-collapse:collapse; font-size:12px; }}
.table td {{ padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); }}
.green {{ color: var(--up); }} .red {{ color: var(--down); }}

/* ANIMATED PULSE LOGO */
.pulse-logo {{
  position:absolute; right:10px; top:6px; width:18px; height:18px;
  background: url('{payload["logo"]}') center/contain no-repeat;
  animation: pl 2.2s ease-in-out infinite;
}}
@keyframes pl {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.2); }} 100% {{ transform: scale(1); }} }}

/* CENTERED POPUP STYLES */
.alert-overlay {{
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.7); z-index: 999998; display: none;
}}
.alert-popup {{
  position: fixed !important; top: 50% !important; left: 50% !important;
  transform: translate(-50%, -50%); width: 350px;
  background: linear-gradient(135deg, #0b2f1a, #06140b);
  border: 3px solid var(--accent); color: var(--text);
  padding: 25px; border-radius: 12px; text-align: center;
  z-index: 999999; display: none; box-shadow: 0 0 40px rgba(180,255,107,0.4);
}}
</style>
</head>
<body>

<div id="alertOverlay" class="alert-overlay"></div>
<div id="alertBubble" class="alert-popup">
  <div id="alertText" style="margin-bottom:20px;"></div>
  <button onclick="closeAlert()" style="background:var(--accent); border:none; padding:8px 20px; cursor:pointer; font-weight:bold;">ACKNOWLEDGE</button>
</div>

<div class="topbar"><div class="wrap"><div class="brand"><img src="{payload['logo']}"><div style="font-weight:700; font-size:22px;">Bank of Sam — SAMBUCKS</div></div></div></div>

<div class="wrap">
  <div class="grid">
    <div class="panel"><div class="hdr">WATCHLIST</div><div id="watch" style="padding:10px;"></div></div>
    <div class="panel">
      <div class="hdr">LIVE CHART</div>
      <div style="padding:8px;"><canvas id="chart" width="680" height="280" style="width:100%; background:#07150b; border:1px solid #111;"></canvas></div>
      <div class="hdr">ORDER FLOW</div>
      <div style="padding:8px; max-height:260px; overflow:auto;"><table class="table" id="blotter"><tbody></tbody></table></div>
    </div>
    <div class="panel">
      <div class="hdr">OTHER NEWS</div>
      <div style="padding:10px; font-size:12px;"><b>Research Headline</b><br>Outlook remains very green.<hr style="border-color:#222"><b>Whale Alert</b><br>Large buy on SAM01.</div>
    </div>
  </div>
</div>

<script>
const SEED = {json.dumps(payload)};
function fmt(n) {{ return Number(n).toFixed(2); }}

// 1. WATCHLIST
function buildWatch() {{
  const tb = document.getElementById("watch");
  let h = '<table class="table">';
  SEED.tickers.forEach((t, i) => {{ h += `<tr><td>${{t}}</td><td class="green">$${{fmt(SEED.prices[i])}}</td></tr>`; }});
  tb.innerHTML = h + '</table>';
}}

// 2. LIVE CHART
const canvas = document.getElementById("chart");
const ctx = canvas.getContext("2d");
let series = Array.from({{length: 50}}, () => 100);
function drawChart() {{
  ctx.clearRect(0,0,680,280);
  ctx.strokeStyle = "#19e57a"; ctx.lineWidth = 2;
  ctx.beginPath();
  series.forEach((v, i) => {{ ctx.lineTo(i*14, 280-v); }});
  ctx.stroke();
  series.push(Math.max(10, series[series.length-1] + (Math.random()-0.5)*20));
  if(series.length > 50) series.shift();
  requestAnimationFrame(drawChart);
}}

// 3. ALERT LOGIC
function showPop() {{
  const alerts = ["<b>MARKET MOVE:</b> SAM01 surged +15%!", "<b>VIBE CHECK:</b> Sentiment is MOONISH."];
  document.getElementById("alertText").innerHTML = alerts[Math.floor(Math.random()*alerts.length)];
  document.getElementById("alertOverlay").style.display = "block";
  document.getElementById("alertBubble").style.display = "block";
}}
function closeAlert() {{
  document.getElementById("alertOverlay").style.display = "none";
  document.getElementById("alertBubble").style.display = "none";
}}

buildWatch();
drawChart();
setTimeout(showPop, 4000);
</script>
</body>
</html>
"""

components.html(HTML, height=1200, scrolling=True)

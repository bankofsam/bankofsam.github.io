import json
import base64
from pathlib import Path
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="Bank of Sam — SAMBUCKS", layout="wide", initial_sidebar_state="collapsed")

# 2. Hide Streamlit UI
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

# 3. Logo Setup
def load_sam_data_url():
    p = Path(__file__).parent / "sam.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAmMB4hQq9XcAAAAASUVORK5CYII="

sam_logo = load_sam_data_url()

# 4. Data Setup
payload = {
    "logo": sam_logo,
    "tickers": [f"SAM{i:02d}" for i in range(1, 11)],
    "prices": [np.random.uniform(10, 200) for _ in range(10)],
    "stories": [
        {"title":"Alex Coin completely valueless", "body":"DO NOT INVEST IN ALEX COIN"},
        {"title":"Robo hedger toggles on", "body":"Latency improved to probably fine"},
        {"title":"Balance sheet very green", "body":"Analysts upgrade outlook to moonish"},
        {"title":"Checking flood of deposits", "body":"Customers embrace new high-yield fling"}
    ]
}

# 5. The HTML Block (Carefully escaped for Python)
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
body {{ margin:0; background:#06140b; color:var(--text); font-family: Verdana, sans-serif; }}
.wrap {{ width: 1120px; margin: 0 auto; }}
.topbar {{ background: linear-gradient(180deg, var(--g3), var(--g2) 60%, var(--g1)); border-bottom: 3px solid #000; padding: 10px; }}
.navbar {{ background: rgba(0,0,0,0.4); display:flex; gap:15px; padding:8px; font-size:12px; border-bottom:1px solid #000; }}
.navbtn {{ border:1px solid rgba(255,255,255,0.3); padding:4px 8px; cursor:pointer; }}
.grid {{ display:grid; grid-template-columns: 260px 1fr 320px; gap:15px; margin-top:15px; }}
.panel {{ background: linear-gradient(180deg, var(--panel), var(--panel2)); border:1px solid var(--border); }}
.hdr {{ background: rgba(255,255,255,0.1); padding:8px; font-weight:bold; border-bottom:1px solid #000; }}

/* Alert Bubble Styles */
#alertBubble {{
  position: fixed; bottom: 30px; right: 30px; width: 280px;
  background: linear-gradient(135deg, #16a34a, #0b2f1a);
  border: 2px solid var(--accent); color: white; padding: 15px;
  border-radius: 10px; z-index: 9999; display: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.7);
  animation: slideIn 0.5s ease-out;
}}
@keyframes slideIn {{ from {{ transform: translateX(120%); }} to {{ transform: translateX(0); }} }}
</style>
</head>
<body>

<div id="alertBubble">
  <span style="float:right; cursor:pointer;" onclick="this.parentElement.style.display='none'">×</span>
  <div id="alertText"><b>MARKET ALERT:</b> SAM01 is mooning!</div>
</div>

<div class="topbar">
  <div class="wrap"><b>Bank of Sam — SAMBUCKS</b></div>
</div>
<div class="navbar">
  <div class="wrap" style="display:flex; gap:15px;">
    <div class="navbtn">HOME</div><div class="navbtn">MARKETS</div><div class="navbtn">ACCOUNTS</div>
  </div>
</div>

<div class="wrap">
  <div class="grid">
    <div class="panel"><div class="hdr">WATCHLIST</div><div id="watch" style="padding:10px;">Loading...</div></div>
    <div class="panel"><div class="hdr">LIVE CHART</div><div style="height:300px; padding:20px; text-align:center;">[ Chart Active ]</div></div>
    <div class="panel">
      <div class="hdr">OTHER NEWS</div>
      <div style="padding:10px; font-size:12px;">
        <b>Research Headline</b><br>Outlook remains green.<hr>
        <b>Weather Bug</b><br>NYC vibes are Alpha.<hr>
        <b>Balance Sheet</b><br>Upgraded to moonish.
      </div>
    </div>
  </div>
</div>

<script>
const data = {json.dumps(payload)};
const alerts = [
  "<b>MARKET MOVE:</b> SAM01 surged +15%!",
  "<b>WHALE ALERT:</b> Large buy on SAM04.",
  "<b>VIBE CHECK:</b> Sentiment is MOONISH.",
  "<b>TECH ALERT:</b> Robo-hedger online."
];

function showPop() {{
  const b = document.getElementById("alertBubble");
  document.getElementById("alertText").innerHTML = alerts[Math.floor(Math.random()*alerts.length)];
  b.style.display = "block";
}}

// Initialize
setTimeout(showPop, 4000);
document.getElementById("watch").innerHTML = data.tickers.map((t,i) => `<div>${{t}}: $${{data.prices[i].toFixed(2)}}</div>`).join("");
</script>
</body>
</html>
"""

components.html(HTML, height=1000, scrolling=True)

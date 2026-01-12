import json
import base64
from pathlib import Path
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# full width with Streamlit chrome hidden
st.set_page_config(page_title="Bank of Sam — SAMBUCKS", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* app + page background forced dark so any gaps aren’t white */
:root { --bankofsam-bg: #06140b; }
html, body, .stApp { background: var(--bankofsam-bg) !important; }

/* nuke sidebar entirely */
[data-testid="stSidebar"] { display: none !important; }

/* fully remove the top header */
[data-testid="stHeader"] { display: none !important; }
header { display: none !important; }            
footer { display: none !important; }            

/* remove the default top padding/margins */
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }

/* make the component iframe not add any stray spacing */
iframe[title="st.iframe"] { display: block; margin: 0; background: transparent; }
</style>
""", unsafe_allow_html=True)

json_file = None
logo_file = None

def load_sam_data_url():
    if logo_file is not None:
        b = logo_file.read()
        return "data:image/png;base64," + base64.b64encode(b).decode("ascii")
    p = Path(__file__).parent / "sam.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAmMB4hQq9XcAAAAASUVORK5CYII="

sam_data_url = load_sam_data_url()

def load_feed():
    default = {
        "stories": [
            {"title":"Alex Coin completely valueless", "body":"DO NOT INVEST IN ALEX COIN"},
            {"title":"Robo hedger toggles on", "body":"Latency improved to probably fine"},
            {"title":"Balance sheet very green", "body":"Analysts upgrade outlook to moonish"},
            {"title":"Checking flood of deposits", "body":"Customers embrace new high-yield fling"},
            {"title":"ATM queues shrink overnight", "body":"Bank credits speed boosts to app"},
            {"title":"Loan approvals go brrr", "body":"Underwriting says 'we like the vibes'"},
        ],
        "names": ["Sam A", "Jamie Q", "Taylor Q", "Jordan K", "Avery P", "Riley M", "Casey D", "Morgan L", "Drew T", "Cameron J", "Reese F", "Peyton S"]
    }
    return default

feed = load_feed()
rng = np.random.default_rng(7)
tickers = [f"SAM{i:02d}" for i in range(1, 11)]
start_prices = np.round(rng.uniform(4, 250, len(tickers)), 2).tolist()
vols = np.round(rng.uniform(0.2, 2.0, len(tickers)), 2).tolist()

payload = {
    "theme": "green",
    "logo": sam_data_url,
    "tickers": tickers,
    "prices": start_prices,
    "vols": vols,
    "stories": feed["stories"],
    "names": feed["names"]
}

HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
:root {{
  --g1: #0b2f1a;
  --g2: #0e5a2f;
  --g3: #16a34a;
  --panel: rgba(255,255,255,0.06);
  --panel2: rgba(0,0,0,0.3);
  --border: rgba(255,255,255,0.12);
  --text: #eaf6ec;
  --muted: #b6d6bf;
  --up: #19e57a;
  --down: #ff5b4d;
  --accent: #b4ff6b;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#06140b; color:var(--text); font-family: Verdana, Arial, Helvetica, sans-serif; }}
.wrap {{ width: 1120px; margin: 0 auto; }}

.topbar {{
  background: linear-gradient(180deg, var(--g3), var(--g2) 60%, var(--g1));
  border-bottom: 3px solid #000;
  position: sticky; top: 0; z-index: 999;
  box-shadow: 0 4px 18px rgba(0,0,0,0.5);
}}
.brand {{ display:flex; align-items:center; gap:14px; padding:10px 12px; }}
.brand img {{ height:44px; border:2px solid rgba(255,255,255,0.2); box-shadow:0 2px 6px rgba(0,0,0,0.6); }}
.brand .title {{ font-weight:700; font-size:22px; letter-spacing:.5px; text-shadow:0 1px 0 #000; }}

.navbar {{
  background: linear-gradient(180deg, rgba(0,0,0,0.35), rgba(255,255,255,0.05));
  border-top:1px solid rgba(255,255,255,0.1); border-bottom:1px solid rgba(0,0,0,0.8);
  display:flex; gap:18px; padding:6px 10px; font-size:13px;
}}
.navbtn {{
  padding:5px 10px; border:1px solid rgba(255,255,255,0.25);
  background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(0,0,0,0.25));
  text-transform: uppercase; letter-spacing:.6px; cursor:pointer;
}}

.banner {{ display:grid; grid-template-columns: 1fr 280px; gap:14px; padding:10px 0 6px; }}
.breaking {{ background: linear-gradient(180deg, #0f3a21, #0b2a19); border:2px solid #000; position:relative; overflow:hidden; }}
.breaking .hdr {{ background:#000; color:#fff; font-weight:700; padding:4px 8px; font-size:12px; }}
.breaking .marquee {{ padding:6px 10px; white-space:nowrap; overflow:hidden; font-weight:600; }}

.ticker {{ background:#000; border-top:2px solid #1a1a1a; border-bottom:2px solid #1a1a1a; overflow:hidden; white-space:nowrap; font-size:13px; }}
.ticker-inner {{ display:inline-block; padding-left:100%; animation: ticker 18s linear infinite; }}
@keyframes ticker {{ 0% {{transform:translateX(0%);}} 100% {{transform:translateX(-100%);}} }}
.badge {{ display:inline-block; padding:3px 8px; margin:0 16px 0 0; background: linear-gradient(180deg, #1b1b1b, #2b2b2b); border:1px solid #444; }}

.grid {{ display:grid; grid-template-columns: 260px 1fr 320px; gap:14px; margin-top:12px; }}
.panel {{ background: linear-gradient(180deg, var(--panel), var(--panel2)); border:1px solid var(--border); }}
.panel .hdr {{ padding:6px 10px; background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(0,0,0,0.35)); font-weight:700; }}

.table {{ width:100%; border-collapse:collapse; font-size:12px; }}
.table th, .table td {{ border-bottom:1px solid rgba(255,255,255,0.08); padding:6px 8px; }}
.green {{ color: var(--up); }}
.red {{ color: var(--down); }}

/* --- NEW ALERT POPUP STYLES --- */
.alert-popup {{
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 280px;
  background: linear-gradient(135deg, #16a34a, #0b2f1a);
  border: 2px solid #b4ff6b;
  color: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.9);
  z-index: 10000;
  display: none; 
  font-size: 14px;
  animation: slideIn 0.5s ease-out;
}}
.close-alert {{
  position: absolute;
  top: 5px;
  right: 10px;
  cursor: pointer;
  font-weight: bold;
  font-size: 18px;
  color: #b4ff6b;
}}
@keyframes slideIn {{
  from {{ transform: translateX(120%); opacity: 0; }}
  to {{ transform: translateX(0); opacity: 1; }}
}}
</style>
</head>
<body>

  <div id="alertBubble" class="alert-popup">
    <span class="close-alert" onclick="closeAlert()">×</span>
    <div id="alertText"><b>MARKET ALERT:</b> SAM01 is mooning!</div>
  </div>

  <div class="topbar">
    <div class="wrap">
      <div class="brand">
        <img src="{payload['logo']}" onerror="this.style.display='none'"/>
        <div class="title">Bank of Sam — SAMBUCKS</div>
      </div>
      <div class="navbar">
        <div class="navbtn">Home</div>
        <div class="navbtn">Markets</div>
        <div class="navbtn">Your Accounts</div>
      </div>
    </div>
  </div>

  <div class="wrap">
    <div class="banner">
      <div class="breaking">
        <div class="hdr">Breaking NEWS</div>
        <div class="marquee" id="breaking">Loading headlines</div>
      </div>
      <div class="panel">
        <div class="hdr">Top Story</div>
        <div id="lead" style="padding:10px; font-size:13px;"></div>
      </div>
    </div>

    <div class="ticker">
      <div class="ticker-inner" id="ticker-strip"></div>
    </div>

    <div class="grid">
      <div class="panel">
        <div class="hdr">Watchlist</div>
        <div style="padding:8px;">
          <table class="table" id="watch">
            <thead><tr><th>Ticker</th><th>Price</th><th>Chg</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="hdr">Chart</div>
        <div style="padding:8px;">
          <canvas id="chart" width="680" height="280" style="width:100%; background:#07150b;"></canvas>
        </div>
        <div class="hdr">Order Flow</div>
        <div style="padding:8px; max-height:260px; overflow:auto;">
          <table class="table" id="blotter">
            <thead><tr><th>Trader</th><th>Side</th><th>Price</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="hdr">OTHER NEWS OF THE DAY</div>
        <div style="padding:10px;">
          <div style="font-weight:700;">Research Headline</div>
          <div style="font-size:12px; color:var(--muted);">SAMBUCKS outlook remains very green</div>
          <hr style="border-color: rgba(255,255,255,0.08)" />
          <div style="font-weight:700;">Weather Bug</div>
          <div style="font-size:12px;">NYC numbers finally feel like alpha!</div>
        </div>
      </div>
    </div>
  </div>

<script>
const SEED = {json.dumps(payload)};
const TICKERS = SEED.tickers.slice();
let prices = SEED.prices.slice();
const vols = SEED.vols.slice();

function fmt(n) {{ return Number(n).toFixed(2); }}

function buildWatch() {{
  const tb = document.querySelector("#watch tbody");
  tb.innerHTML = "";
  for (let i=0;i<TICKERS.length;i++) {{
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${{TICKERS[i]}}</td><td>${{fmt(prices[i])}}</td><td class="green">+1.2%</td>`;
    tb.appendChild(tr);
  }}
}}

function buildTickerStrip() {{
  const el = document.getElementById("ticker-strip");
  el.innerHTML = "";
  TICKERS.forEach((t, i) => {{
    const node = document.createElement("span");
    node.className = "badge";
    node.innerHTML = `<b>${{t}}</b>: ${{fmt(prices[i])}}`;
    el.appendChild(node);
  }});
}}

// --- NEW ALERT BUBBLE LOGIC ---
const alertOptions = [
  "<b>MARKET MOVE:</b> SAM01 surged +15% on high volume!",
  "<b>WHALE ALERT:</b> Large buy order detected on SAM04.",
  "<b>RUMOR:</b> Bank of Sam to announce 2:1 stock split?",
  "<b>VIBE CHECK:</b> Market sentiment is officially 'MOONISH'.",
  "<b>TECH ALERT:</b> Robo-hedger just executed 5,000 trades."
];

function showRandomAlert() {{
  const bubble = document.getElementById("alertBubble");
  const text = document.getElementById("alertText");
  const randomMsg = alertOptions[Math.floor(Math.random() * alertOptions.length)];
  text.innerHTML = randomMsg;
  bubble.style.display = "block";
}}

function closeAlert() {{
  document.getElementById("alertBubble").style.display = "none";
}}

// Initialize
buildWatch();
buildTickerStrip();
setTimeout(showRandomAlert, 4000); // Popup after 4 seconds

</script>
</body>
</html>
"""

components.html(HTML, height=1200, scrolling=True)

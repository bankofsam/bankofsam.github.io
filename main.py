import json
import base64
from pathlib import Path
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# 1. Setup the page
st.set_page_config(page_title="BANK OF SAM — SAMBUCKS", layout="wide", initial_sidebar_state="collapsed")

# 2. Hide standard Streamlit elements to make it look like a real website
st.markdown("""
<style>
    :root { --bankofsam-bg: #06140b; }
    html, body, .stApp { background: var(--bankofsam-bg) !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    header { display: none !important; }
    footer { display: none !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    iframe[title="st.iframe"] { display: block; margin: 0; background: transparent; }
</style>
""", unsafe_allow_html=True)

# 3. Image loading logic
json_file = None
logo_file = None

def load_sam_data_url():
    # If you have a file uploader later, this handles it
    if logo_file is not None:
        b = logo_file.read()
        return "data:image/png;base64," + base64.b64encode(b).decode("ascii")
    
    # Fallback: check for local file
    p = Path(__file__).parent / "sam.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    
    # Final fallback: a tiny transparent pixel so it doesn't show a broken image icon
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAmMB4hQq9XcAAAAASUVORK5CYII="

sam_data_url = load_sam_data_url()

# 4. Load News Feed
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
        "names": ["Sam A", "Jamie Q", "Taylor Q", "Jordan K", "Avery P", "Riley M"]
    }
    # If you add file loading later, put logic here. For now, return default.
    return default

feed = load_feed()

# 5. Generate random market data
rng = np.random.default_rng(7)
tickers = [f"SAM{i:02d}" for i in range(1, 11)]
start_prices = np.round(rng.uniform(4, 250, len(tickers)), 2).tolist()
vols = np.round(rng.uniform(0.2, 2.0, len(tickers)), 2).tolist()

# 6. Prepare data for the HTML/JS
payload = {
    "theme": "green",
    "logo": sam_data_url,
    "tickers": tickers,
    "prices": start_prices,
    "vols": vols,
    "stories": feed["stories"],
    "names": feed["names"]
}

# 7. THE MAIN HTML BLOCK
# Note: In f-strings, we use {{ for CSS/JS braces and { for Python variables.
HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>BANK OF SAM — SAMBUCKS</title>
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
html, body {{ margin:0; padding:0; background:#06140b; color:var(--text); font-family: Verdana, Arial, Helvetica, sans-serif; overflow: hidden; }}
.wrap {{ width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 10px; }}

/* HEADER STYLES */
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
  padding:5px 10px;
  border:1px solid rgba(255,255,255,0.25);
  background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(0,0,0,0.25));
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.25), 0 2px 0 rgba(0,0,0,0.5);
  text-transform: uppercase; letter-spacing:.6px; cursor:pointer;
}}

/* CONTENT STYLES */
.banner {{ display:grid; grid-template-columns: 1fr 280px; gap:14px; padding:10px 0 6px; }}
.breaking {{
  background: linear-gradient(180deg, #0f3a21, #0b2a19);
  border:2px solid #000; box-shadow:0 4px 16px rgba(0,0,0,0.6); position:relative; overflow:hidden;
}}
.breaking .hdr {{ background:#000; color:#fff; font-weight:700; padding:4px 8px; font-size:12px; letter-spacing:.8px; }}
.breaking .marquee {{ padding:6px 10px; white-space:nowrap; overflow:hidden; font-weight:600; }}

.ticker {{
  background:#000; border-top:2px solid #1a1a1a; border-bottom:2px solid #1a1a1a;
  overflow:hidden; white-space:nowrap; font-size:13px;
}}
.ticker-inner {{ display:inline-block; padding-left:100%; animation: ticker 25s linear infinite; }}
@keyframes ticker {{ 0% {{transform:translateX(0%);}} 100% {{transform:translateX(-100%);}} }}

.badge {{
  display:inline-block; padding:3px 8px; margin:0 16px 0 0;
  background: linear-gradient(180deg, #1b1b1b, #2b2b2b);
  border:1px solid #444; color:#fff; box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);
}}

.grid {{ display:grid; grid-template-columns: 260px 1fr 320px; gap:14px; margin-top:12px; }}
.panel {{
  background: linear-gradient(180deg, var(--panel), var(--panel2));
  border:1px solid var(--border); box-shadow:0 6px 24px rgba(0,0,0,0.4);
}}
.panel .hdr {{
  padding:6px 10px; background: linear-gradient(180deg, rgba(255,255,255,0.15), rgba(0,0,0,0.35));
  border-bottom:1px solid rgba(0,0,0,0.6); font-weight:700; text-shadow:0 1px 0 rgba(0,0,0,0.8);
}}

.table {{ width:100%; border-collapse:collapse; font-size:12px; }}
.table th, .table td {{ border-bottom:1px solid rgba(255,255,255,0.08); padding:6px 8px; }}
.green {{ color: var(--up); }}
.red {{ color: var(--down); }}

/* CUSTOM POPUP CSS */
.custom-overlay {{
    position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0, 0, 0, 0.85); z-index: 999998; display: none;
}}
.custom-popup {{
    position: fixed !important; top: 50% !important; left: 50% !important;
    transform: translate(-50%, -50%); width: 400px;
    background: linear-gradient(135deg, #0b2f1a, #06140b);
    border: 3px solid #b4ff6b; color: #eaf6ec;
    padding: 30px; border-radius: 15px; text-align: center;
    z-index: 999999; display: none; box-shadow: 0 0 40px rgba(180, 255, 107, 0.4);
}}
.popup-btn {{
    margin-top: 20px; padding: 10px 25px; background: #b4ff6b; color: #06140b;
    font-weight: bold; border: none; border-radius: 5px; cursor: pointer; text-transform: uppercase;
}}

/* CHATBOT CSS */
#samChatbot {{
    position: fixed; bottom: 20px; right: 20px; width: 300px; max-width: 90%;
    font-family: Verdana, sans-serif; z-index: 10000;
}}
#samChatHeader {{
    background: linear-gradient(135deg, #0b2f1a, #06140b); border: 3px solid #b4ff6b;
    color: #eaf6ec; padding: 10px; border-radius: 12px 12px 0 0; font-weight: bold;
    cursor: pointer; text-align: center;
}}
#samChatContent {{
    display: none; background: linear-gradient(135deg, #06140b, #0b2f1a);
    border: 3px solid #b4ff6b; border-top: none; border-radius: 0 0 12px 12px;
    max-height: 250px; overflow-y: auto; padding: 10px; color: #eaf6ec; font-size: 13px;
}}
#samChatInput {{
    width: 100%; padding: 6px 8px; margin-top: 6px; border-radius: 6px;
    border: 1px solid #b4ff6b; background: #06140b; color: #eaf6ec;
}}
</style>
</head>
<body>

  <div id="popupOverlay" class="custom-overlay"></div>
  <div id="popupBox" class="custom-popup">
    <div id="popupMessage" style="font-size: 16px; line-height: 1.5;"></div>
    <button class="popup-btn" onclick="closeSamAlert()">Acknowledge</button>
  </div>

  <div class="topbar">
    <div class="wrap">
      <div class="brand">
        <img src="{payload['logo']}" style="background:#fff; border-radius:50%;" />
        <div class="title">BANK OF SAM — SAMBUCKS</div>
      </div>
      <div class="navbar">
        <div class="navbtn sam">Home</div>
        <div class="navbtn">Markets</div>
        <div class="navbtn">Tech Ticker</div>
        <div class="navbtn">Your Accounts</div>
      </div>
    </div>
  </div>

  <div class="wrap">
    <div class="banner">
      <div class="breaking">
        <div class="hdr">Breaking News</div>
        <div class="marquee" id="breaking">Loading headlines...</div>
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
        <div class="hdr" style="margin-top:10px;">News Feed</div>
        <div id="news" style="padding:8px; font-size:12px; height:200px; overflow:auto;"></div>
      </div>

      <div class="panel">
        <div class="hdr">SAMBUCKS / USD</div>
        <div style="padding:8px;">
          <canvas id="chart" width="600" height="300" style="width:100%; background:#07150b; border:1px solid rgba(255,255,255,0.08)"></canvas>
        </div>
        <div class="hdr">Order Flow</div>
        <div style="padding:8px; max-height:200px; overflow:auto;">
          <table class="table" id="blotter">
            <thead><tr><th>Time</th><th>Trader</th><th>Side</th><th>Sym</th><th>Qty</th></tr></thead>
            <tbody></tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="hdr">Daily Brief</div>
        <div style="padding:10px; font-size:12px; color:var(--muted);">
           <p><b>Research:</b> Outlook remains very green.</p>
           <hr style="border-color:rgba(255,255,255,0.1)">
           <p><b>Weather:</b> NYC numbers finally feel like Alpha.</p>
           <hr style="border-color:rgba(255,255,255,0.1)">
           <p><b>Sponsored:</b> Open an account, get a free mousepad.</p>
        </div>
      </div>
    </div>
  </div>

  <div id="samChatbot">
    <div id="samChatHeader">💬 SAM AI</div>
    <div id="samChatContent">
      <div id="samChatMessages">
        <div class="message" style="background:rgba(180,255,107,0.1); padding:6px; border-radius:4px;">Hello! I am Sam AI. 🚀</div>
      </div>
      <input type="text" id="samChatInput" placeholder="Type a message..." />
    </div>
  </div>

<script>
// --- DATA FROM PYTHON ---
const SEED = {json.dumps(payload)};

// --- HELPERS ---
function fmt(n) {{ return Number(n).toFixed(2); }}
function nowTime() {{ return new Date().toTimeString().slice(0,8); }}

// --- STATE ---
const TICKERS = SEED.tickers;
let prices = SEED.prices;
let series = Array.from({{length: 100}}, (_,i)=> prices[0] + Math.sin(i/5)*5);

// --- LOGIC ---
function buildWatch() {{
    const tb = document.querySelector("#watch tbody");
    tb.innerHTML = "";
    TICKERS.forEach((t, i) => {{
        const p = prices[i];
        const ch = (Math.random()*4 - 2).toFixed(2);
        const color = ch >= 0 ? "green" : "red";
        tb.innerHTML += `<tr><td>${{t}}</td><td>${{p.toFixed(2)}}</td><td class="${{color}}">${{ch}}%</td></tr>`;
    }});
}}

function buildTickerStrip() {{
    const el = document.getElementById("ticker-strip");
    let html = "";
    TICKERS.forEach((t, i) => {{
        const p = prices[i].toFixed(2);
        html += `<span class="badge"><b>${{t}}</b> ${{p}}</span>`;
    }});
    el.innerHTML = html;
}}

function drawChart() {{
    const ctx = document.getElementById("chart").getContext("2d");
    const W = ctx.canvas.width, H = ctx.canvas.height;
    ctx.clearRect(0,0,W,H);
    
    // Draw Grid
    ctx.strokeStyle = "rgba(255,255,255,0.1)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    for(let i=0; i<W; i+=50) {{ ctx.moveTo(i,0); ctx.lineTo(i,H); }}
    ctx.stroke();

    // Draw Line
    const min = Math.min(...series), max = Math.max(...series);
    const scale = (H-20) / (max-min || 1);
    
    ctx.strokeStyle = "#19e57a";
    ctx.lineWidth = 2;
    ctx.beginPath();
    series.forEach((v, i) => {{
        const x = i * (W / (series.length-1));
        const y = H - 10 - (v - min) * scale;
        if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }});
    ctx.stroke();
}}

function step() {{
    // Random walk
    const change = (Math.random() - 0.5) * 2;
    const next = series[series.length-1] + change;
    series.push(next);
    if(series.length > 100) series.shift();
    
    // Update random prices
    prices = prices.map(p => Math.max(0.1, p * (1 + (Math.random()-0.5)*0.01)));
    
    drawChart();
    requestAnimationFrame(step);
}}

// Blotter Logic
const NAMES = SEED.names;
function addOrder() {{
    const tb = document.querySelector("#blotter tbody");
    const side = Math.random() > 0.5 ? "BUY" : "SELL";
    const color = side === "BUY" ? "green" : "red";
    const sym = TICKERS[Math.floor(Math.random()*TICKERS.length)];
    const name = NAMES[Math.floor(Math.random()*NAMES.length)];
    const row = `<tr><td>${{nowTime()}}</td><td>${{name}}</td><td class="${{color}}">${{side}}</td><td>${{sym}}</td><td>${{Math.floor(Math.random()*1000)}}</td></tr>`;
    tb.insertAdjacentHTML('afterbegin', row);
    if(tb.children.length > 20) tb.removeChild(tb.lastChild);
}}

// POPUP LOGIC
const popMsgs = [
   "<b>⚠️ MARKET ADVISORY</b><br><br>SAM01 breached resistance. Ultra-moonish sentiment detected!",
   "<b>🚨 WHALE ACTIVITY</b><br><br>Massive buy order detected from Tier-1 Client.",
   "<b>💎 VIBE CHECK</b><br><br>Algorithm detects Diamond Hands in your sector."
];
function showSamAlert() {{
    const msg = popMsgs[Math.floor(Math.random() * popMsgs.length)];
    document.getElementById("popupMessage").innerHTML = msg;
    document.getElementById("popupOverlay").style.display = "block";
    document.getElementById("popupBox").style.display = "block";
}}
function closeSamAlert() {{
    document.getElementById("popupOverlay").style.display = "none";
    document.getElementById("popupBox").style.display = "none";
}}

// CHATBOT LOGIC
document.getElementById("samChatHeader").onclick = function() {{
    const c = document.getElementById("samChatContent");
    c.style.display = c.style.display === "none" ? "block" : "none";
}};
document.getElementById("samChatInput").addEventListener("keypress", function(e) {{
    if(e.key === "Enter" && this.value.trim()) {{
        const d = document.getElementById("samChatMessages");
        d.innerHTML += `<div style="margin:4px 0;"><b>You:</b> ${{this.value}}</div>`;
        this.value = "";
        setTimeout(() => {{
            const replies = ["Bullish!", "Priced in.", "Only up from here.", "Have you tried restarting the economy?"];
            const r = replies[Math.floor(Math.random()*replies.length)];
            d.innerHTML += `<div style="margin:4px 0; background:rgba(180,255,107,0.1); padding:4px;"><b>Sam AI:</b> ${{r}}</div>`;
            d.scrollTop = d.scrollHeight;
        }}, 600);
    }}
}});

// INIT
buildWatch();
buildTickerStrip();
document.getElementById("lead").innerHTML = `<b>${{SEED.stories[0].title}}</b><br>${{SEED.stories[0].body}}`;

// TIMERS
setInterval(buildWatch, 3000);
setInterval(addOrder, 1500);
requestAnimationFrame(step);

// Trigger popup after 2 seconds
setTimeout(showSamAlert, 2000);

</script>
</body>
</html>
"""

# 8. Render the HTML
components.html(HTML, height=1000, scrolling=True)

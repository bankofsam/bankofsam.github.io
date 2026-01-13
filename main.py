import json
import base64
from pathlib import Path
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="BANK OF SAM", layout="wide", initial_sidebar_state="collapsed")

# --- 2. SETUP DATA & IMAGES ---
# (We handle the image loading safely here)
json_file = None
logo_file = None

def load_sam_data_url():
    # If a file is uploaded (future proofing), read it
    if logo_file is not None:
        b = logo_file.read()
        return "data:image/png;base64," + base64.b64encode(b).decode("ascii")
    # Check local folder
    p = Path(__file__).parent / "sam.png"
    if p.exists():
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    # Fallback transparent pixel
    return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAmMB4hQq9XcAAAAASUVORK5CYII="

sam_data_url = load_sam_data_url()

# Create dummy news feed
feed = {
    "stories": [
        {"title":"Alex Coin completely valueless", "body":"DO NOT INVEST IN ALEX COIN"},
        {"title":"Robo hedger toggles on", "body":"Latency improved to probably fine"},
        {"title":"Balance sheet very green", "body":"Analysts upgrade outlook to moonish"},
        {"title":"Checking flood of deposits", "body":"Customers embrace new high-yield fling"},
    ],
    "names": ["Sam A", "Jamie Q", "Taylor Q", "Jordan K", "Avery P"]
}

# Generate random stock data
rng = np.random.default_rng(7)
tickers = [f"SAM{i:02d}" for i in range(1, 11)]
start_prices = np.round(rng.uniform(4, 250, len(tickers)), 2).tolist()

payload = {
    "theme": "green",
    "logo": sam_data_url,
    "tickers": tickers,
    "prices": start_prices,
    "stories": feed["stories"],
    "names": feed["names"]
}

# Convert payload to JSON string for the HTML to use
payload_json = json.dumps(payload)

# --- 3. FORCE DARK MODE ON STREAMLIT ITSELF ---
st.markdown("""
<style>
    /* Forces the main Streamlit background to be dark so you don't see white flashes */
    .stApp { background-color: #06140b; }
    header, footer { display: none !important; }
</style>
""", unsafe_allow_html=True)


# --- 4. THE HTML TEMPLATE ---
# We use a standard string here. No f-string.
# We will use .replace("__PAYLOAD_PLACEHOLDER__", ...) later.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>BANK OF SAM</title>
<style>
/* CSS RESET & VARIABLES */
:root {
  --bg: #06140b;
  --text: #eaf6ec;
  --green: #19e57a;
  --red: #ff5b4d;
  --accent: #b4ff6b;
  --panel: rgba(255,255,255,0.05);
}
* { box-sizing: border-box; }
body { 
    margin: 0; padding: 0; 
    background-color: var(--bg); 
    color: var(--text); 
    font-family: Verdana, sans-serif; 
    overflow-x: hidden;
}

/* UTILS */
.green { color: var(--green); }
.red { color: var(--red); }
.wrap { max-width: 1200px; margin: 0 auto; padding: 0 10px; }

/* HEADER */
.topbar {
    background: linear-gradient(180deg, #16a34a, #0e5a2f);
    border-bottom: 3px solid #000;
    padding: 10px 0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    position: sticky; top: 0; z-index: 100;
}
.brand { font-size: 20px; font-weight: bold; display: flex; align-items: center; gap: 10px; }
.brand img { height: 30px; background: #fff; border-radius: 50%; }

/* LAYOUT */
.grid { display: grid; grid-template-columns: 250px 1fr 250px; gap: 15px; margin-top: 20px; }
.panel { 
    background: var(--panel); 
    border: 1px solid rgba(255,255,255,0.1); 
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.hdr { 
    background: rgba(0,0,0,0.3); 
    padding: 8px 10px; 
    font-weight: bold; 
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.content { padding: 10px; }

/* TABLES */
table { width: 100%; border-collapse: collapse; font-size: 13px; }
td, th { padding: 6px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: left; }

/* TICKER STRIP */
.ticker-wrap { background: #000; overflow: hidden; white-space: nowrap; border-top: 1px solid #333; border-bottom: 1px solid #333; }
.ticker { display: inline-block; animation: tick 20s linear infinite; padding-left: 100%; }
.tick-item { display: inline-block; margin-right: 20px; padding: 5px 0; }
@keyframes tick { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }

/* POPUP */
.overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; display: none; }
.popup { 
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 300px; background: #0b2f1a; border: 2px solid var(--accent); padding: 20px;
    text-align: center; color: #fff; box-shadow: 0 0 30px rgba(180,255,107,0.3);
}
button { background: var(--accent); border: none; padding: 8px 16px; font-weight: bold; cursor: pointer; margin-top: 15px; }

/* CHAT */
.chat-btn { position: fixed; bottom: 20px; right: 20px; background: #0b2f1a; border: 2px solid var(--accent); padding: 10px 20px; cursor: pointer; font-weight: bold; z-index: 5000; }
.chat-box { 
    position: fixed; bottom: 70px; right: 20px; width: 300px; height: 300px; 
    background: #000; border: 2px solid var(--accent); display: none; 
    flex-direction: column; z-index: 5000;
}
.chat-msgs { flex: 1; padding: 10px; overflow-y: auto; font-size: 12px; }
.chat-input { border: none; border-top: 1px solid #333; padding: 10px; background: #111; color: #fff; }

</style>
</head>
<body>

<div id="overlay" class="overlay">
    <div class="popup">
        <h3 style="margin-top:0">⚠️ MARKET ALERT</h3>
        <p id="alert-msg">Loading...</p>
        <button onclick="closeAlert()">ACKNOWLEDGE</button>
    </div>
</div>

<div class="topbar">
    <div class="wrap">
        <div class="brand">
            <img src="__LOGO_PLACEHOLDER__" />
            BANK OF SAM
        </div>
    </div>
</div>

<div class="ticker-wrap">
    <div class="ticker" id="ticker">Loading...</div>
</div>

<div class="wrap">
    <div class="grid">
        <div class="panel">
            <div class="hdr">WATCHLIST</div>
            <div class="content">
                <table id="watch-table"><tbody></tbody></table>
            </div>
            <div class="hdr">NEWS</div>
            <div class="content" id="news-feed" style="font-size:12px; height: 200px; overflow-y: auto;">
            </div>
        </div>

        <div class="panel">
            <div class="hdr">SAMBUCKS / USD</div>
            <div class="content">
                <canvas id="chart" width="500" height="300" style="width:100%; background:#000;"></canvas>
            </div>
            <div class="hdr">ORDER FLOW</div>
            <div class="content" style="height: 150px; overflow-y: hidden;">
                <table id="orders"><tbody></tbody></table>
            </div>
        </div>

        <div class="panel">
            <div class="hdr">DAILY BRIEF</div>
            <div class="content" style="font-size:13px; color: #aaa;">
                <p><b>Strategy:</b> Buy high, sell low.</p>
                <hr style="border-color:#333">
                <p><b>Weather:</b> Cloudy with a chance of liquidity.</p>
                <hr style="border-color:#333">
                <p><b>Sponsored:</b> "I lost it all on SAMBUCKS and you can too!"</p>
            </div>
        </div>
    </div>
</div>

<div class="chat-btn" onclick="toggleChat()">💬 SAM AI</div>
<div class="chat-box" id="chat-box">
    <div class="chat-msgs" id="chat-msgs">
        <div style="color:var(--accent)"><b>SAM AI:</b> How can I help you lose money today?</div>
    </div>
    <input type="text" class="chat-input" placeholder="Type here..." onkeypress="handleChat(event)">
</div>

<script>
// INJECT DATA HERE
const DATA = __PAYLOAD_PLACEHOLDER__;

// 1. SETUP TICKER
const tickerDiv = document.getElementById('ticker');
let tickerHtml = "";
DATA.tickers.forEach((t, i) => {
    const p = DATA.prices[i];
    tickerHtml += `<span class="tick-item"><b>${t}</b> $${p}</span>`;
});
tickerDiv.innerHTML = tickerHtml;

// 2. SETUP WATCHLIST
const watchTable = document.querySelector("#watch-table tbody");
DATA.tickers.forEach((t, i) => {
    const p = DATA.prices[i];
    const chg = (Math.random() * 10 - 5).toFixed(2);
    const color = chg > 0 ? "green" : "red";
    watchTable.innerHTML += `<tr><td>${t}</td><td>${p}</td><td class="${color}">${chg}%</td></tr>`;
});

// 3. SETUP NEWS
const newsDiv = document.getElementById("news-feed");
DATA.stories.forEach(s => {
    newsDiv.innerHTML += `<div style="margin-bottom:10px"><b>${s.title}</b><br><span style="color:#888">${s.body}</span></div>`;
});

// 4. SIMPLE CHART
const ctx = document.getElementById('chart').getContext('2d');
let prices = [100, 102, 101, 105, 104, 108, 110, 109, 115, 112, 118];
function drawChart() {
    const w = ctx.canvas.width;
    const h = ctx.canvas.height;
    ctx.clearRect(0,0,w,h);
    
    // Grid
    ctx.strokeStyle = "#222";
    ctx.beginPath();
    for(let i=0;i<w;i+=50) { ctx.moveTo(i,0); ctx.lineTo(i,h); }
    ctx.stroke();

    // Line
    ctx.strokeStyle = "#19e57a";
    ctx.lineWidth = 2;
    ctx.beginPath();
    const max = Math.max(...prices);
    const min = Math.min(...prices);
    const range = max - min + 1;
    
    prices.forEach((p, i) => {
        const x = (i / (prices.length - 1)) * w;
        const y = h - ((p - min) / range) * (h - 20) - 10;
        if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.stroke();
}
drawChart();

// Animation Loop
setInterval(() => {
    const last = prices[prices.length-1];
    const next = last + (Math.random() - 0.5) * 5;
    prices.push(next);
    if(prices.length > 50) prices.shift();
    drawChart();
    
    // Random order flow
    const names = DATA.names;
    const rndName = names[Math.floor(Math.random()*names.length)];
    const rndTicker = DATA.tickers[Math.floor(Math.random()*DATA.tickers.length)];
    const side = Math.random() > 0.5 ? "BUY" : "SELL";
    const color = side === "BUY" ? "green" : "red";
    const row = `<tr><td>${rndName}</td><td class="${color}">${side}</td><td>${rndTicker}</td></tr>`;
    const tb = document.querySelector("#orders tbody");
    tb.insertAdjacentHTML("afterbegin", row);
    if(tb.children.length > 8) tb.removeChild(tb.lastChild);
    
}, 1000);

// POPUP LOGIC
setTimeout(() => {
    document.getElementById("alert-msg").innerText = "SAMBUCKS stock is rising! (Maybe).";
    document.getElementById("overlay").style.display = "block";
}, 2000);

function closeAlert() {
    document.getElementById("overlay").style.display = "none";
}

// CHAT LOGIC
function toggleChat() {
    const box = document.getElementById("chat-box");
    box.style.display = box.style.display === "flex" ? "none" : "flex";
}

function handleChat(e) {
    if(e.key === "Enter") {
        const input = e.target;
        const msg = input.value;
        if(!msg) return;
        
        const div = document.getElementById("chat-msgs");
        div.innerHTML += `<div style="margin-top:5px; color:#fff"><b>You:</b> ${msg}</div>`;
        input.value = "";
        div.scrollTop = div.scrollHeight;
        
        setTimeout(() => {
            const replies = ["Bullish.", "Have you checked the vibes?", "I am just a script.", "Buy high!"];
            const r = replies[Math.floor(Math.random()*replies.length)];
            div.innerHTML += `<div style="margin-top:5px; color:var(--accent)"><b>SAM AI:</b> ${r}</div>`;
            div.scrollTop = div.scrollHeight;
        }, 500);
    }
}
</script>
</body>
</html>
"""

# --- 5. INJECT DATA AND RENDER ---
# This is the magic part. We replace the placeholder with the real data.
final_html = HTML_TEMPLATE.replace("__PAYLOAD_PLACEHOLDER__", payload_json)
final_html = final_html.replace("__LOGO_PLACEHOLDER__", sam_data_url)

# Render with a fixed height to ensure it doesn't collapse
components.html(final_html, height=1000, scrolling=True)

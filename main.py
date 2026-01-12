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

/* kill any first-child spacing in the main stack */
section.main > div:first-child { margin-top: 0 !important; padding-top: 0 !important; }

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
        "names": ["Sam A", "Jamie Q", "Taylor Q", "Jordan K", "Avery P", "Riley M", "Casey D", "Morgan L", "Drew T", "Cameron J", "Reese F", "Peyton S", "Rowan H", "Skyler V", "Emerson N", "Quinn C", "Logan R", "Harper W", "Sage K", "Blake Z", "Elliot Y", "Finley G", "Charlie P", "Dakota M", "Jules E", "Alex B", "Corey L", "Shawn D", "Tatum F", "Hayden J", "Micah T", "Kendall C", "Spencer H", "Arden V", "Bailey N", "Parker E", "Devon S", "Cory R", "Blair G", "Sydney P", "Cameron M", "Lane K", "Toby Q", "Ashton W", "Jordan T", "Marley V", "Quincy B", "Aiden Z", "Rowan L", "Reagan Y", "Sasha N", "Kai G", "Ari P", "Harley J", "Phoenix R", "Dylan C", "Morgan T", "Kieran E", "Avery L", "Jesse S", "Taylor B", "Reese H", "Skylar M", "Cory D", "Casey N", "Toby R", "Jamie P", "Spencer V", "Riley K", "Emery F", "Rowan J", "Aiden Q", "Blake C", "Parker T", "Harper L", "Drew M", "Elliot R", "Quinn H", "Jules N", "Sage P", "Taylor D", "Cameron W", "Morgan G", "Dakota L", "Rowan Z", "Alex T", "Avery Q", "Skyler B", "Emerson V", "Jamie N", "Casey K", "Jordan F", "Riley Y", "Taylor W", "Spencer G", "Blair D", "Finley C", "Hayden P", "Rowan M", "Elliot S", "Ari J", "Reese H"]
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
  --g1: #0b2f1a; --g2: #0e5a2f; --g3: #16a34a;
  --panel: rgba(255,255,255,0.06); --panel2: rgba(0,0,0,0.3);
  --border: rgba(255,255,255,0.12); --text: #eaf6ec;
  --muted: #b6d6bf; --up: #19e57a; --down: #ff5b4d; --accent: #b4ff6b;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#06140b; color:var(--text); font-family: Verdana, Arial, sans-serif; }}
.wrap {{ width: 1120px; margin: 0 auto; }}

.topbar {{ background: linear-gradient(180deg, var(--g3), var(--g2) 60%, var(--g1)); border-bottom: 3px solid #000; position: sticky; top: 0; z-index: 999; box-shadow: 0 4px 18px rgba(0,0,0,0.5); }}
.brand {{ display:flex; align-items:center; gap:14px; padding:10px 12px; }}
.brand img {{ height:44px; border:2px solid rgba(255,255,255,0.2); }}
.brand .title {{ font-weight:700; font-size:22px; text-shadow:0 1px 0 #000; }}

.navbar {{ background: linear-gradient(180deg, rgba(0,0,0,0.35), rgba(255,255,255,0.05)); border-top:1px solid rgba(255,255,255,0.1); display:flex; gap:18px; padding:6px 10px; font-size:13px; }}

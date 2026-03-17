
# =============================================================================
# THE MOUNTAIN PATH — WORLD OF FINANCE
# Bond Primary Market Issue Pricing Model
# Prof. V. Ravichandran | themountainpathacademy.com
# =============================================================================

import streamlit as st
import numpy as np
import pandas as pd
from datetime import date, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bond Primary Market Pricing | The Mountain Path",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DESIGN CONSTANTS ──────────────────────────────────────────────────────────
DARK_BLUE   = "#003366"
MID_BLUE    = "#004d80"
CARD_BG     = "#112240"
GOLD        = "#FFD700"
TXT         = "#e6f1ff"
MUTED       = "#8892b0"
GREEN       = "#28a745"
RED         = "#dc3545"
LT_BLUE     = "#ADD8E6"
BG_GRAD     = "linear-gradient(135deg,#1a2332,#243447,#2a3f5f)"

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.html(f"""
<style>
  /* Background */
  .stApp {{
    background: {BG_GRAD};
    color: {TXT};
  }}
  /* Global text — ensure all p/span/div have contrast */
  .stApp p, .stApp span, .stApp div {{
    color: {TXT};
  }}
  /* Main content area text */
  [data-testid="stMainBlockContainer"] p,
  [data-testid="stMainBlockContainer"] span:not(.st-emotion-cache-hidden) {{
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
  }}
  /* Headings inside main */
  [data-testid="stMainBlockContainer"] h1,
  [data-testid="stMainBlockContainer"] h2,
  [data-testid="stMainBlockContainer"] h3 {{
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
  }}
  /* Sidebar */
  [data-testid="stSidebar"] {{
    background: linear-gradient(180deg,#0a1628,#112240,#0d1f3c) !important;
    border-right: 1px solid {GOLD}33;
  }}
  [data-testid="stSidebar"] * {{ color: {TXT} !important; }}
  /* Sidebar input text — force white */
  [data-testid="stSidebar"] input {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: #0a1628 !important;
  }}
  [data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: #0a1628 !important;
    color: #ffffff !important;
  }}
  [data-testid="stSidebar"] [data-baseweb="select"] span {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  [data-testid="stSidebar"] .stDateInput input {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background: #0a1628 !important;
  }}
  [data-testid="stSidebar"] [data-testid="InputInstructions"] {{
    color: {MUTED} !important;
  }}
  /* Sidebar selectbox closed state text */
  [data-testid="stSidebar"] [data-baseweb="select"] * {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #0a1628 !important;
  }}
  /* Sidebar selectbox container */
  [data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: #0a1628 !important;
    border: 1px solid {MID_BLUE} !important;
  }}
  /* Open dropdown list — MUST be white text on dark bg */
  ul[role="listbox"],
  div[role="listbox"],
  [data-baseweb="popover"] [role="listbox"] {{
    background: #071120 !important;
    border: 1px solid {GOLD}88 !important;
  }}
  li[role="option"],
  [data-baseweb="menu"] [role="option"],
  [data-baseweb="list-item"] {{
    background: #071120 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  li[role="option"]:hover,
  li[aria-selected="true"],
  [data-baseweb="menu"] li[aria-selected="true"] {{
    background: {DARK_BLUE} !important;
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
  }}
  /* Placeholder text inside closed selectbox */
  [data-baseweb="select"] input,
  [data-baseweb="select"] input::placeholder {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
  }}
  /* Data editor / tables */
  .stDataFrame td, .stDataFrame th {{
    color: {TXT} !important;
  }}
  [data-testid="data-grid-canvas"] {{
    color: {TXT} !important;
  }}
  /* General all text inputs anywhere */
  input[type="text"], input[type="number"], input[class*="st-"] {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  /* Placeholder text */
  input::placeholder {{
    color: {MUTED} !important;
    -webkit-text-fill-color: {MUTED} !important;
    opacity: 0.7;
  }}
  /* Inputs — high contrast text */
  .stTextInput input,
  .stNumberInput input,
  .stDateInput input {{
    background: #0d1f3c !important;
    color: #ffffff !important;
    border: 1px solid {MID_BLUE} !important;
    border-radius: 6px !important;
    caret-color: {GOLD} !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  /* Select boxes */
  .stSelectbox > div > div {{
    background: #0d1f3c !important;
    border: 1px solid {MID_BLUE} !important;
    border-radius: 6px !important;
    color: #ffffff !important;
  }}
  .stSelectbox > div > div > div {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  /* Dropdown options */
  [data-baseweb="select"] span,
  [data-baseweb="select"] div,
  [data-baseweb="popover"] li {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  /* Number input */
  .stNumberInput > div {{
    background: #0d1f3c !important;
    border: 1px solid {MID_BLUE} !important;
    border-radius: 6px !important;
  }}
  /* Date input */
  .stDateInput > div > div > input {{
    background: #0d1f3c !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid {MID_BLUE} !important;
    border-radius: 6px !important;
  }}
  /* Labels above inputs */
  .stTextInput label,
  .stNumberInput label,
  .stSelectbox label,
  .stDateInput label,
  .stSlider label {{
    color: {LT_BLUE} !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
  }}
  /* Slider */
  .stSlider > div > div > div {{
    background: {GOLD} !important;
  }}
  .stSlider [data-testid="stTickBarMin"],
  .stSlider [data-testid="stTickBarMax"] {{
    color: {MUTED} !important;
  }}
  /* Tabs — gold active, bright inactive */
  .stTabs [data-baseweb="tab-list"] {{
    background: #071120;
    border-radius: 10px;
    gap: 3px;
    padding: 5px;
    border: 1px solid {MID_BLUE}66;
  }}
  /* Inactive tab */
  .stTabs [data-baseweb="tab"] {{
    background: #0d1f3c !important;
    color: #cdd8f0 !important;
    -webkit-text-fill-color: #cdd8f0 !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    opacity: 1 !important;
    padding: 6px 12px !important;
    border: 1px solid {MID_BLUE}44 !important;
    transition: all 0.15s !important;
  }}
  .stTabs [data-baseweb="tab"] *,
  .stTabs [data-baseweb="tab"] p,
  .stTabs [data-baseweb="tab"] span,
  .stTabs [data-baseweb="tab"] div {{
    color: #cdd8f0 !important;
    -webkit-text-fill-color: #cdd8f0 !important;
    opacity: 1 !important;
  }}
  /* Inactive tab hover */
  .stTabs [data-baseweb="tab"]:hover {{
    background: {MID_BLUE} !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: {GOLD}55 !important;
  }}
  /* ACTIVE tab — GOLD background */
  .stTabs [aria-selected="true"],
  .stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: {GOLD} !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border: 1px solid {GOLD} !important;
    border-radius: 7px !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 8px {GOLD}55 !important;
  }}
  .stTabs [aria-selected="true"] *,
  .stTabs [aria-selected="true"] p,
  .stTabs [aria-selected="true"] span,
  .stTabs [aria-selected="true"] div {{
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
  }}
  /* Remove Streamlit's default bottom border underline on active tab */
  .stTabs [data-baseweb="tab-highlight"] {{
    display: none !important;
    background: transparent !important;
  }}
  /* Dataframe / Tables — full contrast */
  .stDataFrame {{ border: 1px solid {MID_BLUE}; border-radius: 8px; overflow: hidden; }}
  /* Table headers */
  .stDataFrame thead th,
  .stDataFrame [data-testid="glideDataEditor"] .gdg-header,
  [data-testid="stDataFrameResizable"] th,
  [data-testid="stDataFrameResizable"] [role="columnheader"] {{
    background: {DARK_BLUE} !important;
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {GOLD}66 !important;
  }}
  /* Table cells */
  .stDataFrame tbody td,
  [data-testid="stDataFrameResizable"] td,
  [data-testid="stDataFrameResizable"] [role="gridcell"] {{
    background: {CARD_BG} !important;
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
    border-bottom: 1px solid {MID_BLUE}44 !important;
    font-size: 0.83rem !important;
  }}
  /* Alternating rows */
  .stDataFrame tbody tr:nth-child(even) td,
  [data-testid="stDataFrameResizable"] tr:nth-child(even) [role="gridcell"] {{
    background: #0d1f3c !important;
  }}
  /* Glide data editor canvas text */
  .gdg-cell, .gdg-cell span, .gdg-cell div {{
    color: {TXT} !important;
    -webkit-text-fill-color: {TXT} !important;
  }}
  /* Metrics — full contrast */
  [data-testid="metric-container"] {{
    background: {CARD_BG} !important;
    border: 1px solid {MID_BLUE} !important;
    border-radius: 10px !important;
    padding: 12px !important;
  }}
  [data-testid="metric-container"] label,
  [data-testid="metric-container"] [data-testid="stMetricLabel"],
  [data-testid="metric-container"] [data-testid="stMetricLabel"] p,
  [data-testid="metric-container"] [data-testid="stMetricLabel"] div {{
    color: {LT_BLUE} !important;
    -webkit-text-fill-color: {LT_BLUE} !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;
  }}
  [data-testid="metric-container"] [data-testid="stMetricValue"],
  [data-testid="metric-container"] [data-testid="stMetricValue"] div {{
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    opacity: 1 !important;
  }}
  [data-testid="metric-container"] [data-testid="stMetricDelta"],
  [data-testid="metric-container"] [data-testid="stMetricDelta"] div,
  [data-testid="metric-container"] [data-testid="stMetricDelta"] p {{
    opacity: 1 !important;
    font-size: 0.75rem !important;
  }}
  /* Divider */
  hr {{ border-color: {GOLD}44 !important; }}

  /* ═══ DROPDOWN / SELECTBOX — full contrast ═══ */
  /* The open dropdown list panel */
  [data-baseweb="popover"],
  [data-baseweb="popover"] ul,
  [data-baseweb="menu"],
  [data-baseweb="menu"] ul {{
    background: #0a1628 !important;
    border: 1px solid {GOLD}88 !important;
    border-radius: 8px !important;
  }}
  /* Each option in the list */
  [data-baseweb="menu"] li,
  [data-baseweb="option"],
  [data-baseweb="popover"] li {{
    background: #0a1628 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 0.85rem !important;
  }}
  /* Highlighted / hovered option */
  [data-baseweb="menu"] li:hover,
  [data-baseweb="option"]:hover,
  [aria-selected="true"][data-baseweb="option"] {{
    background: {DARK_BLUE} !important;
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
  }}
  /* Currently selected item shown in the closed selectbox */
  [data-baseweb="select"] [data-testid="stSelectbox"],
  [data-baseweb="select"] div[class*="valueContainer"] span,
  [data-baseweb="select"] div[class*="singleValue"],
  [data-baseweb="select"] > div > div > div {{
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
  }}
  /* Dropdown arrow */
  [data-baseweb="select"] svg {{ fill: {GOLD} !important; }}
  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 6px; background: #0a1628; }}
  ::-webkit-scrollbar-thumb {{ background: {MID_BLUE}; border-radius: 3px; }}
  /* Buttons */
  .stButton > button {{
    background: {DARK_BLUE} !important;
    color: {GOLD} !important;
    border: 1px solid {GOLD}88 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: all 0.2s;
  }}
  .stButton > button:hover {{
    background: {MID_BLUE} !important;
    border-color: {GOLD} !important;
    transform: translateY(-1px);
  }}
</style>
""")

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def bond_price(settlement, maturity, coupon, ytm, face=100, freq=2, basis=0):
    """Calculate bond price using present value of cash flows (30/360)."""
    if basis == 0:  # 30/360
        def days_30_360(d1, d2):
            y1,m1,day1 = d1.year,d1.month,min(d1.day,30)
            y2,m2,day2 = d2.year,d2.month,d2.day
            if day2 == 31 and day1 >= 30: day2 = 30
            if day1 == 31: day1 = 30
            return 360*(y2-y1) + 30*(m2-m1) + (day2-day1)
    # Generate coupon dates
    periods = []
    d = maturity
    while d > settlement:
        periods.append(d)
        if freq == 2:
            m = d.month - 6
            y = d.year
            if m <= 0: m += 12; y -= 1
            try: d = date(y, m, d.day)
            except: d = date(y, m, 28)
        else:
            try: d = date(d.year-1, d.month, d.day)
            except: d = date(d.year-1, d.month, 28)
    periods = sorted(periods)
    if not periods: return face

    pv = 0.0
    rate_per = ytm / freq
    # Days in full period (for accrual)
    for i, cpn_date in enumerate(periods):
        if i == 0:
            prev = settlement
        else:
            prev = periods[i-1]
        if basis == 0:
            days_in = days_30_360(settlement, cpn_date)
            days_full = days_30_360(prev if i>0 else settlement, cpn_date)
        else:
            days_in = (cpn_date - settlement).days
            days_full = (cpn_date - prev).days if i>0 else (cpn_date - settlement).days
        t = days_in / (360/freq) if basis==0 else days_in / (365/freq)
        cf = (coupon / freq) * face
        if i == len(periods) - 1:
            cf += face
        pv += cf / (1 + rate_per)**t
    return pv

def macaulay_duration(settlement, maturity, coupon, ytm, face=100, freq=2):
    """Macaulay duration in years."""
    def days_30_360(d1, d2):
        y1,m1,day1 = d1.year,d1.month,min(d1.day,30)
        y2,m2,day2 = d2.year,d2.month,d2.day
        if day2==31 and day1>=30: day2=30
        if day1==31: day1=30
        return 360*(y2-y1)+30*(m2-m1)+(day2-day1)
    periods = []
    d = maturity
    while d > settlement:
        periods.append(d)
        m = d.month - 6
        y = d.year
        if m <= 0: m += 12; y -= 1
        try: d = date(y, m, d.day)
        except: d = date(y, m, 28)
    periods = sorted(periods)
    if not periods: return 0
    price = bond_price(settlement, maturity, coupon, ytm, face, freq, 0)
    pv_t = 0.0
    rate_per = ytm / freq
    for i, cpn_date in enumerate(periods):
        days_in = days_30_360(settlement, cpn_date)
        t = days_in / (360 / freq)
        t_yrs = t / freq
        cf = (coupon / freq) * face
        if i == len(periods)-1: cf += face
        pv_t += (t_yrs * cf) / (1 + rate_per)**t
    return pv_t / price

def round_to_eighth(x):
    """Round to nearest 1/8%."""
    return round(x * 8) / 8

def format_currency(x, unit=""):
    """Format numbers nicely."""
    if unit == "mm":
        return f"${x:,.2f}mm"
    elif unit == "cr":
        return f"₹{x:,.2f} Cr"
    elif unit == "pct":
        return f"{x:.4f}%"
    return f"{x:,.4f}"

# ── HERO HEADER ───────────────────────────────────────────────────────────────
st.html(f"""
<div style="
  background: linear-gradient(135deg,{DARK_BLUE},{MID_BLUE});
  border: 1px solid {GOLD}66;
  border-radius: 14px;
  padding: 20px 30px 16px;
  margin-bottom: 18px;
  user-select: none;
">
  <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
    <div>
      <div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">
        THE MOUNTAIN PATH — WORLD OF FINANCE
      </div>
      <div style="color:{TXT}; font-size:1.65rem; font-weight:800; line-height:1.2;">
        Bond Primary Market
        <span style="color:{GOLD};"> Issue Pricing Model</span>
      </div>
      <div style="color:{MUTED}; font-size:0.82rem; margin-top:4px;">
        Prof. V. Ravichandran &nbsp;|&nbsp;
        <a href="https://themountainpathacademy.com" target="_blank"
           style="color:{LT_BLUE}; text-decoration:none;">
          themountainpathacademy.com
        </a>
        &nbsp;|&nbsp; Fixed Income Securities &amp; Analysis
      </div>
    </div>
    <div style="text-align:right;">
      <div style="color:{GOLD}; font-size:2rem;">📊</div>
      <div style="color:{MUTED}; font-size:0.72rem;">New Issue Pricing &amp; Spread Analysis</div>
    </div>
  </div>
</div>
""")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.html(f"""
    <div style="text-align:center; padding:10px 0 16px; border-bottom:1px solid {GOLD}44; margin-bottom:16px; user-select:none;">
      <div style="color:{GOLD}; font-size:1.05rem; font-weight:800;">⚙️ DEAL PARAMETERS</div>
      <div style="color:{MUTED}; font-size:0.72rem; margin-top:3px;">Blue = editable inputs</div>
    </div>
    """)

    # ── SECTION 1: Deal Terms ─────────────────────────────────────────────────
    st.html(f'<div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:1.5px; margin:8px 0 6px; user-select:none;">① DEAL TERMS</div>')
    issuer_name = st.text_input("Issuer Name", value="ABC Corporation")
    currency    = st.selectbox("Currency", ["USD", "INR (₹)", "EUR", "GBP"])
    notional    = st.number_input("Face Value / Notional", value=500.0, min_value=1.0, step=50.0,
                                   help="In millions (USD) or crores (INR)")
    coupon_freq = st.selectbox("Coupon Frequency", ["Semi-Annual", "Annual", "Quarterly"])
    freq_map    = {"Semi-Annual": 2, "Annual": 1, "Quarterly": 4}
    freq        = freq_map[coupon_freq]
    trade_date  = st.date_input("Trade Date", value=date(2026, 3, 17))
    settle_date = st.date_input("Settlement Date", value=date(2026, 3, 19))
    maturity_date = st.date_input("Maturity Date", value=date(2036, 3, 19))
    tenor       = (maturity_date - settle_date).days / 365.25

    st.divider()
    # ── SECTION 2: Benchmark ─────────────────────────────────────────────────
    st.html(f'<div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:1.5px; margin:8px 0 6px; user-select:none;">② BENCHMARK RATE</div>')
    benchmark_type  = st.selectbox("Benchmark", ["US Treasury", "GoI G-Sec", "SOFR", "Swap Rate"])
    benchmark_yield = st.slider("Benchmark Yield (%)", 1.0, 12.0, 4.25, 0.05,
                                 format="%.2f%%")

    st.divider()
    # ── SECTION 3: Credit Spread ─────────────────────────────────────────────
    st.html(f'<div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:1.5px; margin:8px 0 6px; user-select:none;">③ CREDIT SPREAD BUILDUP</div>')
    base_spread = st.slider("Base Credit Spread (bps)", 0, 500, 150, 5)
    nip         = st.slider("New Issue Premium / NIP (bps)", 0, 100, 15, 1)
    liq_prem    = st.slider("Liquidity Premium (bps)", 0, 50, 5, 1)
    curve_adj   = st.slider("Curve Adjustment (bps)", -50, 50, 0, 1)
    other_adj   = st.slider("Other Adjustments (bps)", -50, 50, 0, 1)
    ipt_spread  = st.slider("IPT Spread (bps)", 50, 600, 185, 5,
                             help="Initial Price Thoughts — opening negotiating spread")
    guidance    = st.slider("Final Guidance (bps)", 50, 600, 175, 5)

    st.divider()
    # ── SECTION 4: Fees ──────────────────────────────────────────────────────
    st.html(f'<div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:1.5px; margin:8px 0 6px; user-select:none;">④ FEE STRUCTURE</div>')
    mgmt_fee   = st.number_input("Management Fee (%)", value=0.20, step=0.05, format="%.2f")
    uwrt_fee   = st.number_input("Underwriting Fee (%)", value=0.25, step=0.05, format="%.2f")
    sell_conc  = st.number_input("Selling Concession (%)", value=0.20, step=0.05, format="%.2f")

    st.divider()
    # ── SECTION 5: Bookbuilding ───────────────────────────────────────────────
    st.html(f'<div style="color:{GOLD}; font-size:0.78rem; font-weight:700; letter-spacing:1.5px; margin:8px 0 6px; user-select:none;">⑤ BOOKBUILDING</div>')
    book_multiple = st.slider("Book Size Multiple (×)", 0.5, 10.0, 3.5, 0.1)
    num_orders    = st.number_input("Number of Orders", value=185, step=5)

    st.html(f"""
    <div style="border-top:1px solid {GOLD}44; padding-top:14px; margin-top:10px; text-align:center; user-select:none;">
      <a href="https://themountainpathacademy.com" target="_blank"
         style="color:{GOLD}; font-size:0.75rem; font-weight:700; text-decoration:none;">
        🌐 themountainpathacademy.com
      </a><br/>
      <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
         style="color:{LT_BLUE}; font-size:0.72rem; text-decoration:none;">
        💼 LinkedIn
      </a>
      &nbsp;&nbsp;
      <a href="https://github.com/trichyravis" target="_blank"
         style="color:{LT_BLUE}; font-size:0.72rem; text-decoration:none;">
        🐙 GitHub
      </a>
    </div>
    """)

# ── CALCULATIONS ──────────────────────────────────────────────────────────────
total_spread   = base_spread + nip + liq_prem + curve_adj + other_adj
reoffer_spread = total_spread
ytm            = (benchmark_yield + total_spread / 100) / 100
coupon_rate    = round_to_eighth(ytm * 100) / 100

try:
    reoffer_price  = bond_price(settle_date, maturity_date, coupon_rate, ytm, 100, freq, 0)
except:
    reoffer_price  = 100.0

accrued        = 0.0
dirty_price    = reoffer_price + accrued
gross_proceeds = notional * (dirty_price / 100)
total_fee_rate = (mgmt_fee + uwrt_fee + sell_conc) / 100
total_fees     = notional * total_fee_rate
net_proceeds   = gross_proceeds - total_fees
all_in_cost    = coupon_rate + total_fee_rate / tenor
tightening     = ipt_spread - reoffer_spread

# Duration / DV01 / Convexity
try:
    mac_dur = macaulay_duration(settle_date, maturity_date, coupon_rate, ytm, 100, freq)
    mod_dur = mac_dur / (1 + ytm / freq)
    dv01    = mod_dur * (reoffer_price / 100) * 0.0001 * 1_000_000 / 100
    p_up    = bond_price(settle_date, maturity_date, coupon_rate, ytm + 0.01, 100, freq, 0)
    p_dn    = bond_price(settle_date, maturity_date, coupon_rate, ytm - 0.01, 100, freq, 0)
    convexity = (p_up + p_dn - 2 * reoffer_price) / (reoffer_price * 0.01**2)
except:
    mac_dur = mod_dur = dv01 = convexity = 0.0

# Currency symbol
curr_sym = "₹" if "INR" in currency else "$" if currency=="USD" else "€" if currency=="EUR" else "£"

# ── TABS ──────────────────────────────────────────────────────────────────────
# ── ROW 1: Core pricing tabs ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 Pricing Summary",
    "📈 Spread Buildup",
    "💰 Fees & Proceeds",
    "🔍 Comps Analysis",
    "📊 Sensitivity",
])

st.html(f'''<div style="height:6px;"></div>''')

# ── ROW 2: Analysis & Education tabs ─────────────────────────────────────────
tab6, tab7 = st.tabs([
    "📐 Risk Metrics",
    "🎓 Learn",
])

# =============================================================================
# TAB 1 — PRICING SUMMARY
# =============================================================================
with tab1:
    # Key metrics row
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("YTM", f"{ytm*100:.3f}%")
    c2.metric("Coupon Rate", f"{coupon_rate*100:.3f}%")
    c3.metric("Re-Offer Price", f"{curr_sym}{reoffer_price:.3f}")
    c4.metric("Gross Proceeds", f"{curr_sym}{gross_proceeds:,.1f}mm")
    c5.metric("Spread (bps)", f"{reoffer_spread}")
    c6.metric("Tightening", f"{tightening} bps", delta=f"-{tightening} from IPT")

    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">📋 Deal Terms</div>')
        deal_data = {
            "Parameter": ["Issuer", "Currency", "Notional", "Coupon Type", "Frequency",
                          "Trade Date", "Settlement Date", "Maturity Date", "Tenor"],
            "Value": [issuer_name, currency, f"{curr_sym}{notional:,.0f}mm", "Fixed", coupon_freq,
                     str(trade_date), str(settle_date), str(maturity_date), f"{tenor:.2f} yrs"]
        }
        df_deal = pd.DataFrame(deal_data)
        rows_html = "".join([
            f'''<tr style="background:{"#0d1f3c" if i%2==0 else CARD_BG}; border-bottom:1px solid {MID_BLUE}33;">
              <td style="padding:8px 14px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; font-size:0.82rem; font-weight:600;">{row["Parameter"]}</td>
              <td style="padding:8px 14px; color:#ffffff; -webkit-text-fill-color:#ffffff; font-size:0.82rem;">{row["Value"]}</td>
            </tr>'''
            for i, row in df_deal.iterrows()
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Parameter</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Value</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """)

    with col_right:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">🎯 Pricing Outputs</div>')
        price_data = {
            "Output": ["Benchmark Yield", "Total Spread", "YTM", "Coupon Rate",
                      "Re-Offer Price", "Accrued Interest", "Dirty Price",
                      "Gross Proceeds", "Net Proceeds", "All-In Cost"],
            "Value": [f"{benchmark_yield:.3f}%", f"{total_spread} bps",
                     f"{ytm*100:.4f}%", f"{coupon_rate*100:.3f}%",
                     f"{curr_sym}{reoffer_price:.3f}", f"{curr_sym}{accrued:.3f}",
                     f"{curr_sym}{dirty_price:.3f}",
                     f"{curr_sym}{gross_proceeds:,.3f}mm",
                     f"{curr_sym}{net_proceeds:,.3f}mm",
                     f"{all_in_cost*100:.4f}%"]
        }
        df_price = pd.DataFrame(price_data)
        rows_html2 = "".join([
            f'''<tr style="background:{"#0d1f3c" if i%2==0 else CARD_BG}; border-bottom:1px solid {MID_BLUE}33;">
              <td style="padding:8px 14px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; font-size:0.82rem; font-weight:600;">{row["Output"]}</td>
              <td style="padding:8px 14px; color:{GOLD if "YTM" in row["Output"] or "Coupon" in row["Output"] or "Price" in row["Output"] else "#ffffff"}; -webkit-text-fill-color:{GOLD if "YTM" in row["Output"] or "Coupon" in row["Output"] or "Price" in row["Output"] else "#ffffff"}; font-size:0.82rem; font-weight:{"700" if "YTM" in row["Output"] else "400"};">{row["Value"]}</td>
            </tr>'''
            for i, row in df_price.iterrows()
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Output</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Value</th>
            </tr></thead>
            <tbody>{rows_html2}</tbody>
          </table>
        </div>
        """)

    # Bookbuilding summary
    st.divider()
    st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">📚 Bookbuilding Summary</div>')
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.metric("Deal Size", f"{curr_sym}{notional:,.0f}mm")
    b2.metric("Total Orders", f"{curr_sym}{notional*book_multiple:,.1f}mm")
    b3.metric("Oversubscription", f"{book_multiple:.1f}×")
    b4.metric("# of Orders", f"{int(num_orders)}")
    b5.metric("Avg Order Size", f"{curr_sym}{(notional*book_multiple)/num_orders:.1f}mm")

    # Bookbuilding journey
    st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin:14px 0 8px; user-select:none;">📉 Bookbuilding Journey: IPT → Guidance → Reoffer</div>')
    bk_data = {
        "Stage": ["IPT (Initial Price Thoughts)", "Final Guidance", "Reoffer (Final Pricing)"],
        "Spread (bps)": [ipt_spread, guidance, reoffer_spread],
        "YTM (%)": [f"{(benchmark_yield + ipt_spread/100):.3f}%",
                    f"{(benchmark_yield + guidance/100):.3f}%",
                    f"{ytm*100:.3f}%"],
        "Change from IPT": ["—", f"−{ipt_spread-guidance} bps", f"−{ipt_spread-reoffer_spread} bps"],
        "Signal": ["Opening wide to attract demand",
                   "Tightening on strong orders",
                   "Final pricing — deal complete"]
    }
    bk_rows = ""
    bk_colors = [MID_BLUE+"33", "#0d1f3c", DARK_BLUE+"55"]
    for i, stage in enumerate(bk_data["Stage"]):
        row_bg = bk_colors[i]
        is_final = i == 2
        bk_rows += f"""
        <tr style="background:{row_bg}; border-bottom:1px solid {MID_BLUE}44;">
          <td style="padding:10px 14px; color:{'#ffffff' if is_final else TXT}; font-weight:{'700' if is_final else '400'}; -webkit-text-fill-color:{'#ffffff' if is_final else TXT};">{stage}</td>
          <td style="padding:10px 14px; color:{GOLD}; font-weight:700; -webkit-text-fill-color:{GOLD}; text-align:right;">{bk_data["Spread (bps)"][i]}</td>
          <td style="padding:10px 14px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; text-align:right;">{bk_data["YTM (%)"][i]}</td>
          <td style="padding:10px 14px; color:{GREEN if i>0 else MUTED}; -webkit-text-fill-color:{GREEN if i>0 else MUTED}; font-weight:{'700' if i>0 else '400'};">{bk_data["Change from IPT"][i]}</td>
          <td style="padding:10px 14px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.82rem;">{bk_data["Signal"][i]}</td>
        </tr>"""
    st.html(f"""
    <div style="overflow-x:auto; border-radius:10px; border:1px solid {MID_BLUE}; margin-top:4px; user-select:none;">
      <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
        <thead>
          <tr style="background:{DARK_BLUE}; border-bottom:2px solid {GOLD}55;">
            <th style="padding:10px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; font-weight:700; text-align:left;">Stage</th>
            <th style="padding:10px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; font-weight:700; text-align:right;">Spread (bps)</th>
            <th style="padding:10px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; font-weight:700; text-align:right;">YTM (%)</th>
            <th style="padding:10px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; font-weight:700;">Change from IPT</th>
            <th style="padding:10px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; font-weight:700;">Signal</th>
          </tr>
        </thead>
        <tbody>{bk_rows}</tbody>
      </table>
    </div>
    """)

    # Issuer savings
    annual_saving = (ipt_spread - reoffer_spread) / 10000 * notional
    total_saving  = annual_saving * tenor
    st.html(f"""
    <div style="background:{CARD_BG}; border:1px solid {GOLD}66; border-radius:10px; padding:14px 20px; margin-top:12px; user-select:none;">
      <span style="color:{GOLD}; font-weight:700;">💡 Tightening Benefit to Issuer:</span>
      <span style="color:{TXT};"> {tightening} bps tightening from IPT saves
        <span style="color:{GREEN}; font-weight:700;">{curr_sym}{annual_saving:.2f}mm/year</span>
        = <span style="color:{GREEN}; font-weight:700;">{curr_sym}{total_saving:.1f}mm total</span>
        over {tenor:.1f} years
      </span>
    </div>
    """)

# =============================================================================
# TAB 2 — SPREAD BUILDUP
# =============================================================================
with tab2:
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">🔧 Credit Spread Buildup</div>')
        spread_data = {
            "Component": ["Base Credit Spread", "New Issue Premium (NIP)",
                          "Liquidity Premium", "Curve Adjustment", "Other Adjustments",
                          "Total Credit Spread"],
            "bps": [base_spread, nip, liq_prem, curve_adj, other_adj, total_spread],
            "(%)": [f"{x/100:.3f}%" for x in [base_spread, nip, liq_prem, curve_adj, other_adj, total_spread]],
            "Notes": [
                "Comps-derived; reflects credit risk",
                "Sweetener for new bonds vs. secondary",
                "Corporate bonds less liquid than benchmark",
                "Tenor mismatch vs. comps",
                "Other market-specific factors",
                "Sum of all components"
            ]
        }
        df_spread = pd.DataFrame(spread_data)
        is_total = [False, False, False, False, False, True]
        s_rows = "".join([
            f'''<tr style="background:{GOLD+"22" if is_total[i] else ("#0d1f3c" if i%2==0 else CARD_BG)}; border-bottom:1px solid {MID_BLUE}33; border-top:{"2px solid "+GOLD+"66" if is_total[i] else "none"};">
              <td style="padding:9px 14px; color:{GOLD if is_total[i] else LT_BLUE}; -webkit-text-fill-color:{GOLD if is_total[i] else LT_BLUE}; font-weight:{"700" if is_total[i] else "400"}; font-size:0.82rem;">{row["Component"]}</td>
              <td style="padding:9px 14px; color:{GOLD if is_total[i] else "#ffffff"}; -webkit-text-fill-color:{GOLD if is_total[i] else "#ffffff"}; font-weight:{"700" if is_total[i] else "400"}; text-align:right;">{row["bps"]}</td>
              <td style="padding:9px 14px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; text-align:right;">{row["(%)"]}</td>
              <td style="padding:9px 14px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.78rem;">{row["Notes"]}</td>
            </tr>'''
            for i, row in df_spread.iterrows()
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Component</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">bps</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">%</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Notes</th>
            </tr></thead>
            <tbody>{s_rows}</tbody>
          </table>
        </div>
        """)

        # Total spread formula display
        st.html(f"""
        <div style="background:{CARD_BG}; border:1px solid {GOLD}66; border-left:4px solid {GOLD}; border-radius:10px; padding:16px; margin-top:12px; user-select:none;">
          <div style="color:{GOLD}; font-weight:700; font-size:0.85rem; margin-bottom:8px;">YTM Computation</div>
          <div style="color:{MUTED}; font-size:0.8rem;">
            Benchmark Yield: <span style="color:{TXT};">{benchmark_yield:.3f}%</span><br>
            + Total Spread: <span style="color:{TXT};">+{total_spread/100:.3f}%</span><br>
            <span style="border-top:1px solid {GOLD}44; display:block; padding-top:6px; margin-top:6px; color:{GOLD}; font-weight:700;">
              = YTM: {ytm*100:.4f}%
            </span>
            <span style="color:{LT_BLUE}; font-size:0.78rem;">
              Coupon (rounded to 1/8%): {coupon_rate*100:.3f}%
            </span>
          </div>
        </div>
        """)

    with col_r:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">📊 Spread Waterfall</div>')
        # Build waterfall data
        import altair as alt
        waterfall_df = pd.DataFrame({
            "Component": ["Benchmark", "Base Spread", "NIP", "Liq Prem", "Curve Adj", "Other", "YTM"],
            "Value": [benchmark_yield,
                      base_spread/100, nip/100, liq_prem/100,
                      curve_adj/100, other_adj/100,
                      ytm*100],
            "Type": ["Benchmark", "Spread", "Spread", "Spread", "Spread", "Spread", "YTM"]
        })
        color_map = {"Benchmark": MID_BLUE, "Spread": GOLD, "YTM": GREEN}
        chart = alt.Chart(waterfall_df).mark_bar(
            cornerRadiusTopLeft=4, cornerRadiusTopRight=4
        ).encode(
            x=alt.X("Component:N", sort=None, axis=alt.Axis(labelColor=TXT, titleColor=TXT, labelAngle=-20)),
            y=alt.Y("Value:Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT, format=".2f", title="Rate (%)")),
            color=alt.Color("Type:N", scale=alt.Scale(domain=list(color_map.keys()),
                            range=list(color_map.values())), legend=None),
            tooltip=["Component", alt.Tooltip("Value:Q", format=".3f", title="%")]
        ).properties(height=280, background="transparent").configure_axis(
            gridColor=MID_BLUE+"44"
        ).configure_view(strokeWidth=0)
        st.altair_chart(chart, use_container_width=True)

        # NIP explanation box
        st.html(f"""
        <div style="background:{CARD_BG}; border:1px solid {LT_BLUE}44; border-radius:10px; padding:14px; margin-top:8px; user-select:none;">
          <div style="color:{LT_BLUE}; font-weight:700; font-size:0.82rem; margin-bottom:6px;">📘 NIP Explained</div>
          <div style="color:{MUTED}; font-size:0.78rem; line-height:1.6;">
            The <span style="color:{TXT};">New Issue Premium</span> of <span style="color:{GOLD};">{nip} bps</span>
            compensates investors for:<br>
            • Buying an unproven new bond vs. tested secondary bonds<br>
            • Initial illiquidity before the bond season in the market<br>
            • Execution risk during the bookbuilding window<br><br>
            <span style="color:{MUTED};">Typical range: 5–25 bps (IG) | 25–50 bps (HY)</span>
          </div>
        </div>
        """)

# =============================================================================
# TAB 3 — FEES & PROCEEDS
# =============================================================================
with tab3:
    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">💸 Fee Structure</div>')
        fee_rows_data = [
            ("Management Fee",          f"{mgmt_fee:.2f}%",              f"{curr_sym}{notional*mgmt_fee/100:.3f}mm",  "Lead bookrunners",   False),
            ("Underwriting Fee",        f"{uwrt_fee:.2f}%",              f"{curr_sym}{notional*uwrt_fee/100:.3f}mm",  "All underwriters",   False),
            ("Selling Concession",      f"{sell_conc:.2f}%",             f"{curr_sym}{notional*sell_conc/100:.3f}mm", "All syndicate banks",False),
            ("Total Fees (Gross Spread)",f"{mgmt_fee+uwrt_fee+sell_conc:.2f}%",f"{curr_sym}{total_fees:.3f}mm",    "Banking syndicate",  True),
        ]
        f_rows = "".join([
            f'''<tr style="background:{GOLD+"22" if is_tot else ("#0d1f3c" if i%2==0 else CARD_BG)}; border-bottom:1px solid {MID_BLUE}33; border-top:{"2px solid "+GOLD+"66" if is_tot else "none"};">
              <td style="padding:9px 14px; color:{GOLD if is_tot else LT_BLUE}; -webkit-text-fill-color:{GOLD if is_tot else LT_BLUE}; font-weight:{"700" if is_tot else "400"}; font-size:0.82rem;">{comp}</td>
              <td style="padding:9px 14px; color:#ffffff; -webkit-text-fill-color:#ffffff; text-align:right;">{rate}</td>
              <td style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-weight:{"700" if is_tot else "400"}; text-align:right;">{amt}</td>
              <td style="padding:9px 14px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.78rem;">{recip}</td>
            </tr>'''
            for i,(comp,rate,amt,recip,is_tot) in enumerate(fee_rows_data)
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Fee Component</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Rate (%)</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Amount</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Recipient</th>
            </tr></thead>
            <tbody>{f_rows}</tbody>
          </table>
        </div>
        """)

    with col_r:
        st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:10px; user-select:none;">🏦 Proceeds Waterfall</div>')
        proceeds_data = {
            "Item": ["Face Value / Notional",
                     "Premium / (Discount) from par pricing",
                     "Gross Proceeds",
                     "Less: Management Fee",
                     "Less: Underwriting Fee",
                     "Less: Selling Concession",
                     "Net Proceeds to Issuer"],
            f"Amount ({curr_sym}mm)": [
                notional,
                gross_proceeds - notional,
                gross_proceeds,
                -(notional * mgmt_fee / 100),
                -(notional * uwrt_fee / 100),
                -(notional * sell_conc / 100),
                net_proceeds
            ]
        }
        proc_rows_list = [
            ("Face Value / Notional",            notional,                        False),
            ("Premium / (Discount) from par",    gross_proceeds - notional,       False),
            ("Gross Proceeds",                   gross_proceeds,                  False),
            ("Less: Management Fee",             -(notional*mgmt_fee/100),        False),
            ("Less: Underwriting Fee",           -(notional*uwrt_fee/100),        False),
            ("Less: Selling Concession",         -(notional*sell_conc/100),       False),
            ("Net Proceeds to Issuer",           net_proceeds,                    True),
        ]
        pr_rows = "".join([
            f'''<tr style="background:{GOLD+"22" if is_tot else ("#0d1f3c" if i%2==0 else CARD_BG)}; border-bottom:1px solid {MID_BLUE}33; border-top:{"2px solid "+GOLD+"66" if is_tot else "none"};">
              <td style="padding:9px 14px; color:{GOLD if is_tot else LT_BLUE}; -webkit-text-fill-color:{GOLD if is_tot else LT_BLUE}; font-weight:{"700" if is_tot else "400"}; font-size:0.82rem;">{label}</td>
              <td style="padding:9px 14px; color:{GOLD if is_tot else (GREEN if val>0 else (RED if val<0 else "#ffffff"))}; -webkit-text-fill-color:{GOLD if is_tot else (GREEN if val>0 else (RED if val<0 else "#ffffff"))}; font-weight:{"700" if is_tot else "400"}; text-align:right;">{curr_sym}{val:+,.3f}mm</td>
            </tr>'''
            for i,(label,val,is_tot) in enumerate(proc_rows_list)
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Item</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Amount ({curr_sym}mm)</th>
            </tr></thead>
            <tbody>{pr_rows}</tbody>
          </table>
        </div>
        """)

    st.divider()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Proceeds", f"{curr_sym}{gross_proceeds:,.3f}mm")
    m2.metric("Total Fees", f"{curr_sym}{total_fees:,.3f}mm",
              delta=f"-{(mgmt_fee+uwrt_fee+sell_conc):.2f}%")
    m3.metric("Net Proceeds", f"{curr_sym}{net_proceeds:,.3f}mm")
    m4.metric("All-In Cost", f"{all_in_cost*100:.4f}%",
              delta=f"+{(all_in_cost-coupon_rate)*100:.3f}% vs coupon")

    st.html(f"""
    <div style="background:{CARD_BG}; border:1px solid {GOLD}44; border-radius:10px; padding:16px; margin-top:14px; user-select:none;">
      <div style="color:{GOLD}; font-weight:700; font-size:0.85rem; margin-bottom:8px;">📌 All-In Cost Formula</div>
      <div style="color:{MUTED}; font-size:0.8rem;">
        All-In Cost = YTM + (Total Fee Rate / Tenor)
        = {ytm*100:.4f}% + ({(mgmt_fee+uwrt_fee+sell_conc):.2f}% / {tenor:.2f})
        = <span style="color:{GOLD}; font-weight:700;">{all_in_cost*100:.4f}%</span><br><br>
        <span style="color:{TXT};">The all-in cost is the true borrowing cost for the issuer.
        Use this as K<sub>d</sub> (pre-tax cost of debt) in WACC calculations — not the YTM.</span>
      </div>
    </div>
    """)

# =============================================================================
# TAB 4 — COMPS ANALYSIS
# =============================================================================
with tab4:
    st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:12px; user-select:none;">🔍 Comparable Bonds — Secondary Market Reference</div>')

    # Editable comps table
    comps_default = pd.DataFrame({
        "Issuer": ["XYZ Corp", "DEF Inc", "GHI Holdings", "JKL Corp", "MNO Industries"],
        "Rating": ["Baa2/BBB", "Baa1/BBB+", "Baa3/BBB-", "Baa2/BBB", "Baa2/BBB"],
        "Coupon (%)": [4.875, 5.125, 5.250, 4.750, 5.000],
        "Tenor (Yrs)": [9.2, 9.5, 9.7, 10.0, 10.2],
        "Spread (bps)": [145, 135, 165, 155, 148],
        "YTM (%)": [5.80, 5.65, 6.00, 5.90, 5.83],
        "Price ($)": [96.25, 97.50, 95.75, 95.125, 96.00]
    })

    edited_comps = st.data_editor(
        comps_default,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Issuer": st.column_config.TextColumn("Issuer"),
            "Rating": st.column_config.TextColumn("Rating"),
            "Coupon (%)": st.column_config.NumberColumn("Coupon (%)", format="%.3f"),
            "Tenor (Yrs)": st.column_config.NumberColumn("Tenor (Yrs)", format="%.1f"),
            "Spread (bps)": st.column_config.NumberColumn("Spread (bps)", format="%d"),
            "YTM (%)": st.column_config.NumberColumn("YTM (%)", format="%.2f"),
            "Price ($)": st.column_config.NumberColumn("Price ($)", format="%.3f"),
        }
    )

    spreads       = edited_comps["Spread (bps)"].values
    mean_spread   = np.mean(spreads)
    median_spread = np.median(spreads)
    min_spread    = np.min(spreads)
    max_spread    = np.max(spreads)
    nip_vs_mean   = reoffer_spread - mean_spread

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.html(f'<div style="color:{GOLD}; font-size:0.85rem; font-weight:700; margin:12px 0 8px; user-select:none;">📊 Comps Summary Statistics</div>')
        stats = {
            "Metric": ["Mean Spread", "Median Spread", "Min Spread", "Max Spread",
                       "Spread Range", "Our Reoffer Spread", "NIP vs. Mean"],
            "Value (bps)": [f"{mean_spread:.1f}", f"{median_spread:.1f}",
                            f"{min_spread:.0f}", f"{max_spread:.0f}",
                            f"{max_spread-min_spread:.0f}",
                            f"{reoffer_spread}",
                            f"{nip_vs_mean:+.1f}"]
        }
        st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)

    with col_r:
        st.html(f'<div style="color:{GOLD}; font-size:0.85rem; font-weight:700; margin:12px 0 8px; user-select:none;">📈 Spread Distribution</div>')
        chart_data = edited_comps[["Issuer", "Spread (bps)"]].copy()
        chart_data["Color"] = chart_data["Spread (bps)"].apply(
            lambda x: "Comp" if x != reoffer_spread else "New Issue"
        )
        # Add new issue row
        new_row = pd.DataFrame({"Issuer": [f"{issuer_name} (NEW)"],
                                  "Spread (bps)": [reoffer_spread],
                                  "Color": ["New Issue"]})
        chart_data = pd.concat([chart_data, new_row], ignore_index=True)

        bar = alt.Chart(chart_data).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
            x=alt.X("Issuer:N", sort=None, axis=alt.Axis(labelColor=TXT, labelAngle=-20)),
            y=alt.Y("Spread (bps):Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT)),
            color=alt.Color("Color:N", scale=alt.Scale(domain=["Comp","New Issue"],
                            range=[MID_BLUE, GOLD]), legend=None),
            tooltip=["Issuer", "Spread (bps)"]
        ).properties(height=220, background="transparent").configure_axis(
            gridColor=MID_BLUE+"44"
        ).configure_view(strokeWidth=0)
        st.altair_chart(bar, use_container_width=True)

    # Mean line annotation
    color_nip = GREEN if nip_vs_mean <= 20 else RED
    st.html(f"""
    <div style="background:{CARD_BG}; border:1px solid {color_nip}66; border-radius:10px; padding:14px 20px; margin-top:10px; user-select:none;">
      <span style="color:{GOLD}; font-weight:700;">📌 NIP vs. Comps Mean:</span>
      <span style="color:{TXT};"> Our reoffer spread of <strong>{reoffer_spread} bps</strong>
        is <span style="color:{color_nip}; font-weight:700;">{nip_vs_mean:+.1f} bps</span>
        vs. the comps mean of {mean_spread:.1f} bps.
        {"✅ NIP is within normal range (5–25 bps for IG)." if 5 <= nip_vs_mean <= 25
         else "⚠️ NIP is outside typical IG range — check market conditions." if nip_vs_mean > 25
         else "⚠️ New issue priced tighter than comps — very strong demand required."}
      </span>
    </div>
    """)

# =============================================================================
# TAB 5 — SENSITIVITY ANALYSIS
# =============================================================================
with tab5:
    st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:6px; user-select:none;">📊 Sensitivity Analysis</div>')

    sens_tab1, sens_tab2, sens_tab3 = st.tabs(["1D: Spread", "1D: Benchmark", "2D: Matrix"])

    # ── 1D SPREAD SENSITIVITY ────────────────────────────────────────────────
    with sens_tab1:
        st.html(f'<div style="color:{MUTED}; font-size:0.8rem; margin-bottom:10px; user-select:none;">Re-Offer Price vs. Credit Spread (±30 bps from base)</div>')
        spread_range = range(-30, 35, 5)
        sens_rows = []
        for delta in spread_range:
            s   = total_spread + delta
            y   = (benchmark_yield + s/100) / 100
            try:
                p = bond_price(settle_date, maturity_date, coupon_rate, y, 100, freq, 0)
            except:
                p = 100.0
            gp  = notional * (p / 100)
            sens_rows.append({
                "Δ Spread": f"{delta:+d} bps",
                "Spread (bps)": s,
                "YTM (%)": f"{y*100:.3f}",
                "Price": f"{p:.3f}",
                "Δ Price": f"{p-reoffer_price:+.3f}",
                "Gross Proceeds": f"{curr_sym}{gp:,.1f}mm",
                "Base?": "⭐ BASE" if delta == 0 else ""
            })
        df_sens1 = pd.DataFrame(sens_rows)
        st.dataframe(df_sens1, use_container_width=True, hide_index=True,
                     column_config={"Base?": st.column_config.TextColumn(width="small")})

        # Chart
        chart_df = pd.DataFrame({
            "Spread (bps)": [total_spread + d for d in spread_range],
            "Price": [float(r["Price"]) for r in sens_rows]
        })
        line = alt.Chart(chart_df).mark_line(color=GOLD, strokeWidth=2.5).encode(
            x=alt.X("Spread (bps):Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT)),
            y=alt.Y("Price:Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT),
                    scale=alt.Scale(zero=False)),
            tooltip=["Spread (bps)", alt.Tooltip("Price:Q", format=".3f")]
        )
        rule = alt.Chart(pd.DataFrame({"x": [100.0]})).mark_rule(
            color=GREEN, strokeDash=[4,4], strokeWidth=1.5
        ).encode(y="x:Q")
        base_pt = alt.Chart(pd.DataFrame({"x": [total_spread], "y": [reoffer_price]})).mark_point(
            color=GOLD, size=120, filled=True
        ).encode(x="x:Q", y="y:Q")
        (line + rule + base_pt).properties(height=240, background="transparent"
        ).configure_axis(gridColor=MID_BLUE+"44"
        ).configure_view(strokeWidth=0)
        st.altair_chart((line + rule + base_pt).properties(
            height=240, background="transparent"
        ).configure_axis(gridColor=MID_BLUE+"44"
        ).configure_view(strokeWidth=0), use_container_width=True)

    # ── 1D BENCHMARK SENSITIVITY ─────────────────────────────────────────────
    with sens_tab2:
        st.html(f'<div style="color:{MUTED}; font-size:0.8rem; margin-bottom:10px; user-select:none;">Re-Offer Price vs. Benchmark Yield (±75 bps from base)</div>')
        bench_range = [-75, -50, -25, -10, 0, 10, 25, 50, 75]
        bench_rows  = []
        for delta in bench_range:
            bm  = benchmark_yield + delta/100
            y   = (bm + total_spread/100) / 100
            try:
                p = bond_price(settle_date, maturity_date, coupon_rate, y, 100, freq, 0)
            except:
                p = 100.0
            gp  = notional * (p / 100)
            np_ = gp - total_fees
            bench_rows.append({
                "Δ Benchmark": f"{delta:+d} bps",
                "Benchmark (%)": f"{bm:.3f}",
                "YTM (%)": f"{y*100:.3f}",
                "Price": f"{p:.3f}",
                "Δ Price": f"{p-reoffer_price:+.3f}",
                "Net Proceeds": f"{curr_sym}{np_:,.1f}mm",
                "Base?": "⭐ BASE" if delta == 0 else ""
            })
        st.dataframe(pd.DataFrame(bench_rows), use_container_width=True, hide_index=True)

    # ── 2D SENSITIVITY MATRIX ─────────────────────────────────────────────────
    with sens_tab3:
        st.html(f'<div style="color:{MUTED}; font-size:0.8rem; margin-bottom:10px; user-select:none;">Re-Offer Price: Benchmark Yield Change (columns) × Credit Spread Change (rows)</div>')
        bench_deltas  = [-50, -25, -10, 0, 10, 25, 50]
        spread_deltas = [-30, -20, -10, 0, 10, 20, 30]
        matrix_rows   = []
        for sd in spread_deltas:
            row = {"Spread Δ \\ Bench Δ": f"{sd:+d} bps"}
            for bd in bench_deltas:
                bm = benchmark_yield + bd/100
                y  = (bm + (total_spread + sd)/100) / 100
                try:
                    p = bond_price(settle_date, maturity_date, coupon_rate, y, 100, freq, 0)
                except:
                    p = 100.0
                label = f"{'⭐' if bd==0 and sd==0 else ''}{p:.2f}"
                row[f"Bench {bd:+d}"] = p
            matrix_rows.append(row)

        df_matrix = pd.DataFrame(matrix_rows)

        # Style the dataframe
        def color_cell(val):
            if isinstance(val, float):
                if val > reoffer_price + 1:
                    return f"background-color: {GREEN}33; color: {GREEN}"
                elif val < reoffer_price - 1:
                    return f"background-color: {RED}33; color: {RED}"
                else:
                    return f"background-color: {GOLD}22; color: {GOLD}"
            return ""

        num_cols = [c for c in df_matrix.columns if c != "Spread Δ \\ Bench Δ"]
        styled = df_matrix.style.applymap(color_cell, subset=num_cols).format(
            "{:.3f}", subset=num_cols
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

        st.html(f"""
        <div style="background:{CARD_BG}; border:1px solid {MID_BLUE}; border-radius:8px; padding:12px 16px; margin-top:10px; user-select:none; display:flex; gap:24px; flex-wrap:wrap;">
          <span style="color:{GREEN}; font-size:0.8rem;">🟩 Price &gt; Base + 1: Favourable scenario</span>
          <span style="color:{GOLD}; font-size:0.8rem;">🟨 Price near base: Normal range</span>
          <span style="color:{RED}; font-size:0.8rem;">🟥 Price &lt; Base − 1: Adverse scenario</span>
          <span style="color:{TXT}; font-size:0.8rem;">⭐ = Base case ({reoffer_price:.3f})</span>
        </div>
        """)

        # Worst / Best case callouts
        all_prices = [row[f"Bench {bd:+d}"] for row in matrix_rows for bd in bench_deltas]
        best_price = max(all_prices)
        worst_price = min(all_prices)
        best_proceeds  = notional * best_price / 100
        worst_proceeds = notional * worst_price / 100

        bc1, bc2 = st.columns(2)
        with bc1:
            st.html(f"""
            <div style="background:#0d3322; border:1px solid {GREEN}66; border-radius:10px; padding:14px 18px; margin-top:10px; user-select:none;">
              <div style="color:{GREEN}; font-weight:700; font-size:0.88rem; margin-bottom:4px;">🏆 Best Case Scenario</div>
              <div style="color:{TXT}; font-size:0.82rem;">
                Price: <span style="color:{GREEN}; font-weight:700;">{curr_sym}{best_price:.3f}</span><br>
                Gross Proceeds: <span style="color:{GREEN};">{curr_sym}{best_proceeds:,.1f}mm</span><br>
                <span style="color:{MUTED};">Benchmark −50 bps + Spread −30 bps</span>
              </div>
            </div>
            """)
        with bc2:
            st.html(f"""
            <div style="background:#3d0d0d; border:1px solid {RED}66; border-radius:10px; padding:14px 18px; margin-top:10px; user-select:none;">
              <div style="color:{RED}; font-weight:700; font-size:0.88rem; margin-bottom:4px;">⚠️ Stress Scenario</div>
              <div style="color:{TXT}; font-size:0.82rem;">
                Price: <span style="color:{RED}; font-weight:700;">{curr_sym}{worst_price:.3f}</span><br>
                Gross Proceeds: <span style="color:{RED};">{curr_sym}{worst_proceeds:,.1f}mm</span><br>
                <span style="color:{MUTED};">Benchmark +50 bps + Spread +30 bps</span>
              </div>
            </div>
            """)

# =============================================================================
# TAB 6 — RISK METRICS
# =============================================================================
with tab6:
    st.html(f'<div style="color:{GOLD}; font-size:0.9rem; font-weight:700; margin-bottom:12px; user-select:none;">📐 Key Risk Metrics</div>')

    r1, r2, r3, r4, r5 = st.columns(5)
    r1.metric("Macaulay Duration", f"{mac_dur:.2f} yrs")
    r2.metric("Modified Duration", f"{mod_dur:.2f}")
    r3.metric("DV01 (per $1mm)", f"${dv01:.2f}")
    r4.metric("Convexity", f"{convexity:.2f}")
    r5.metric("Spread Duration", f"{mod_dur:.2f}")

    st.divider()

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.html(f'<div style="color:{GOLD}; font-size:0.85rem; font-weight:700; margin-bottom:8px; user-select:none;">📊 Duration & Risk Summary</div>')
        risk_rows_data = [
            ("Macaulay Duration",             f"{mac_dur:.4f} yrs",        "Avg time to recover investment"),
            ("Modified Duration",             f"{mod_dur:.4f}",            "% price change per 100 bps yield change"),
            ("Spread Duration",               f"{mod_dur:.4f}",            "Same as mod. duration (fixed-rate bond)"),
            (f"DV01 (per {curr_sym}1mm)",     f"{curr_sym}{dv01:.2f}",     f"Dollar change per 1 bp move"),
            (f"Total DV01 ({curr_sym}{notional:,.0f}mm)", f"{curr_sym}{dv01*notional:,.1f}", "Full portfolio DV01"),
            ("Convexity",                     f"{convexity:.2f}",          "Positive convexity favours investor"),
        ]
        rm_rows = "".join([
            f'''<tr style="background:{"#0d1f3c" if i%2==0 else CARD_BG}; border-bottom:1px solid {MID_BLUE}33;">
              <td style="padding:9px 14px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; font-size:0.82rem; font-weight:600;">{m}</td>
              <td style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.82rem; font-weight:700; text-align:right;">{v}</td>
              <td style="padding:9px 14px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.78rem;">{interp}</td>
            </tr>'''
            for i,(m,v,interp) in enumerate(risk_rows_data)
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Metric</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Value</th>
              <th style="padding:9px 14px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:left;">Interpretation</th>
            </tr></thead>
            <tbody>{rm_rows}</tbody>
          </table>
        </div>
        """)

        # Price impact table
        st.html(f'<div style="color:{GOLD}; font-size:0.85rem; font-weight:700; margin:14px 0 8px; user-select:none;">💥 Price Impact at Different Yield Moves</div>')
        yield_moves = [-100, -50, -25, -10, 10, 25, 50, 100]
        impact_rows = []
        for move in yield_moves:
            approx_price_change = -mod_dur * reoffer_price/100 * move/100 * 100
            convex_adj = 0.5 * convexity * reoffer_price/100 * (move/10000)**2 * 100
            total_change = approx_price_change + convex_adj
            impact_rows.append({
                "Yield Move (bps)": f"{move:+d}",
                "Duration Effect": f"{approx_price_change:+.3f}",
                "Convexity Adj.": f"{convex_adj:+.3f}",
                "Total Δ Price": f"{total_change:+.3f}",
                f"Δ Proceeds ({curr_sym}mm)": f"{notional*total_change/100:+.2f}"
            })
        impact_df = pd.DataFrame(impact_rows)
        imp_rows_html = "".join([
            f'''<tr style="background:{"#0d1f3c" if i%2==0 else CARD_BG}; border-bottom:1px solid {MID_BLUE}33;">
              <td style="padding:8px 12px; color:{GREEN if int(row["Yield Move (bps)"].replace("+","")) < 0 else RED if int(row["Yield Move (bps)"].replace("+","")) > 0 else GOLD}; -webkit-text-fill-color:{GREEN if int(row["Yield Move (bps)"].replace("+","")) < 0 else RED if int(row["Yield Move (bps)"].replace("+","")) > 0 else GOLD}; font-weight:700; text-align:right;">{row["Yield Move (bps)"]}</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:right;">{row["Duration Effect"]}</td>
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE}; text-align:right;">{row["Convexity Adj."]}</td>
              <td style="padding:8px 12px; color:{GREEN if float(row["Total Δ Price"].replace("+","")) > 0 else RED}; -webkit-text-fill-color:{GREEN if float(row["Total Δ Price"].replace("+","")) > 0 else RED}; font-weight:700; text-align:right;">{row["Total Δ Price"]}</td>
              <td style="padding:8px 12px; color:{GREEN if "+" in row[list(row.keys())[-1]] else RED}; -webkit-text-fill-color:{GREEN if "+" in row[list(row.keys())[-1]] else RED}; text-align:right;">{row[list(row.keys())[-1]]}</td>
            </tr>'''
            for i, row in enumerate(impact_rows)
        ])
        st.html(f"""
        <div style="border-radius:10px; border:1px solid {MID_BLUE}; overflow:hidden; user-select:none;">
          <table style="width:100%; border-collapse:collapse; background:{CARD_BG};">
            <thead><tr style="background:{DARK_BLUE};">
              <th style="padding:9px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Yield Move (bps)</th>
              <th style="padding:9px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Duration Effect</th>
              <th style="padding:9px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Convexity Adj.</th>
              <th style="padding:9px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Total Δ Price</th>
              <th style="padding:9px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.78rem; font-weight:700; text-align:right;">Δ Proceeds</th>
            </tr></thead>
            <tbody>{imp_rows_html}</tbody>
          </table>
        </div>
        """)

    with col_r:
        st.html(f'<div style="color:{GOLD}; font-size:0.85rem; font-weight:700; margin-bottom:8px; user-select:none;">📈 Price-Yield Relationship</div>')
        ytm_range = np.linspace(max(0.001, ytm - 0.04), ytm + 0.04, 80)
        prices_py  = []
        for y_val in ytm_range:
            try:
                p = bond_price(settle_date, maturity_date, coupon_rate, y_val, 100, freq, 0)
            except:
                p = 100.0
            prices_py.append(p)

        py_df = pd.DataFrame({"YTM (%)": ytm_range * 100, "Price": prices_py})
        base_point = pd.DataFrame({"YTM (%)": [ytm*100], "Price": [reoffer_price]})

        line_py = alt.Chart(py_df).mark_line(color=GOLD, strokeWidth=2.5).encode(
            x=alt.X("YTM (%):Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT, format=".2f")),
            y=alt.Y("Price:Q", axis=alt.Axis(labelColor=TXT, titleColor=TXT),
                    scale=alt.Scale(zero=False)),
            tooltip=[alt.Tooltip("YTM (%):Q", format=".3f"),
                     alt.Tooltip("Price:Q", format=".3f")]
        )
        base_dot = alt.Chart(base_point).mark_point(
            color=GREEN, size=150, filled=True
        ).encode(x="YTM (%):Q", y="Price:Q")
        par_rule = alt.Chart(pd.DataFrame({"y": [100.0]})).mark_rule(
            color=MID_BLUE, strokeDash=[4,4], strokeWidth=1.5
        ).encode(y="y:Q")

        chart_py = (line_py + base_dot + par_rule).properties(
            height=280, background="transparent"
        ).configure_axis(gridColor=MID_BLUE+"44").configure_view(strokeWidth=0)
        st.altair_chart(chart_py, use_container_width=True)

        # Convexity insight
        st.html(f"""
        <div style="background:{CARD_BG}; border:1px solid {LT_BLUE}44; border-radius:10px; padding:14px; margin-top:6px; user-select:none;">
          <div style="color:{LT_BLUE}; font-weight:700; font-size:0.82rem; margin-bottom:6px;">📘 Convexity Benefit</div>
          <div style="color:{MUTED}; font-size:0.78rem; line-height:1.6;">
            Convexity = <span style="color:{GOLD};">{convexity:.2f}</span> — Positive convexity means:<br>
            • When yields <span style="color:{GREEN};">fall 100 bps</span>: Price gains <em>more</em> than duration predicts<br>
            • When yields <span style="color:{RED};">rise 100 bps</span>: Price loses <em>less</em> than duration predicts<br>
            • This asymmetry is the <span style="color:{TXT};">"convexity advantage"</span> — why high-convexity bonds
            trade at tighter spreads and are preferred in volatile rate environments.
          </div>
        </div>
        """)


# =============================================================================
# TAB 7 — EDUCATION: Q&A LEARNING HUB
# =============================================================================
with tab7:

    st.html(f"""
    <div style="background:linear-gradient(135deg,{DARK_BLUE},{MID_BLUE}); border:1px solid {GOLD}55;
      border-radius:14px; padding:18px 24px; margin-bottom:20px; user-select:none;">
      <div style="color:{GOLD}; font-size:1.1rem; font-weight:800; margin-bottom:4px;">
        🎓 Bond Primary Market — Complete Learning Guide
      </div>
      <div style="color:{TXT}; font-size:0.84rem; line-height:1.6;">
        A structured Q&amp;A covering everything from the basics of bond issuance to advanced pricing mechanics,
        risk metrics, and real-world market practice. Use the topic selector to navigate sections.
      </div>
      <div style="color:{MUTED}; font-size:0.76rem; margin-top:6px;">
        Prof. V. Ravichandran &nbsp;|&nbsp; Fixed Income Securities &amp; Analysis &nbsp;|&nbsp;
        <a href="https://themountainpathacademy.com" style="color:{LT_BLUE};" target="_blank">themountainpathacademy.com</a>
      </div>
    </div>
    """)

    # ── TOPIC SELECTOR ─────────────────────────────────────────────────────
    topic = st.selectbox("📚 Choose a Topic", [
        "1. What is a Bond? Fundamentals",
        "2. Primary Market & New Issue Process",
        "3. Deal Terms Explained",
        "4. Benchmark Rates & the Yield Curve",
        "5. Credit Spread Buildup",
        "6. Bookbuilding: IPT → Guidance → Reoffer",
        "7. Bond Pricing: From Yield to Dollar Price",
        "8. Fee Structure & Net Proceeds",
        "9. Comparable Bonds Analysis",
        "10. Sensitivity Analysis",
        "11. Duration, DV01 & Convexity",
        "12. Risk Management & Hedging",
        "13. Glossary & Quick Reference",
    ], label_visibility="collapsed")

    def qa_block(q, a, idx):
        """Render a single Q&A block."""
        st.html(f"""
        <div style="background:{CARD_BG}; border:1px solid {MID_BLUE}44; border-left:4px solid {GOLD};
          border-radius:10px; padding:16px 20px; margin-bottom:14px; user-select:none;">
          <div style="color:{GOLD}; font-size:0.82rem; font-weight:800; margin-bottom:8px; letter-spacing:0.5px;">
            Q{idx}. {q}
          </div>
          <div style="color:{TXT}; font-size:0.83rem; line-height:1.75;">
            {a}
          </div>
        </div>
        """)

    def section_header(title, subtitle=""):
        st.html(f"""
        <div style="background:{DARK_BLUE}; border-radius:10px; padding:14px 20px; margin:20px 0 14px;
          border-bottom:3px solid {GOLD}; user-select:none;">
          <div style="color:{GOLD}; font-size:1rem; font-weight:800;">{title}</div>
          {f'<div style="color:{MUTED}; font-size:0.78rem; margin-top:3px;">{subtitle}</div>' if subtitle else ""}
        </div>
        """)

    def highlight(text, color=None):
        c = color or GOLD
        return f'<span style="color:{c}; font-weight:700; -webkit-text-fill-color:{c};">{text}</span>'

    def note_box(text):
        return f"""<div style="background:{MID_BLUE}22; border:1px solid {LT_BLUE}44; border-radius:8px;
          padding:10px 14px; margin-top:10px; color:{LT_BLUE}; font-size:0.8rem; line-height:1.6;">
          💡 <em>{text}</em></div>"""

    # ===========================================================================
    # TOPIC 1 — BOND FUNDAMENTALS
    # ===========================================================================
    if topic == "1. What is a Bond? Fundamentals":
        section_header("📘 Topic 1: What is a Bond? Fundamentals", "The building blocks every finance professional must know")

        qa_block("What is a bond?",
            f"""A bond is a {highlight("debt instrument")} — essentially a formal IOU issued by a borrower (the issuer)
            to lenders (investors). When you buy a bond, you are {highlight("lending money")} to the issuer.
            In return, the issuer promises two things:<br><br>
            1. {highlight("Coupon payments:")} Regular interest payments (usually semi-annual) during the life of the bond.<br>
            2. {highlight("Principal repayment:")} Return of the full face value (par value) on the maturity date.<br><br>
            <em>Example:</em> ABC Corporation issues a 6% bond with face value $1,000, maturing in 10 years.
            You receive $30 every 6 months for 10 years, then $1,000 back at maturity. Your total return if held
            to maturity is the Yield to Maturity (YTM).
            {note_box("Bond = Debt. Shareholder = Owner. Bondholder = Creditor. Bondholders rank ABOVE shareholders in liquidation.")}""", 1)

        qa_block("How is a bond different from a stock?",
            f"""<table style="width:100%; border-collapse:collapse; font-size:0.82rem;">
            <tr style="background:{DARK_BLUE};">
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:left;">Feature</th>
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:left;">Bond</th>
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:left;">Stock / Equity</th>
            </tr>
            <tr style="background:#0d1f3c;">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">Nature</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Debt — you are a creditor</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Equity — you are an owner</td>
            </tr>
            <tr style="background:{CARD_BG};">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">Income</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Fixed coupon (contractual)</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Dividends (discretionary)</td>
            </tr>
            <tr style="background:#0d1f3c;">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">Upside</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Limited (par + coupons)</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Unlimited (price appreciation)</td>
            </tr>
            <tr style="background:{CARD_BG};">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">Priority in default</td>
              <td style="padding:8px 12px; color:{GREEN}; -webkit-text-fill-color:{GREEN};">Senior — paid first</td>
              <td style="padding:8px 12px; color:{RED}; -webkit-text-fill-color:{RED};">Junior — paid last (residual)</td>
            </tr>
            <tr style="background:#0d1f3c;">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">Term</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Fixed maturity date</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT};">Perpetual (no maturity)</td>
            </tr>
            </table>""", 2)

        qa_block("What is 'par value' and why does price deviate from par?",
            f"""Par value (face value) is {highlight("$100 per $100 of notional")} — the amount repaid at maturity.
            Bond prices deviate from par because of the relationship between the coupon rate and current market yields:<br><br>
            • {highlight("Coupon > YTM → Price > $100 (Premium bond)")} — investors pay more upfront because future coupons exceed what the market currently offers.<br>
            • {highlight("Coupon < YTM → Price < $100 (Discount bond)")} — investors pay less because future coupons are below market rates.<br>
            • {highlight("Coupon = YTM → Price = $100 (Par bond)")} — investor gets exactly what the market demands.<br><br>
            In our model: Coupon = 6.000%, YTM = 5.950% → Price = $100.373 (slight premium).
            {note_box("Price and yield always move in OPPOSITE directions. This is the single most important bond concept.")}""", 3)

        qa_block("What is Yield to Maturity (YTM) and why does it matter?",
            f"""YTM is the {highlight("total annualised return")} an investor earns by buying the bond at its current price,
            receiving all coupons, and getting the face value back at maturity. It is the single most important number in bond pricing.<br><br>
            YTM accounts for: (1) the coupon stream, (2) any premium or discount vs. par, and (3) the time value of money across all cash flows.<br><br>
            <strong>Formula (conceptual):</strong><br>
            <code style="background:#0d1f3c; padding:4px 8px; border-radius:4px; color:{GOLD};">Price = Σ Coupon_t/(1+YTM/2)^t + Face/(1+YTM/2)^n</code><br><br>
            Why it matters: YTM is how ALL bonds are compared regardless of coupon, maturity, or price.
            A 3% bond priced at $85 may have the same YTM as a 6% bond priced at $112.
            {note_box("Never compare bonds by coupon alone. Always compare YTM.")}""", 4)

        qa_block("What are Investment Grade and High Yield bonds?",
            f"""Credit rating agencies (Moody's, S&P, Fitch) rate issuers on their ability to repay debt:<br><br>
            {highlight("Investment Grade (IG):")} Rated Baa3/BBB- or above. Lower default risk. Lower yields. Accessible to pension funds, insurance companies, most institutional investors.<br><br>
            {highlight("High Yield (HY) / Junk:")} Rated Ba1/BB+ or below. Higher default risk. Significantly higher yields (usually 300–600+ bps over Treasuries). More volatile.<br><br>
            <strong>Practical spread differences (approx.):</strong><br>
            • AAA: 40–80 bps | AA: 60–120 bps | A: 80–150 bps | BBB: 130–250 bps<br>
            • BB: 250–450 bps | B: 400–700 bps | CCC+: 700–1500+ bps
            {note_box("ABC Corp in our model is Baa2/BBB — lower-medium investment grade. Solid, but not top-tier.")}""", 5)

    # ===========================================================================
    # TOPIC 2 — PRIMARY MARKET
    # ===========================================================================
    elif topic == "2. Primary Market & New Issue Process":
        section_header("🏛️ Topic 2: Primary Market & New Issue Process", "How a bond goes from idea to investor accounts")

        qa_block("What is the primary market for bonds?",
            f"""The primary market is where bonds are {highlight("sold for the first time")} — directly from the issuer to investors.
            This is called a 'new issue' or 'primary issue'. After this initial sale, bonds trade between investors in the
            {highlight("secondary market")} (like a stock exchange but over-the-counter for bonds).<br><br>
            <strong>Why it matters:</strong> The issuer only receives cash from the primary market sale.
            Secondary market trading does not bring new money to the issuer — it just changes who holds the bond.
            {note_box("Primary market = New money to issuer. Secondary market = Existing bonds trading between investors.")}""", 1)

        qa_block("Who are the key participants in a bond new issue?",
            f"""<strong>{highlight("Issuer:")}</strong> The borrower — a corporation, bank, government, or supranational. Receives the net proceeds and is responsible for coupon payments and principal repayment.<br><br>
            <strong>{highlight("Bookrunners / Lead Managers:")}</strong> Investment banks (e.g., Goldman Sachs, JPMorgan, Citi) that structure, price, and distribute the bond. They 'run the book' — collect and manage investor orders.<br><br>
            <strong>{highlight("Co-Managers:")}</strong> Smaller banks in the syndicate that help sell to their investor clients for a portion of the selling concession.<br><br>
            <strong>{highlight("Investors:")}</strong> Pension funds, insurance companies, asset managers, hedge funds, sovereign wealth funds, and central banks. They place orders during bookbuilding.<br><br>
            <strong>{highlight("Rating Agencies:")}</strong> Moody's, S&P, Fitch — assign credit ratings that directly determine the credit spread.<br><br>
            <strong>{highlight("Legal Counsel:")}</strong> Draft the offering memorandum and indenture (legal bond contract).<br><br>
            <strong>{highlight("Trustee:")}</strong> A bank appointed to represent bondholders' interests and enforce the indenture.
            {note_box("On a major investment-grade deal, there can be 10–20 banks in the syndicate and 100–300 investor accounts.")}""", 2)

        qa_block("What is the step-by-step process of issuing a bond?",
            f"""<strong>Phase 1 — Mandate & Preparation (weeks before)</strong><br>
            Issuer selects bookrunners via a mandate beauty parade. Lawyers draft the offering memorandum.
            Rating agencies assign/confirm ratings. Investor roadshow is planned.<br><br>
            <strong>Phase 2 — Investor Education / Roadshow (1–5 days before)</strong><br>
            Bookrunners present the issuer's credit story to large investors. Gauge appetite for the deal.
            No pricing yet — just building relationships and demand awareness.<br><br>
            <strong>Phase 3 — Launch & Bookbuilding (1–3 days)</strong><br>
            Deal is officially announced. IPT (Initial Price Thoughts) sent to investors.
            Orders are collected. Book typically closes within hours for IG deals.<br><br>
            <strong>Phase 4 — Pricing (same day as book close)</strong><br>
            Final spread set. Coupon determined. Price calculated. Deal tombstone issued.<br><br>
            <strong>Phase 5 — Settlement (T+2)</strong><br>
            Bonds delivered to investors. Issuer receives net proceeds. Bonds begin trading in secondary market.
            {note_box("For a benchmark $500mm IG deal, the entire process from launch to pricing can take as little as 4–6 hours.")}""", 3)

        qa_block("What is a 'greenshoe' or over-allotment option?",
            f"""A {highlight("greenshoe")} (named after Green Shoe Manufacturing Co., the first company to use it) is the right
            for the issuer to sell {highlight("up to X% more bonds")} than the announced base size if investor demand is strong enough.<br><br>
            <strong>How it works:</strong><br>
            • Base deal announced: $500mm. Greenshoe: 15% = $75mm additional.<br>
            • If the book is 4× oversubscribed, the issuer exercises the greenshoe.<br>
            • Total issuance = $575mm at the same price and terms.<br><br>
            <strong>Benefits:</strong><br>
            • Issuer raises more capital at same all-in cost (no additional structuring fee).<br>
            • Larger deal = better secondary market liquidity.<br>
            • Reduces investor disappointment from heavy allocation cuts.
            {note_box("Greenshoes are more common in equity IPOs but increasingly used in bond markets, especially in Asia.")}""", 4)

    # ===========================================================================
    # TOPIC 3 — DEAL TERMS
    # ===========================================================================
    elif topic == "3. Deal Terms Explained":
        section_header("📋 Topic 3: Deal Terms Explained", "Understanding every field on a bond term sheet")

        qa_block("What is the 'notional' or face value, and is it what investors pay?",
            f"""{highlight("Notional / Face Value / Principal")} is the {highlight("amount the issuer promises to repay")} at maturity.
            It is the reference amount on which coupons are calculated. However, investors do NOT necessarily pay
            the face value — they pay the market price (which can be above or below par).<br><br>
            <strong>Example:</strong><br>
            • Notional: $500mm (total debt being raised)<br>
            • Price: $100.373 (slightly above par)<br>
            • Actual cash paid by investors: $500mm × 1.00373 = $501.865mm<br>
            • At maturity, issuer repays exactly $500mm (not $501.865mm)
            {note_box("The issuer's obligation at maturity is ALWAYS the notional amount, regardless of the issue price.")}""", 1)

        qa_block("What is the 'day count convention' and why does 30/360 matter?",
            f"""Day count conventions determine how interest accrues between coupon dates.
            {highlight("30/360")} assumes every month has 30 days and every year has 360 days.<br><br>
            <strong>Common conventions:</strong><br>
            • {highlight("30/360:")} US corporate bonds — simple, standardised<br>
            • {highlight("Actual/365:")} UK gilts, Indian government bonds<br>
            • {highlight("Actual/360:")} US Treasury bills, money market<br>
            • {highlight("Actual/Actual:")} US Treasury notes and bonds<br><br>
            <strong>Why it matters:</strong> On a $500mm bond at 6%, the difference between 30/360 and Act/365
            over a 6-month period can be thousands of dollars in accrued interest — significant at institutional scale.
            {note_box("Always check the day count convention when comparing bonds or calculating accrued interest.")}""", 2)

        qa_block("What is T+2 settlement and why not T+0 (same day)?",
            f"""T+2 means bonds are delivered and cash is transferred {highlight("2 business days after the trade date")}.
            For a trade on Monday, settlement is Wednesday.<br><br>
            <strong>Why T+2?</strong><br>
            1. {highlight("Operational processing:")} With 200+ investor accounts receiving allocations, back offices need time to confirm, reconcile, and instruct custodians.<br>
            2. {highlight("Fund transfers:")} Moving $500mm+ across clearing systems (DTC in the US, Euroclear/Clearstream in Europe) requires processing time.<br>
            3. {highlight("Documentation:")} Legal confirmations and trade tickets must be processed.<br>
            4. {highlight("Failed trades:")} T+2 provides a buffer for any discrepancies before money moves.<br><br>
            In some markets (India), T+1 is becoming standard as technology improves.
            {note_box("For the issuer, the bond proceeds land in their bank account on the settlement date, not the trade date.")}""", 3)

        qa_block("What is the minimum piece / denomination requirement?",
            f"""The {highlight("minimum piece")} (typically $100,000 for investment grade bonds) is the smallest amount
            an investor can purchase. The denomination ($1,000) is the face value of each individual bond unit.<br><br>
            <strong>Purpose of minimum piece:</strong><br>
            • Keeps the deal {highlight("institutional")} — prevents retail investors from buying in small amounts<br>
            • Reduces administrative burden of managing thousands of small investors<br>
            • Helps maintain {highlight("market discipline")} — retail investors are not the target<br><br>
            <strong>Denominations by market:</strong><br>
            • US IG bonds: $1,000 face, $100,000–$250,000 minimum<br>
            • US High Yield: $1,000 face, $1,000–$2,000 minimum (broader retail access)<br>
            • Eurobonds: €1,000 or €100,000 per bond<br>
            • Indian NCDs: ₹10 lakh (₹1,000,000) minimum for listed bonds
            {note_box("High yield bonds often have lower minimums because they're sometimes sold to high-net-worth retail investors.")}""", 4)

    # ===========================================================================
    # TOPIC 4 — BENCHMARK RATES
    # ===========================================================================
    elif topic == "4. Benchmark Rates & the Yield Curve":
        section_header("📈 Topic 4: Benchmark Rates & the Yield Curve", "The risk-free foundation of all bond pricing")

        qa_block("Why are government bonds used as the benchmark?",
            f"""Government bonds (US Treasuries, UK Gilts, German Bunds, GoI G-Secs) are considered
            {highlight("'risk-free'")} because governments in their own currency can always print money to repay debt
            (though this causes inflation). They provide the {highlight("pure time value of money")} with zero credit risk.<br><br>
            Corporate bonds are priced as a {highlight("spread above")} the risk-free rate because they carry
            credit risk (the company might default), liquidity risk (harder to sell quickly), and other risks.<br><br>
            <strong>The benchmark rate answers:</strong> "What return would I get if I took NO credit risk?"
            The credit spread then answers: "How much extra do I need for THIS company's credit risk?"
            {note_box("SOFR (Secured Overnight Financing Rate) has replaced LIBOR as the main floating-rate benchmark for USD bonds since 2023.")}""", 1)

        qa_block("What is the yield curve and how does its shape affect bond pricing?",
            f"""The {highlight("yield curve")} plots the yields of government bonds across different maturities (1M, 3M, 1Y, 2Y, 5Y, 10Y, 30Y)
            at a single point in time. Its shape signals economic expectations:<br><br>
            {highlight("Normal (upward sloping):")} Short rates < Long rates. Investors demand more for lending long-term.
            Typical in normal economic conditions. {highlight("→ Most common shape.")}<br><br>
            {highlight("Flat:")} Similar yields across all maturities. Signals economic uncertainty or transition.<br><br>
            {highlight("Inverted:")} Short rates > Long rates. Often precedes recessions. The 2-year/10-year inversion
            has preceded every US recession since 1955.<br><br>
            {highlight("Humped:")} Medium-term rates highest. Uncommon; signals specific supply/demand dynamics.<br><br>
            <strong>Effect on bond pricing:</strong> A 10-year corporate bond uses the 10-year Treasury yield as benchmark.
            If the curve is steep, the 10-year benchmark is much higher than the 2-year, making long-term bonds carry a higher yield.
            {note_box("When the yield curve inverts (happened in 2022-2023), it actually creates unusual situations where 2-year bonds yield MORE than 10-year bonds.")}""", 2)

        qa_block("What is 'interpolation' of benchmark yields?",
            f"""When a bond's maturity doesn't exactly match an on-the-run Treasury maturity,
            you {highlight("interpolate")} between the two nearest Treasuries.<br><br>
            <strong>Example:</strong> A 9.5-year corporate bond:<br>
            • 9-year Treasury yields: 4.10%<br>
            • 10-year Treasury yields: 4.25%<br>
            • Interpolated 9.5-year benchmark = 4.10% + 0.5 × (4.25% − 4.10%) = 4.10% + 0.075% = {highlight("4.175%")}<br><br>
            <strong>Why this matters:</strong> If you used the wrong benchmark, the implied credit spread is wrong,
            making the bond appear mispriced vs. comparables.
            {note_box("In our model, the bond is exactly 10 years — so the interpolated yield equals the 10-year Treasury yield exactly.")}""", 3)

    # ===========================================================================
    # TOPIC 5 — CREDIT SPREAD
    # ===========================================================================
    elif topic == "5. Credit Spread Buildup":
        section_header("📊 Topic 5: Credit Spread Buildup", "Why corporate bonds yield more than Treasuries")

        qa_block("What is a credit spread and how is it measured?",
            f"""A {highlight("credit spread")} is the additional yield (above the risk-free benchmark) that investors
            require to compensate for lending to a corporate issuer rather than the government.<br><br>
            Measured in {highlight("basis points (bps)")} where {highlight("100 bps = 1.00%")}.<br><br>
            <strong>Example:</strong><br>
            • 10-year Treasury: 4.25% yield<br>
            • ABC Corp 10-year bond: 5.95% yield<br>
            • Credit spread = 5.95% − 4.25% = 1.70% = {highlight("170 bps")}<br><br>
            The spread reflects the market's collective judgment on: credit risk, liquidity risk, new issue premium,
            structural features, and supply/demand dynamics.
            {note_box("Credit spreads widen in recessions/stress (investors demand more for risk) and tighten in bull markets (investors chase yield).")}""", 1)

        qa_block("What are the components of the spread buildup?",
            f"""The total credit spread is built component by component:<br><br>
            <strong>1. {highlight("Base Credit Spread (150 bps)")}</strong><br>
            The core compensation for the issuer's credit risk. Anchored to where comparable bonds
            (same rating, similar tenor) trade in the secondary market. This is the most important component.<br><br>
            <strong>2. {highlight("New Issue Premium / NIP (15 bps)")}</strong><br>
            A sweetener offered to investors to buy a NEW bond instead of existing secondary bonds.
            New bonds have initial illiquidity and unproven performance, so investors want extra.<br><br>
            <strong>3. {highlight("Liquidity Premium (5 bps)")}</strong><br>
            Corporate bonds are harder to trade quickly than Treasuries. Smaller or less frequent issuers
            pay more. A $10bn deal has lower liquidity premium than a $200mm deal.<br><br>
            <strong>4. {highlight("Curve Adjustment (0 bps)")}</strong><br>
            If comps have a different average tenor than the new bond, adjust for the credit curve slope.<br><br>
            <strong>5. {highlight("Other Adjustments (0 bps)")}</strong><br>
            Structural features: subordination, covenants, call options, sector-specific factors.
            {note_box("The Base Credit Spread is set empirically from comps analysis. The other components are judgement-based.")}""", 2)

        qa_block("What exactly is the New Issue Premium (NIP) and when is it higher or lower?",
            f"""The NIP is extra yield offered on a {highlight("new bond vs. existing bonds from the same issuer or similar issuers")}
            trading in the secondary market. It compensates for:<br><br>
            • {highlight("Initial illiquidity:")} New bonds take weeks/months to become freely traded<br>
            • {highlight("Price uncertainty:")} The bond has no market track record<br>
            • {highlight("Allocation risk:")} Investors may not get all they want; orders are cut<br>
            • {highlight("Execution risk:")} Deal could be pulled or repriced if market moves<br><br>
            <strong>NIP is HIGHER when:</strong><br>
            • Market volatility is elevated (wider bid/offer spreads)<br>
            • The issuer is not a frequent borrower (name risk)<br>
            • There is existing secondary market supply to compete with<br>
            • The deal is large relative to the investor base<br><br>
            <strong>NIP is LOWER when:</strong><br>
            • Market is very strong and investors are scrambling for paper<br>
            • The issuer is a household name (very familiar credit)<br>
            • The deal is small relative to demand
            {note_box("In our model, NIP = 15 bps but the effective NIP vs. comps mean was 20.4 bps — the extra 5.4 bps came from liquidity premium and curve adjustment.")}""", 3)

    # ===========================================================================
    # TOPIC 6 — BOOKBUILDING
    # ===========================================================================
    elif topic == "6. Bookbuilding: IPT → Guidance → Reoffer":
        section_header("📚 Topic 6: Bookbuilding Process", "The art and science of price discovery in bond markets")

        qa_block("What is bookbuilding and why is it used?",
            f"""Bookbuilding is the {highlight("price discovery process")} for new bond issues. Instead of the issuer
            setting a price unilaterally, bookrunners collect investor orders at various spread levels to
            find the market-clearing price.<br><br>
            <strong>Why not just set a fixed price?</strong><br>
            • Bond markets have no centralised exchange — prices are not publicly observable<br>
            • Demand varies enormously across investors and market conditions<br>
            • Too-tight pricing → deal fails to sell; too-wide pricing → issuer pays too much<br>
            • Bookbuilding efficiently aggregates information from 100–300 sophisticated investors<br><br>
            The result is a price that both {highlight("clears the market")} (all bonds are sold) and is
            {highlight("optimal for the issuer")} (lowest possible yield given market conditions).
            {note_box("The bookbuilding process typically takes 2–6 hours for a benchmark investment-grade deal.")}""", 1)

        qa_block("What is IPT (Initial Price Thoughts) and why is it set wide?",
            f"""IPT is the {highlight("first spread indication")} sent by bookrunners to the investor community.
            It is deliberately set {highlight("wider (higher yield) than where the deal is expected to price")}.<br><br>
            <strong>Why set wide?</strong><br>
            1. {highlight("Anchoring strategy:")} A wide starting point creates room to tighten (which signals strong demand)<br>
            2. {highlight("Investor attraction:")} Wide spread attracts more orders from a broader investor base<br>
            3. {highlight("Buffer for uncertainty:")} If markets deteriorate, there's room to price at the IPT level<br>
            4. {highlight("Negotiating position:")} Bookrunners can use strong demand to justify tightening<br><br>
            In our model: IPT = 185 bps, Final reoffer = 170 bps. The 15 bps tightening signals the book was well oversubscribed.
            {note_box("If a deal prices at or wider than IPT, it signals weak demand — a negative signal for the secondary market.")}""", 2)

        qa_block("How do you interpret oversubscription ratios?",
            f"""The {highlight("oversubscription ratio")} = Total orders received ÷ Deal size<br><br>
            In our model: $1,750mm orders ÷ $500mm deal = {highlight("3.5×")}<br><br>
            <strong>Interpretation guide:</strong><br>
            • {highlight("Below 1.5×:")} Weak. Deal struggles to fully sell. Potential secondary market weakness.<br>
            • {highlight("1.5× – 2.5×:")} Adequate. Deal works but limited ability to tighten.<br>
            • {highlight("2.5× – 4×:")} Strong. Comfortable tightening of 5–15 bps from IPT.<br>
            • {highlight("4× – 6×:")} Very strong. Aggressive tightening possible. May increase deal size.<br>
            • {highlight("Above 6×:")} Exceptional. Significant tightening and/or greenshoe likely.<br><br>
            However, oversubscription ratios can be inflated by {highlight("'demand inflation'")} — some investors
            put in orders 2–3× their desired allocation expecting to be cut.
            {note_box("Quality of the book matters as much as size. 200 real-money accounts is better than 500 hedge fund accounts.")}""", 3)

        qa_block("What happens after the book closes and the deal prices?",
            f"""<strong>1. Allocation:</strong> Bookrunners decide how to distribute bonds among investors.
            Priority given to long-only accounts (pension funds, insurance), regional diversity, and investors
            who provided price discovery (indicated early, at tight levels).<br><br>
            <strong>2. Trade confirmation:</strong> Each investor receives a trade confirmation showing allocated amount,
            price, settlement date, and ISIN number.<br><br>
            <strong>3. Secondary market trading:</strong> Bonds begin trading 'when issued' (WI) immediately
            after pricing, before settlement. Early trading shows whether the deal priced correctly.<br><br>
            <strong>4. Settlement (T+2):</strong> Cash transfers to issuer; bonds delivered to investors' custodians.<br><br>
            <strong>5. Post-issue performance:</strong> How tight the bond trades vs. reoffer spread ('new issue performance')
            determines the issuer's reputation for future deals.
            {note_box("A bond that trades 5 bps tighter than reoffer on Day 1 ('5 bps through issue') is a big win. Trading 10 bps wider is bad news.")}""", 4)

    # ===========================================================================
    # TOPIC 7 — BOND PRICING
    # ===========================================================================
    elif topic == "7. Bond Pricing: From Yield to Dollar Price":
        section_header("💹 Topic 7: Bond Pricing", "The mathematics of converting yield to dollar price")

        qa_block("How is a bond price calculated from yield?",
            f"""A bond's price is the {highlight("present value of all future cash flows")} discounted at the YTM:<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0; font-size:0.85rem;">
            Price = Σ [Coupon/2 ÷ (1 + YTM/2)^t] + [Face ÷ (1 + YTM/2)^n]
            </code>
            Where t goes from 1 to 2n (semi-annual periods) and n = tenor in years.<br><br>
            <strong>For ABC Corp (6% coupon, 5.95% YTM, 10 years semi-annual):</strong><br>
            • 20 coupon payments of $3.00 (semi-annual) discounted at 2.975% per period<br>
            • 1 principal payment of $100 discounted at 2.975% for 20 periods<br>
            • Sum = $100.373<br><br>
            In Excel: <code style="background:#0d1f3c; padding:3px 8px; border-radius:4px; color:{GOLD};">
            =PRICE(settlement, maturity, coupon, yield, 100, 2, 0)</code>
            {note_box("Arguments: 2 = semi-annual frequency; 0 = 30/360 day count convention.")}""", 1)

        qa_block("Why is the coupon rounded to the nearest 1/8%?",
            f"""Bond coupons are stated in the {highlight("indenture (legal bond document)")} and must be fixed
            fractions. The 1/8% (0.125%) increment is a century-old US bond market convention.<br><br>
            <strong>Rounding formula:</strong><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            Coupon = ROUND(YTM × 100 × 8, 0) ÷ 8 ÷ 100
            </code>
            <strong>Example:</strong> YTM = 5.950%<br>
            → 5.950 × 8 = 47.6 → ROUND(47.6, 0) = 48 → 48 ÷ 8 ÷ 100 = {highlight("6.000%")}<br><br>
            <strong>Effect of rounding:</strong><br>
            • Coupon rounds UP from 5.950% to 6.000% → bond prices at premium ($100.373)<br>
            • If rounded down to 5.875%, bond would price at discount (below $100)<br>
            • Issuers prefer rounding up as it results in above-par proceeds
            {note_box("Indian bond market uses 0.05% increments. European markets use 0.01% increments.")}""", 2)

        qa_block("What is accrued interest and when does it apply?",
            f"""Accrued interest is the {highlight("interest that has built up since the last coupon payment")}
            but has not yet been paid. Bond buyers compensate sellers for this accrued interest.<br><br>
            <strong>Clean price vs. Dirty price:</strong><br>
            • {highlight("Clean price:")} The price quoted on screens — excludes accrued interest<br>
            • {highlight("Dirty price:")} What the buyer actually pays = Clean price + Accrued interest<br><br>
            <strong>Formula:</strong>
            <code style="background:#0d1f3c; padding:6px 12px; border-radius:4px; color:{GOLD}; display:block; margin:6px 0;">
            Accrued = Face × Coupon × (Days since last coupon) ÷ (Days in coupon period)
            </code>
            <strong>For new issues:</strong> Settlement date = dated date (start of interest accrual),
            so Accrued = $0. Dirty price = Clean price = $100.373.
            {note_box("If you buy a bond 3 months after issue (one quarter into a semi-annual coupon period), you pay ~$15 per $1,000 in accrued interest to the seller.")}""", 3)

        qa_block("How do proceeds exceed the face value amount raised?",
            f"""When a bond prices {highlight("above par")} (premium), the issuer receives MORE than the face value:<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            Gross Proceeds = Notional × (Dirty Price ÷ 100)<br>
            = $500mm × (100.373 ÷ 100) = $500mm × 1.00373 = $501.865mm
            </code>
            The issuer receives $1.865mm MORE than the $500mm they promised to repay at maturity.
            This 'bonus' arises because the 1/8% coupon rounding took the coupon from 5.950% to 6.000%.<br><br>
            <strong>At maturity:</strong> Issuer repays exactly $500mm (the face value), not $501.865mm.
            The premium is 'amortised' over the life of the bond — each coupon period, the premium
            reduces slightly until the bond is worth exactly $100 at maturity.
            {note_box("On a discount bond (price below $100), the issuer receives LESS than face value but still repays the full face value at maturity.")}""", 4)

    # ===========================================================================
    # TOPIC 8 — FEES
    # ===========================================================================
    elif topic == "8. Fee Structure & Net Proceeds":
        section_header("💰 Topic 8: Fee Structure & Net Proceeds", "Who gets paid what in a bond new issue")

        qa_block("What is the 'gross spread' and how is it divided?",
            f"""The {highlight("gross spread")} is the total underwriting fee charged by the banking syndicate,
            expressed as a percentage of face value. It has three components:<br><br>
            <strong>1. {highlight("Management Fee (0.20%)")}</strong><br>
            Paid to lead managers (bookrunners) for: structuring the deal, preparing the offering memorandum,
            coordinating with lawyers and rating agencies, managing the bookbuilding process,
            and taking primary responsibility for execution risk.<br><br>
            <strong>2. {highlight("Underwriting Fee (0.25%)")}</strong><br>
            Compensation for taking {highlight("underwriting risk")} — the commitment to buy ALL bonds from the
            issuer even if they cannot sell them all to investors. If markets collapse between pricing and
            settlement, underwriters may be 'stuck' holding bonds at a loss.<br><br>
            <strong>3. {highlight("Selling Concession (0.20%)")}</strong><br>
            Paid to banks for actually distributing bonds to their investor clients.
            The more a bank sells, the more concession it earns. This incentivises broad distribution.
            {note_box("Total fees on our deal: 0.65% × $500mm = $3.25mm. Investment banking fees seem small as a % but are enormous in dollar terms.")}""", 1)

        qa_block("How does the all-in cost differ from the YTM?",
            f"""The YTM of 5.950% is the yield {highlight("paid to investors")}. But the issuer's true borrowing cost
            is higher because it also pays the underwriting fee. The {highlight("all-in cost")} captures both:<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            All-In Cost = YTM + (Total Fee Rate ÷ Tenor)<br>
            = 5.950% + (0.65% ÷ 10) = 5.950% + 0.065% = 6.015%
            </code>
            <strong>Why this matters for WACC:</strong><br>
            When calculating WACC, use the {highlight("all-in cost")} as the pre-tax cost of debt (K_d),
            not the YTM. The fees represent a real cash outflow to the issuer that increases the effective
            borrowing cost above the yield paid to investors.
            {note_box("For short-term bonds (1–3 years), the annualised fee impact is much larger. A 0.65% fee on a 2-year bond adds 0.325% to the all-in cost.")}""", 2)

        qa_block("Why do high-yield bonds have much higher fees than investment grade?",
            f"""High yield (HY) bonds carry fees of {highlight("1.5–2.5%")} vs. 0.5–0.75% for investment grade because:<br><br>
            <strong>1. {highlight("Higher underwriting risk:")}</strong> HY bonds are much harder to place.
            If the deal struggles, underwriters may be stuck with large positions in risky bonds.<br><br>
            <strong>2. {highlight("More work:")}</strong> HY deals require deeper credit analysis, more investor meetings,
            longer marketing periods, and more complex documentation.<br><br>
            <strong>3. {highlight("Market volatility:")}</strong> HY spreads are more volatile — the deal can gap out
            significantly between commitment and pricing.<br><br>
            <strong>4. {highlight("Smaller investor universe:")}</strong> Fewer investors buy HY, making distribution
            harder and more time-intensive.<br><br>
            On a $500mm HY deal at 2%: fees = $10mm vs. $3.25mm for our IG deal.
            {note_box("HY issuers typically pay 150–200 bps more in yield AND much higher fees. This is the true cost of a weak balance sheet.")}""", 3)

    # ===========================================================================
    # TOPIC 9 — COMPS
    # ===========================================================================
    elif topic == "9. Comparable Bonds Analysis":
        section_header("🔍 Topic 9: Comparable Bonds Analysis", "Anchoring new issue pricing in market reality")

        qa_block("Why do we need comparable bonds analysis?",
            f"""Comparable bonds (comps) analysis {highlight("anchors the base credit spread")} in real market data.
            Without comps, pricing would be arbitrary — the issuer would want 50 bps, investors would demand 250 bps,
            and there would be no objective reference.<br><br>
            Comps answer: {highlight('"Where do similar bonds trade in the secondary market right now?"')}<br><br>
            If 5 similar bonds trade at 130–165 bps, pricing a new bond at 100 bps is unrealistic (investors won't buy)
            and pricing at 250 bps is too expensive for the issuer. The comps narrow the range to roughly 145–175 bps,
            with the specific point determined by the NIP and deal-specific factors.
            {note_box("Comps analysis is like checking Zillow before pricing a house. You need to know what comparable properties are selling for.")}""", 1)

        qa_block("What makes a 'good comp'?",
            f"""A good comparable bond should match the new bond as closely as possible on:<br><br>
            <strong>{highlight("1. Credit rating:")}</strong> Same rating tier (Baa2/BBB for our deal).<br>
            <strong>{highlight("2. Industry/sector:")}</strong> Same or similar sector (same credit dynamics).<br>
            <strong>{highlight("3. Tenor:")}</strong> Within ±2 years of the new bond's maturity.<br>
            <strong>{highlight("4. Currency:")}</strong> Same currency and market (USD for our deal).<br>
            <strong>{highlight("5. Recency:")}</strong> Prices should be current (within days), not stale.<br>
            <strong>{highlight("6. Seniority:")}</strong> Same ranking in the capital structure (senior unsecured).<br>
            <strong>{highlight("7. Size:")}</strong> Comparable notional (large enough to trade well).<br><br>
            If the perfect comp doesn't exist, use the closest available and adjust for differences
            (e.g., add 5–10 bps for a lower-rated comp; subtract for a tighter tenor).
            {note_box("Even with good comps, pricing is still an art — market technicals, supply/demand, and timing all matter.")}""", 2)

        qa_block("How do you interpret the NIP vs. comps mean?",
            f"""The NIP vs. comps mean = {highlight("Reoffer spread − Comps mean spread")}<br><br>
            In our model: 170 bps − 149.6 bps = {highlight("+20.4 bps effective NIP")}<br><br>
            <strong>What the number tells you:</strong><br>
            • The issuer paid 20.4 bps MORE than where secondary comps trade<br>
            • Investors received a 20.4 bps 'gift' for buying the new issue<br>
            • This gap closes over time as the new bond 'seasons' and trades in line with comps<br><br>
            <strong>Healthy NIP range for IG bonds:</strong><br>
            • 5–15 bps: tight market, strong demand, experienced issuer<br>
            • 15–25 bps: normal market, typical NIP<br>
            • 25–50 bps: weak market OR unusual issuer (first-time, less-known name)<br>
            • >50 bps: very weak market or distressed name
            {note_box("A bond that prices at 0 NIP (in line with comps) is exceptional — requires a very popular issuer in ideal market conditions.")}""", 3)

    # ===========================================================================
    # TOPIC 10 — SENSITIVITY
    # ===========================================================================
    elif topic == "10. Sensitivity Analysis":
        section_header("📊 Topic 10: Sensitivity Analysis", "Understanding how price responds to market changes")

        qa_block("Why do bonds need sensitivity analysis?",
            f"""Bond pricing is highly sensitive to market conditions that can change rapidly between
            deal announcement and pricing. Sensitivity analysis helps:<br><br>
            <strong>{highlight("1. Issuers:")}</strong> Decide whether to proceed with the deal or wait for better conditions.<br>
            <strong>{highlight("2. Underwriters:")}</strong> Assess underwriting risk — how much can the bank lose if markets move?<br>
            <strong>{highlight("3. Investors:")}</strong> Understand the price risk of their new bond allocation.<br>
            <strong>{highlight("4. Risk managers:")}</strong> Quantify interest rate exposure for hedging.<br><br>
            Example: An issuer might say: "We're comfortable pricing if the 10-year Treasury stays below 4.75%.
            If it breaches 4.75%, we'll pull the deal and wait."
            {note_box("Major deals have been pulled (cancelled mid-bookbuilding) due to sudden market deterioration. This is a real risk.")}""", 1)

        qa_block("How do you read a 2D sensitivity matrix?",
            f"""The 2D matrix shows bond prices across {highlight("two simultaneously changing variables")}
            — typically the benchmark yield and the credit spread.<br><br>
            <strong>How to navigate the matrix:</strong><br>
            • {highlight("Start at the centre (gold cell)")} — this is the base case.<br>
            • {highlight("Moving RIGHT (column by column)")} — benchmark yield rises → price falls.<br>
            • {highlight("Moving DOWN (row by row)")} — credit spread widens → price falls.<br>
            • {highlight("Top-left corner")} — best case (rates fall + spreads tighten).<br>
            • {highlight("Bottom-right corner")} — worst case (rates rise + spreads widen).<br><br>
            <strong>Practical use:</strong><br>
            Identify which combinations cause the bond to price below par ($100).
            Any scenario where Price < 100 means the issuer raises less than the face value.
            {note_box("The diagonal from top-right to bottom-left represents scenarios where rate moves and spread moves offset each other — the price stays near par.")}""", 2)

        qa_block("What does a $1 change in price mean for the issuer?",
            f"""On a $500mm notional deal, each $1 change in price (per $100 face) translates to:<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            Proceeds change = Notional × (ΔPrice ÷ 100) = $500mm × (1 ÷ 100) = $5mm
            </code>
            So a $1 price move = $5mm change in gross proceeds on our deal.<br><br>
            In our sensitivity table:<br>
            • Best case (+2.22 price): Extra $11.1mm proceeds vs. base<br>
            • Worst case (−2.17 price): $10.85mm fewer proceeds vs. base<br><br>
            This is why deal timing matters enormously. A 2-day delay that allows markets to improve can
            be worth millions in lower borrowing costs.
            {note_box("For a 30-year bond, the same 100 bps yield move produces roughly 3× the price impact vs. a 10-year bond (higher duration).")}""", 3)

    # ===========================================================================
    # TOPIC 11 — DURATION, DV01, CONVEXITY
    # ===========================================================================
    elif topic == "11. Duration, DV01 & Convexity":
        section_header("📐 Topic 11: Duration, DV01 & Convexity", "Quantifying interest rate risk")

        qa_block("What is duration and why does it matter?",
            f"""Duration is the {highlight("sensitivity of a bond's price to interest rate changes")}.
            There are two main types:<br><br>
            <strong>{highlight("Macaulay Duration (7.45 years):")}</strong><br>
            The weighted average time until you receive the bond's cash flows, measured in years.
            For a zero-coupon bond, Macaulay Duration = Tenor (all cash flow at maturity).
            For a coupon bond, it's less than tenor (coupons arrive before maturity).<br><br>
            <strong>{highlight("Modified Duration (7.23):")}</strong><br>
            The percentage price change for a 100 bps change in yield.
            <code style="background:#0d1f3c; padding:4px 8px; border-radius:4px; color:{GOLD};">
            Mod Duration = Mac Duration ÷ (1 + YTM/2)</code><br><br>
            Interpretation: If rates rise 100 bps, this bond's price falls approximately 7.23%.
            On $500mm: price loss ≈ $500mm × 7.23% = {highlight("$36.15mm")}
            {note_box("Duration is sometimes called 'the half-life of a bond' — it tells you how long it takes to get half your investment back through cash flows.")}""", 1)

        qa_block("What is DV01 and how do traders use it?",
            f"""DV01 (Dollar Value of 01) is the {highlight("dollar change in bond value for a 1 basis point (0.01%) move in yield")}.<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            DV01 = Mod Duration × (Price÷100) × 0.0001 × (1,000,000÷100)<br>
            = 7.23 × (100.373÷100) × 0.0001 × 10,000 = $7.26 per $1mm face
            </code>
            <strong>On the full $500mm deal:</strong> DV01 = $7.26 × 500 = {highlight("$3,630 per basis point")}<br><br>
            <strong>How traders use DV01:</strong><br>
            • To size Treasury future hedges: Hedge ratio = Bond DV01 ÷ Futures DV01<br>
            • To compare risk across different bonds regardless of size<br>
            • To set position limits: "max $50,000 DV01 per portfolio"<br>
            • To calculate P&L on yield moves: 10 bps move = 10 × $3,630 = $36,300 P&L
            {note_box("DV01 is the lingua franca of fixed income trading desks. All bond positions are sized and managed in DV01 terms.")}""", 2)

        qa_block("What is convexity and why does it favour investors?",
            f"""Convexity measures the {highlight("curvature of the price-yield relationship")}.
            Duration assumes a linear (straight-line) relationship, but the actual relationship is curved (convex).<br><br>
            <code style="background:#0d1f3c; padding:8px 14px; border-radius:6px; color:{GOLD}; display:block; margin:8px 0;">
            Convexity = [P(y-Δy) + P(y+Δy) - 2×P(y)] ÷ [P(y) × (Δy)²]
            </code>
            <strong>Why positive convexity favours investors:</strong><br>
            • When yields {highlight("fall 100 bps")}: Actual price rise > Duration prediction (you gain MORE)<br>
            • When yields {highlight("rise 100 bps")}: Actual price fall < Duration prediction (you lose LESS)<br><br>
            This asymmetry is the "convexity gift" — investors win more in bull scenarios than they lose in bear scenarios.<br><br>
            <strong>Price change with convexity correction:</strong><br>
            ΔPrice ≈ (−ModDur × Δy) + (½ × Convexity × Δy²)
            {note_box("High convexity bonds trade at tighter spreads because investors accept lower yield for the convexity benefit. Zero-coupon bonds have the highest convexity.")}""", 3)

        qa_block("What is the duration rule of thumb for different bond tenors?",
            f"""<table style="width:100%; border-collapse:collapse; font-size:0.82rem;">
            <tr style="background:{DARK_BLUE};">
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:left;">Bond Tenor</th>
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center;">Zero Coupon Duration</th>
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center;">Typical IG Duration</th>
              <th style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center;">Price Move per 100 bps</th>
            </tr>
            <tr style="background:#0d1f3c;">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">2 years</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">2.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">1.8–1.95</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">~1.9%</td>
            </tr>
            <tr style="background:{CARD_BG};">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">5 years</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">5.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">4.3–4.6</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">~4.5%</td>
            </tr>
            <tr style="background:#0d1f3c; border:2px solid {GOLD}44;">
              <td style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-weight:700;">10 years (our bond)</td>
              <td style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center; font-weight:700;">10.0</td>
              <td style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center; font-weight:700;">7.0–8.0</td>
              <td style="padding:8px 12px; color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-align:center; font-weight:700;">~7.2%</td>
            </tr>
            <tr style="background:{CARD_BG};">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">20 years</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">20.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">11.0–13.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">~12%</td>
            </tr>
            <tr style="background:#0d1f3c;">
              <td style="padding:8px 12px; color:{LT_BLUE}; -webkit-text-fill-color:{LT_BLUE};">30 years</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">30.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">15.0–18.0</td>
              <td style="padding:8px 12px; color:{TXT}; -webkit-text-fill-color:{TXT}; text-align:center;">~16%</td>
            </tr>
            </table>
            {note_box("Higher coupon → lower duration (you get money back sooner through coupons). That's why a 6% coupon 10-year bond has lower duration than a 3% coupon 10-year bond.")}""", 4)

    # ===========================================================================
    # TOPIC 12 — RISK MANAGEMENT
    # ===========================================================================
    elif topic == "12. Risk Management & Hedging":
        section_header("🛡️ Topic 12: Risk Management & Hedging", "Managing interest rate and credit risk in bond portfolios")

        qa_block("What are the key risks in a bond new issue?",
            f"""<strong>{highlight("1. Interest Rate Risk (Market Risk):")}</strong><br>
            The risk that rates move against the issuer or underwriter between pricing and settlement.
            A 25 bps rise in yields after pricing → bond loses ~1.8% of value → $9mm loss on $500mm deal
            that underwriters are stuck holding until T+2.<br><br>
            <strong>{highlight("2. Credit Spread Risk:")}</strong><br>
            Spreads can widen suddenly due to issuer-specific news, sector contagion, or market risk-off.
            A 20 bps spread widening = ~$5.8mm mark-to-market loss on $500mm.<br><br>
            <strong>{highlight("3. Execution Risk (Pull Risk):")}</strong><br>
            The deal might be pulled (cancelled mid-bookbuilding) if market conditions deteriorate.
            The issuer has wasted legal/ratings fees ($500k–$2mm); underwriters have reputation cost.<br><br>
            <strong>{highlight("4. Refinancing Risk:")}</strong><br>
            For the issuer: what if rates are much higher when this bond matures in 10 years?
            The issuer will have to refinance at a higher rate.
            {note_box("Underwriters hedge their interest rate risk from pricing to settlement using Treasury futures, typically selling futures to offset long bond exposure.")}""", 1)

        qa_block("How do underwriters hedge their exposure between pricing and settlement?",
            f"""From T (pricing) to T+2 (settlement), the underwriter is {highlight("long the corporate bond")}
            (committed to pay the issuer) but hasn't yet received cash from investors.
            This creates interest rate risk. The hedge:<br><br>
            <strong>Step 1:</strong> Calculate the DV01 of the corporate bond position.<br>
            For $500mm bond at DV01 = $7.26/mm: Total DV01 = $3,630/bp<br><br>
            <strong>Step 2:</strong> Find the equivalent Treasury future hedge.<br>
            10-year Treasury futures DV01 ≈ $95/contract (per basis point)<br><br>
            <strong>Step 3:</strong> Sell futures to offset.<br>
            <code style="background:#0d1f3c; padding:6px 12px; border-radius:4px; color:{GOLD}; display:block; margin:6px 0;">
            Contracts = Bond DV01 ÷ Futures DV01 = $3,630 ÷ $95 ≈ 38 contracts</code>
            If rates rise 10 bps: Bond loses $36,300 but futures gain ~$38 × $950 = $36,100 — near perfect hedge.
            {note_box("The hedge isn't perfect because corporate spreads can move independently of Treasury yields (basis risk).")}""", 2)

        qa_block("What is the difference between interest rate risk and credit risk?",
            f"""These are the two main risk dimensions in corporate bonds:<br><br>
            <strong>{highlight("Interest Rate Risk:")}</strong><br>
            Risk from changes in the overall level of interest rates (driven by central bank policy, inflation expectations).
            Affects ALL bonds — government and corporate. Measured by Duration/DV01.
            Can be hedged using Treasury futures or interest rate swaps.<br><br>
            <strong>{highlight("Credit (Spread) Risk:")}</strong><br>
            Risk from changes in the issuer's creditworthiness or market risk appetite.
            Affects the SPREAD component of the yield. Examples: downgrade from BBB to BB (spread jump from 170 to 350 bps),
            default (bond price collapses to recovery value ~40 cents).<br>
            Harder to hedge — use CDS (credit default swaps) or reduce position.<br><br>
            <strong>Combined yield risk:</strong> YTM = Benchmark rate + Credit spread<br>
            Both components can move, and they often move together in stress events (rates fall + spreads widen, or 'flight to quality').
            {note_box("In 2008 financial crisis: Treasuries rallied (rates fell) while corporate spreads exploded (IG from 150 to 500+ bps, HY from 400 to 2,000+ bps).")}""", 3)

    # ===========================================================================
    # TOPIC 13 — GLOSSARY
    # ===========================================================================
    elif topic == "13. Glossary & Quick Reference":
        section_header("📖 Topic 13: Glossary & Quick Reference", "Every bond market term explained in plain English")

        terms = [
            ("Basis Point (bp/bps)", "1/100th of a percentage point. 100 bps = 1.00%. The standard unit for spreads and small yield changes. A 25 bps rate cut = 0.25% rate cut."),
            ("Par", "$100 per $100 face value. A bond at par means price = 100. Above par = premium bond; below par = discount bond."),
            ("Coupon", "The annual interest rate printed on the bond, expressed as % of face value. A 6% coupon on $1,000 face = $60/year = $30 every 6 months."),
            ("YTM (Yield to Maturity)", "Total annualised return if the bond is held to maturity. Accounts for the coupon stream, price premium/discount, and time value of money. THE key pricing metric."),
            ("Spread", "The difference in yield between a corporate bond and a risk-free benchmark (Treasuries/G-Secs). Measures credit and liquidity risk premium."),
            ("NIP (New Issue Premium)", "Extra yield offered on a new bond vs. secondary market bonds. Compensates investors for buying something unproven and initially illiquid."),
            ("Bookbuilding", "The process of collecting investor orders to discover price and size. IPT → Guidance → Reoffer."),
            ("IPT (Initial Price Thoughts)", "First spread indication sent to investors. Intentionally set wide (high yield) to attract orders and anchor the negotiation."),
            ("Guidance", "Updated spread indication after initial orders. Tightening guidance signals strong demand."),
            ("Reoffer / Reoffer Price", "Final yield/spread/price at which bonds are sold to investors. The definitive pricing of the deal."),
            ("Tenor", "Remaining life of a bond from settlement to maturity. A 10-year bond has tenor = 10."),
            ("Macaulay Duration", "Weighted average time to receive a bond's cash flows. A 10-year bond has Macaulay duration ~7–8 years due to interim coupon payments."),
            ("Modified Duration", "Percentage price change per 100 bps yield change. Mod Duration = Mac Duration ÷ (1 + YTM/freq)."),
            ("DV01 (Dollar Value of 01)", "Dollar change in bond value per 1 basis point yield change. The universal risk measure for fixed income trading."),
            ("Convexity", "Second-order measure of price sensitivity — the curvature of the price-yield curve. Positive convexity benefits investors."),
            ("Investment Grade (IG)", "Bonds rated Baa3/BBB- or higher by at least two agencies. Lower default risk, lower yields, accessible to most institutional investors."),
            ("High Yield (HY) / Junk", "Bonds rated Ba1/BB+ or lower. Higher default risk, much higher yields (300–800+ bps over Treasuries), more volatile."),
            ("Syndicate", "The group of investment banks working together to underwrite and distribute a new bond issue."),
            ("Bookrunner / Lead Manager", "The lead bank(s) responsible for structuring, pricing, and running the bookbuilding process."),
            ("Oversubscription", "When total investor demand exceeds the deal size. 3.5× means $3.50 of demand for every $1 of supply. Enables spread tightening."),
            ("Clean Price", "Bond price excluding accrued interest. What you see quoted on Bloomberg and other trading systems."),
            ("Dirty Price", "Clean Price + Accrued Interest = what the buyer actually pays. For new issues with no accrued, Dirty = Clean."),
            ("Day Count (30/360)", "Convention for calculating accrued interest. Assumes 30-day months and 360-day years. Standard for US corporate bonds."),
            ("T+2 Settlement", "Cash and bonds transfer 2 business days after the trade date. Standard settlement cycle for investment-grade bonds."),
            ("Gross Spread", "Total underwriting fee = Management fee + Underwriting fee + Selling concession."),
            ("All-In Cost", "True borrowing cost for the issuer = YTM + (annual fee). Use as pre-tax Kd in WACC calculations."),
            ("SOFR", "Secured Overnight Financing Rate. Benchmark for floating-rate USD bonds, replaced LIBOR in 2023."),
            ("Greenshoe", "Over-allotment option allowing the issuer to sell extra bonds (typically 10–15% more) if demand is strong."),
            ("CDS (Credit Default Swap)", "A derivative contract that provides insurance against bond default. Used to hedge credit risk."),
        ]

        # Display in two columns
        col1, col2 = st.columns(2)
        for i, (term, definition) in enumerate(terms):
            with (col1 if i % 2 == 0 else col2):
                st.html(f"""
                <div style="background:{CARD_BG}; border:1px solid {MID_BLUE}44; border-left:3px solid {GOLD};
                  border-radius:8px; padding:12px 14px; margin-bottom:10px; user-select:none;">
                  <div style="color:{GOLD}; font-size:0.8rem; font-weight:800; margin-bottom:5px;
                    -webkit-text-fill-color:{GOLD};">{term}</div>
                  <div style="color:{TXT}; font-size:0.78rem; line-height:1.6;
                    -webkit-text-fill-color:{TXT};">{definition}</div>
                </div>
                """)

        # Quick formula card
        st.html(f"""
        <div style="background:linear-gradient(135deg,{DARK_BLUE},{MID_BLUE}); border:1px solid {GOLD}66;
          border-radius:12px; padding:16px 20px; margin-top:10px; user-select:none;">
          <div style="color:{GOLD}; font-weight:800; font-size:0.9rem; margin-bottom:12px;">⚡ Quick Formula Reference</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.79rem;">
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">YTM</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= Benchmark Yield + Total Spread</code>
            </div>
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">Coupon Rate</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= ROUND(YTM×8, 0) / 8 / 100 × 100</code>
            </div>
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">Re-Offer Price</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= PRICE(Set, Mat, Cpn, YTM, 100, 2, 0)</code>
            </div>
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">Gross Proceeds</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= Notional × (Dirty Price / 100)</code>
            </div>
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">Modified Duration</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= MacDuration / (1 + YTM/freq)</code>
            </div>
            <div style="background:#0d1f3c; border-radius:8px; padding:10px 12px;">
              <div style="color:{LT_BLUE}; font-weight:700; margin-bottom:4px;">All-In Cost</div>
              <code style="color:{GOLD}; -webkit-text-fill-color:{GOLD};">= YTM + (Total Fee Rate / Tenor)</code>
            </div>
          </div>
        </div>
        """)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.html(f"""
<div style="
  background: linear-gradient(135deg,{DARK_BLUE},{MID_BLUE});
  border: 1px solid {GOLD}44;
  border-radius: 12px;
  padding: 16px 24px;
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  user-select: none;
">
  <div>
    <div style="color:{GOLD}; font-weight:800; font-size:0.9rem;">THE MOUNTAIN PATH — WORLD OF FINANCE</div>
    <div style="color:{MUTED}; font-size:0.75rem; margin-top:3px;">
      Prof. V. Ravichandran &nbsp;|&nbsp; 28+ Years Corporate Finance &amp; Banking &nbsp;|&nbsp;
      Fixed Income Securities &amp; Analysis
    </div>
    <div style="color:{MUTED}; font-size:0.72rem; margin-top:2px;">
      NMIMS Bangalore &nbsp;·&nbsp; BITS Pilani WILP &nbsp;·&nbsp; RV University Bangalore &nbsp;·&nbsp; Goa Institute of Management
    </div>
  </div>
  <div style="text-align:right;">
    <a href="https://themountainpathacademy.com" target="_blank"
       style="color:{GOLD}; font-weight:700; font-size:0.82rem; text-decoration:none; display:block;">
      🌐 themountainpathacademy.com
    </a>
    <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
       style="color:{LT_BLUE}; font-size:0.78rem; text-decoration:none; margin-right:12px;">
      💼 LinkedIn
    </a>
    <a href="https://github.com/trichyravis" target="_blank"
       style="color:{LT_BLUE}; font-size:0.78rem; text-decoration:none;">
      🐙 GitHub
    </a>
  </div>
</div>
""")

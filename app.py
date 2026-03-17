
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
  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {{
    background: #0d1f3c;
    border-radius: 8px;
    gap: 4px;
    padding: 4px;
  }}
  .stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: #c8d6f0 !important;
    -webkit-text-fill-color: #c8d6f0 !important;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.85rem;
    opacity: 1 !important;
  }}
  .stTabs [data-baseweb="tab"] p,
  .stTabs [data-baseweb="tab"] span,
  .stTabs [data-baseweb="tab"] div {{
    color: #c8d6f0 !important;
    -webkit-text-fill-color: #c8d6f0 !important;
    opacity: 1 !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: {DARK_BLUE} !important;
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
    border-bottom: 2px solid {GOLD} !important;
  }}
  .stTabs [aria-selected="true"] p,
  .stTabs [aria-selected="true"] span,
  .stTabs [aria-selected="true"] div {{
    color: {GOLD} !important;
    -webkit-text-fill-color: {GOLD} !important;
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📌 Pricing Summary",
    "📈 Spread Buildup",
    "💰 Fees & Proceeds",
    "🔍 Comps Analysis",
    "📊 Sensitivity",
    "📐 Risk Metrics"
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

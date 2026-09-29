import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Paytm / UPI MDR Analytics", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

# ---------- Theme ----------
st.markdown("""
<style>
.stApp {background: #f4f7fb;}
.block-container {padding-top: 1rem; padding-bottom: 2rem; max-width: 1450px;}
.hero {padding: 28px 32px; border-radius: 22px; background: linear-gradient(135deg,#081f4d 0%,#075985 52%,#06b6d4 100%); color:white; box-shadow:0 12px 35px rgba(8,31,77,.20); margin-bottom:18px;}
.hero h1 {font-size:38px; margin:0; font-weight:800;}
.hero p {font-size:16px; margin:8px 0 0; opacity:.92;}
.badge {display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(255,255,255,.16); font-size:12px; font-weight:700; margin-bottom:10px;}
.section {font-size:25px; font-weight:800; color:#102a43; margin-top:18px;}
.explain {background:#fff; border:1px solid #e4eaf2; border-radius:16px; padding:14px 17px; margin:7px 0 15px; color:#52606d; font-size:14px; line-height:1.55;}
.rule {background:linear-gradient(135deg,#eff6ff,#ecfeff); border:1px solid #bae6fd; border-left:5px solid #0891b2; border-radius:16px; padding:18px 20px; line-height:1.7;}
.metric-note {font-size:12px;color:#6b7280;margin-top:-10px;margin-bottom:12px;}
.source {background:#fff; border:1px solid #dbe5ef; border-radius:14px; padding:15px;}
div[data-testid="stMetric"] {background:white; border:1px solid #e2e8f0; padding:15px 18px; border-radius:16px; box-shadow:0 4px 14px rgba(15,23,42,.05);}
div[data-testid="stSidebar"] {background:#eef5fb;}
.smallcaps {font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:#64748b; font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="badge">INTERACTIVE DATA DASHBOARD</div>
  <h1>💳 Paytm / UPI Merchant MDR Analytics</h1>
  <p>Explore transaction value, the ₹2,000 threshold, estimated MDR, categories and monthly trends.</p>
</div>
""", unsafe_allow_html=True)

st.info("**Important:** 0.4% here refers to the specified Merchant Discount Rate (MDR) framework, not a government tax. The calculation below is an analytical estimate.")

# ---------- Sidebar ----------
st.sidebar.markdown("## ⚙️ Dashboard Controls")
uploaded_file = st.sidebar.file_uploader("Upload your transaction CSV", type=["csv"], help="Your file should contain a Date and Amount column.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")
else:
    df = pd.DataFrame({
        "Transaction_ID":[f"TXN{i:04d}" for i in range(1,11)],
        "Date":pd.date_range("2026-01-01", periods=10),
        "Category":["Grocery","Restaurant","Retail","Fuel","Telecom","Travel","Insurance","Grocery","Retail","Restaurant"],
        "Amount":[1500,2500,5000,12000,2100,75000,3000,1800,90000,3500],
        "Payment_App":["Paytm"]*10,
        "Type":["P2M"]*10
    })
    st.sidebar.caption("Using the built-in sample dataset. Upload your CSV above for your own analysis.")

df.columns=[str(c).strip() for c in df.columns]
date_candidates=[c for c in df.columns if c.lower() in ["date","transaction_date","transaction date","txn_date"]]
amount_candidates=[c for c in df.columns if c.lower() in ["amount","transaction_amount","transaction amount","sales","value"]]
if not date_candidates:
    st.error("Could not find a Date column. Rename it to **Date**."); st.stop()
if not amount_candidates:
    st.error("Could not find an Amount column. Rename it to **Amount**."); st.stop()
date_col, amount_col = date_candidates[0], amount_candidates[0]
df[date_col]=pd.to_datetime(df[date_col], errors="coerce")
df[amount_col]=pd.to_numeric(df[amount_col].astype(str).str.replace(",","",regex=False).str.replace("₹","",regex=False), errors="coerce")
df=df.dropna(subset=[date_col,amount_col]).copy()

# ---------- Filters ----------
st.sidebar.markdown("### 🔎 Filters")
min_date,max_date=df[date_col].min().date(),df[date_col].max().date()
date_range=st.sidebar.date_input("Date range", value=(min_date,max_date), min_value=min_date, max_value=max_date)
filtered=df.copy()
if isinstance(date_range,tuple) and len(date_range)==2:
    filtered=filtered[(filtered[date_col].dt.date>=date_range[0])&(filtered[date_col].dt.date<=date_range[1])]
if "Category" in filtered.columns:
    cats=sorted(filtered["Category"].dropna().astype(str).unique())
    selected=st.sidebar.multiselect("Categories", cats, default=cats)
    filtered=filtered[filtered["Category"].astype(str).isin(selected)]
if "Payment_App" in filtered.columns:
    apps=sorted(filtered["Payment_App"].dropna().astype(str).unique())
    selected_apps=st.sidebar.multiselect("Payment app", apps, default=apps)
    filtered=filtered[filtered["Payment_App"].astype(str).isin(selected_apps)]
if "Type" in filtered.columns:
    types=sorted(filtered["Type"].dropna().astype(str).unique())
    selected_types=st.sidebar.multiselect("Transaction type", types, default=types)
    filtered=filtered[filtered["Type"].astype(str).isin(selected_types)]

if filtered.empty:
    st.warning("No transactions match the selected filters. Please widen the filters."); st.stop()

# ---------- MDR ----------
filtered=filtered.copy()
filtered["Eligible_0.4_MDR"]=filtered[amount_col]>2000
filtered["MDR_0.4"]=np.where(filtered["Eligible_0.4_MDR"], np.minimum(filtered[amount_col]*0.004,300),0)

total_value=filtered[amount_col].sum(); transaction_count=len(filtered); eligible_count=int(filtered["Eligible_0.4_MDR"].sum()); estimated_mdr=filtered["MDR_0.4"].sum()
eligible_share=eligible_count/transaction_count*100

# ---------- KPIs ----------
st.markdown('<div class="smallcaps">Overview</div>', unsafe_allow_html=True)
c1,c2,c3,c4=st.columns(4)
c1.metric("💰 Transaction Value",f"₹{total_value:,.0f}")
c2.metric("🧾 Transactions",f"{transaction_count:,}")
c3.metric("📌 Above ₹2,000",f"{eligible_count:,}",f"{eligible_share:.1f}% of filtered transactions")
c4.metric("📊 Estimated MDR",f"₹{estimated_mdr:,.0f}")

st.markdown("<div class='metric-note'>All KPI cards update automatically when you change the sidebar filters.</div>", unsafe_allow_html=True)

# ---------- Image / framework ----------
left,right=st.columns([1.15,1])
with left:
    st.markdown("### 📱 Merchant Payment Visual")
    st.image("https://img.theweek.in/content/dam/week/en/archive/news/biz-tech/images/2026/8/8/upi-payment-reuters.jpg?h=650&w=1248", caption="Illustrative UPI QR merchant-payment scene", use_container_width=True)
    st.caption("The image is illustrative; the dashboard calculations come from the uploaded/sample transaction data.")
with right:
    st.markdown("### 🏛️ MDR Framework")
    st.markdown("""
    <div class="rule">
    <b>0.4% MDR:</b> specified P2M merchant transactions above ₹2,000.<br>
    <b>₹2,000 or below:</b> remains free under the stated framework.<br>
    <b>₹75,000+:</b> the 0.4% category has a ₹300 per-transaction cap.<br>
    <b>Important:</b> MDR is not a government tax collected by the Government or NPCI.
    </div>
    """,unsafe_allow_html=True)
    st.markdown("**How to read this dashboard**")
    st.write("Use the filters to narrow the dataset. Every KPI, chart and table below recalculates from the filtered rows.")

# ---------- Charts ----------
st.markdown("<div class='section'>📈 Understand the Transactions</div>",unsafe_allow_html=True)

# Monthly
monthly=(filtered.assign(Month=filtered[date_col].dt.to_period("M").astype(str)).groupby("Month")[amount_col].sum().reset_index())
col1,col2=st.columns(2)
with col1:
    st.markdown("#### 1. Monthly transaction value")
    st.bar_chart(monthly.set_index("Month"), y=amount_col, use_container_width=True)
    st.markdown("<div class='explain'><b>What this chart tells you:</b> It compares the total money value of transactions in each month. A taller bar means more transaction value was processed during that month. Use it to spot high-activity and low-activity periods.</div>",unsafe_allow_html=True)
with col2:
    status=filtered["Eligible_0.4_MDR"].map({True:"Above ₹2,000",False:"₹2,000 or below"}).value_counts().reindex(["₹2,000 or below","Above ₹2,000"],fill_value=0)
    st.markdown("#### 2. Transactions by ₹2,000 threshold")
    st.bar_chart(status, use_container_width=True)
    st.markdown("<div class='explain'><b>What this chart tells you:</b> It counts transactions on either side of the ₹2,000 threshold. This helps you see how many filtered transactions fall into the group used by the dashboard's 0.4% MDR estimate.</div>",unsafe_allow_html=True)

if "Category" in filtered.columns:
    category_data=filtered.groupby("Category")[amount_col].sum().sort_values(ascending=False)
    st.markdown("#### 3. Transaction value by category")
    st.bar_chart(category_data,use_container_width=True)
    st.markdown("<div class='explain'><b>What this chart tells you:</b> Each bar represents the total transaction value for a merchant category. Longer bars indicate categories contributing more transaction value in the current filtered dataset. This is a value comparison, not a profitability ranking.</div>",unsafe_allow_html=True)

# MDR by month
mdr_month=(filtered.assign(Month=filtered[date_col].dt.to_period("M").astype(str)).groupby("Month")["MDR_0.4"].sum().reset_index())
st.markdown("#### 4. Estimated MDR by month")
st.line_chart(mdr_month.set_index("Month"), y="MDR_0.4", use_container_width=True)
st.markdown("<div class='explain'><b>What this chart tells you:</b> This line shows the dashboard's estimated MDR amount over time. Peaks mean the filtered transactions generated a higher estimated MDR amount under the calculation used here.</div>",unsafe_allow_html=True)

# ---------- Table ----------
st.markdown("<div class='section'>🧮 Transaction-Level Details</div>",unsafe_allow_html=True)
st.markdown("<div class='explain'><b>How to use the table:</b> Search, sort and inspect individual transactions. <b>Eligible_0.4_MDR = True</b> means the transaction is above ₹2,000. <b>MDR_0.4</b> shows the dashboard's estimated MDR for that row.</div>",unsafe_allow_html=True)

display_cols=[]
for col in ["Transaction_ID",date_col,"Category",amount_col,"Payment_App","Type"]:
    if col in filtered.columns and col not in display_cols: display_cols.append(col)
display_cols += ["Eligible_0.4_MDR","MDR_0.4"]
st.dataframe(filtered[display_cols].sort_values(date_col,ascending=False),use_container_width=True,hide_index=True)

# ---------- Formula ----------
with st.expander("📚 Show the MDR calculation"):
    st.write("For a transaction above ₹2,000 in the specified 0.4% category:")
    st.code("MDR = Transaction Amount × 0.004")
    st.write("Example: ₹10,000 × 0.004 = ₹40")
    st.write("For transactions of ₹75,000 or more, this dashboard applies the ₹300 cap described for the 0.4% category.")
    st.info("Special-sector rules can differ. Treat these figures as dashboard estimates, not a legal or accounting determination.")

# ---------- Sources ----------
st.markdown("<div class='section'>🏛️ Official References</div>",unsafe_allow_html=True)
st.markdown("""
<div class="source">
<b>Press Information Bureau, Ministry of Finance — 15 September 2026</b><br>
Government release describing the UPI merchant MDR framework and clarifying that MDR is not a government tax.<br><br>
<b>Department of Financial Services — Ministry of Finance</b><br>
FAQs on Merchant Discount Rate (MDR) on Select UPI (P2M) Transactions.
</div>
""",unsafe_allow_html=True)
st.markdown("[Open PIB government release](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2310586&lang=1&reg=3)")
st.markdown("[Open Department of Financial Services FAQ](https://financialservices.gov.in/faqs-merchant-discount-rate-mdr-select-upi-p2m-transactions)")
st.caption("Dashboard note: the 0.4% calculation is based on the government-described MDR framework and should not be described as a Paytm-specific tax.")

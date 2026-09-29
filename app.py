
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Paytm / UPI MDR Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS - attractive dashboard
# -----------------------------
st.markdown("""
<style>
.main {background: #f6f8fb;}
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.hero {
    padding: 24px 28px;
    border-radius: 18px;
    background: linear-gradient(135deg, #062b66, #00a8e8);
    color: white;
    margin-bottom: 20px;
}
.hero h1 {margin: 0; font-size: 36px;}
.hero p {margin: 8px 0 0; font-size: 16px;}
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 3px 15px rgba(0,0,0,.07);
}
.small {color:#667085; font-size:13px;}
.big {font-size:28px; font-weight:700; color:#062b66;}
.source {
    background:#eef7ff;
    padding:15px 18px;
    border-radius:12px;
    border-left:5px solid #00a8e8;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>💳 Paytm / UPI Merchant MDR Dashboard</h1>
    <p>Interactive analysis of transactions and the 0.4% Merchant Discount Rate (MDR)</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "Important: The 0.4% figure discussed here is MDR (Merchant Discount Rate), "
    "not a government tax. The government says MDR is a charge within the merchant "
    "payment ecosystem."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload transaction CSV",
    type=["csv"]
)

# Default sample data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.DataFrame({
        "Transaction_ID": [f"TXN{i:04d}" for i in range(1, 11)],
        "Date": pd.date_range("2026-01-01", periods=10),
        "Category": [
            "Grocery", "Restaurant", "Retail", "Fuel", "Telecom",
            "Travel", "Insurance", "Grocery", "Retail", "Restaurant"
        ],
        "Amount": [1500, 2500, 5000, 12000, 2100, 75000, 3000, 1800, 90000, 3500],
        "Payment_App": ["Paytm"] * 10,
        "Type": ["P2M"] * 10
    })

# -----------------------------
# Clean / detect columns
# -----------------------------
df.columns = [str(c).strip() for c in df.columns]

# Detect date column
date_candidates = [c for c in df.columns if c.lower() in
                   ["date", "transaction_date", "transaction date", "txn_date"]]

# Detect amount column
amount_candidates = [c for c in df.columns if c.lower() in
                     ["amount", "transaction_amount", "transaction amount", "sales", "value"]]

if not date_candidates:
    st.error("Could not find a Date column. Rename your date column to 'Date'.")
    st.stop()

if not amount_candidates:
    st.error("Could not find an Amount column. Rename your amount column to 'Amount'.")
    st.stop()

date_col = date_candidates[0]
amount_col = amount_candidates[0]

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df[amount_col] = pd.to_numeric(
    df[amount_col].astype(str).str.replace(",", "", regex=False).str.replace("₹", "", regex=False),
    errors="coerce"
)

df = df.dropna(subset=[date_col, amount_col]).copy()

# -----------------------------
# Filters
# -----------------------------
st.sidebar.subheader("🔎 Filters")

min_date = df[date_col].min().date()
max_date = df[date_col].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[
        (df[date_col].dt.date >= start_date) &
        (df[date_col].dt.date <= end_date)
    ].copy()
else:
    filtered = df.copy()

if "Category" in filtered.columns:
    categories = sorted(filtered["Category"].dropna().astype(str).unique())
    selected_categories = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories
    )
    filtered = filtered[filtered["Category"].astype(str).isin(selected_categories)]

# -----------------------------
# MDR calculation
# -----------------------------
filtered["Eligible_0.4_MDR"] = filtered[amount_col] > 2000
filtered["MDR_0.4"] = np.where(
    filtered["Eligible_0.4_MDR"],
    np.minimum(filtered[amount_col] * 0.004, 300),
    0
)

# NOTE:
# This is a dashboard calculation based on the government rule.
# Special sectors may have different treatment, so this should not be
# interpreted as a final legal/accounting calculation for every transaction.

total_value = filtered[amount_col].sum()
transaction_count = len(filtered)
eligible_count = int(filtered["Eligible_0.4_MDR"].sum())
estimated_mdr = filtered["MDR_0.4"].sum()

# -----------------------------
# KPI cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Transaction Value", f"₹{total_value:,.0f}")
c2.metric("🧾 Transactions", f"{transaction_count:,}")
c3.metric("📌 > ₹2,000 Transactions", f"{eligible_count:,}")
c4.metric("📊 Estimated 0.4% MDR", f"₹{estimated_mdr:,.0f}")

st.markdown("---")

# -----------------------------
# Image + government rule
# -----------------------------
left, right = st.columns([1.2, 1])

with left:
    st.subheader("📱 Digital Merchant Payments")
    st.image(
        "https://img.theweek.in/content/dam/week/en/archive/news/biz-tech/images/2026/8/8/upi-payment-reuters.jpg?h=650&w=1248",
        caption="Paytm QR / UPI merchant payment example",
        use_container_width=True
    )

with right:
    st.subheader("🏛️ Government MDR Framework")
    st.markdown("""
    <div class="source">
    <b>0.4% MDR:</b> specified P2M merchant transactions above ₹2,000.<br><br>
    <b>Up to ₹2,000:</b> remains free under the stated framework.<br><br>
    <b>₹75,000 and above:</b> MDR capped at ₹300 per transaction under the
    stated 0.4% category.<br><br>
    <b>Important:</b> MDR is not a government tax collected by the Government or NPCI.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Transaction Analysis")

col1, col2 = st.columns(2)

with col1:
    monthly = (
        filtered.assign(Month=filtered[date_col].dt.to_period("M").astype(str))
        .groupby("Month")[amount_col]
        .sum()
        .reset_index()
    )
    st.bar_chart(monthly.set_index("Month"), y=amount_col, use_container_width=True)
    st.caption("Monthly transaction value")

with col2:
    status = (
        filtered["Eligible_0.4_MDR"]
        .map({True: "Above ₹2,000", False: "₹2,000 or below"})
        .value_counts()
    )
    st.bar_chart(status, use_container_width=True)
    st.caption("Transaction count by ₹2,000 threshold")

# Category chart
if "Category" in filtered.columns:
    st.subheader("🛍️ Transaction Value by Category")
    category_data = (
        filtered.groupby("Category")[amount_col]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_data, use_container_width=True)

# -----------------------------
# MDR table
# -----------------------------
st.subheader("🧮 MDR Calculation Details")

display_cols = []
for col in ["Transaction_ID", date_col, "Category", amount_col, "Payment_App", "Type"]:
    if col in filtered.columns and col not in display_cols:
        display_cols.append(col)

display_cols += ["Eligible_0.4_MDR", "MDR_0.4"]

st.dataframe(
    filtered[display_cols].sort_values(date_col, ascending=False),
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Explanation
# -----------------------------
with st.expander("📚 How the 0.4% MDR calculation works"):
    st.write("For a transaction above ₹2,000 in the specified 0.4% category:")
    st.code("MDR = Transaction Amount × 0.004")
    st.write("Example:")
    st.code("₹10,000 × 0.004 = ₹40")
    st.write(
        "For transactions of ₹75,000 or more, this dashboard applies the "
        "₹300 cap described by the government for the 0.4% category."
    )
    st.info(
        "The dataset may contain transactions from different merchant sectors. "
        "Special-sector rules can differ, so the calculation is an analytical "
        "estimate rather than a legal/accounting determination."
    )

# -----------------------------
# Government source
# -----------------------------
st.subheader("🏛️ Official Government Sources")

st.markdown("""
- **Press Information Bureau (Ministry of Finance), 15 September 2026**  
  UPI MDR framework and clarification that MDR is not a government tax.

- **Department of Financial Services, Ministry of Finance**  
  FAQs on Merchant Discount Rate (MDR) on Select UPI (P2M) Transactions.
""")

st.markdown(
    "[Open PIB government release](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2310586&lang=1&reg=3)"
)
st.markdown(
    "[Open Department of Financial Services FAQ](https://financialservices.gov.in/faqs-merchant-discount-rate-mdr-select-upi-p2m-transactions)"
)

st.caption(
    "Dashboard note: The 0.4% calculation is based on the government-described "
    "MDR framework. It should not be described as a Paytm-specific tax."
)

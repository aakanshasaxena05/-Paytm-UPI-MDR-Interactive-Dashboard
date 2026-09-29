# 💳 Paytm / UPI Merchant MDR Analytics Dashboard

An interactive **Streamlit data analytics dashboard** for exploring UPI merchant transactions, transaction values, the ₹2,000 threshold, estimated Merchant Discount Rate (MDR), merchant categories, and monthly transaction trends.

The dashboard allows users to upload their own transaction CSV file and dynamically analyze the data using interactive filters and visualizations.

---

## 📊 Dashboard Preview

The dashboard provides a clean and interactive interface with:

* 💰 Transaction value analysis
* 🧾 Transaction count
* 📌 ₹2,000 threshold analysis
* 📊 Estimated MDR
* 📅 Monthly transaction trends
* 🏪 Category-wise transaction analysis
* 💳 Payment app filtering
* 🔎 Transaction-type filtering
* 🧮 Transaction-level MDR calculations
* 📋 Detailed transaction table

---

## 🚀 Features

### 1. Interactive Dashboard

The dashboard is built using **Streamlit** and provides an easy-to-use interface for analyzing merchant payment transactions.

### 2. CSV File Upload

Users can upload their own transaction CSV file directly through the sidebar.

The application automatically looks for:

* `Date`
* `Amount`

It also supports common alternative column names such as `Transaction_Date`, `Transaction_Amount`, `Sales`, and `Value`.

### 3. Dashboard Filters

Users can filter the data by:

* 📅 Date range
* 🏪 Category
* 💳 Payment App
* 🔄 Transaction Type

All KPI cards, charts, and tables update automatically according to the selected filters.

### 4. KPI Cards

The dashboard displays four important metrics:

| KPI                  | Description                                          |
| -------------------- | ---------------------------------------------------- |
| 💰 Transaction Value | Total value of filtered transactions                 |
| 🧾 Transactions      | Total number of filtered transactions                |
| 📌 Above ₹2,000      | Number and percentage of transactions above ₹2,000   |
| 📊 Estimated MDR     | Estimated MDR calculated using the dashboard formula |

### 5. MDR Analysis

The dashboard identifies transactions above the ₹2,000 threshold and calculates estimated MDR using:

```text
MDR = Transaction Amount × 0.004
```

For example:

```text
₹10,000 × 0.004 = ₹40
```

The dashboard also applies a ₹300 cap for transactions of ₹75,000 or more within the specified 0.4% category.

> **Note:** The MDR calculation is an analytical estimate based on the framework represented in the dashboard. It should not be treated as legal, tax, or accounting advice.

### 6. Data Visualizations

The dashboard includes:

#### 📈 Monthly Transaction Value

Shows the total transaction value for each month.

#### 📊 ₹2,000 Threshold Analysis

Compares transactions:

* ₹2,000 or below
* Above ₹2,000

#### 🏪 Category-wise Transaction Value

Shows which merchant categories contribute the most transaction value.

#### 📉 Estimated MDR by Month

Displays estimated MDR amounts across months.

### 7. Transaction-Level Analysis

The dashboard provides a detailed table containing information such as:

* Transaction ID
* Date
* Category
* Amount
* Payment App
* Transaction Type
* MDR eligibility
* Estimated MDR

Users can sort and inspect individual transactions.

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Data Analysis**
* **Data Visualization**
* **HTML/CSS styling**

---

## 📂 Project Structure

```text
Paytm-UPI-MDR-Analytics/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/Paytm-UPI-MDR-Analytics.git
```

### Step 2 — Open the project folder

```bash
cd Paytm-UPI-MDR-Analytics
```

### Step 3 — Install required libraries

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Streamlit application

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

## 📦 Requirements

Create a `requirements.txt` file containing:

```text
streamlit
pandas
numpy
```

---

## 📄 Input CSV Format

You can upload your own transaction CSV file.

A recommended structure is:

| Transaction_ID | Date       | Category   | Amount | Payment_App | Type |
| -------------- | ---------- | ---------- | -----: | ----------- | ---- |
| TXN0001        | 2026-01-01 | Grocery    |   1500 | Paytm       | P2M  |
| TXN0002        | 2026-01-02 | Restaurant |   2500 | Paytm       | P2M  |
| TXN0003        | 2026-01-03 | Retail     |   5000 | Paytm       | P2M  |

### Required columns

```text
Date
Amount
```

### Optional columns

```text
Transaction_ID
Category
Payment_App
Type
```

---

## 📌 Sample Dataset

If no CSV file is uploaded, the dashboard automatically uses a built-in sample dataset containing transaction information for demonstration.

This allows the dashboard to run immediately without requiring an external dataset.

---

## 🧮 MDR Calculation Logic

The application creates an eligibility field:

```python
filtered["Eligible_0.4_MDR"] = filtered[amount_col] > 2000
```

The estimated MDR is calculated as:

```python
filtered["MDR_0.4"] = np.where(
    filtered[amount_col] > 2000,
    np.minimum(filtered[amount_col] * 0.004, 300),
    0
)
```

Therefore:

```text
Amount ≤ ₹2,000
        ↓
Estimated MDR = ₹0

Amount > ₹2,000
        ↓
MDR = Amount × 0.004
        ↓
Maximum = ₹300 per transaction
```

---

## 🎯 Project Objective

The objective of this project is to demonstrate how **Python, Pandas, NumPy, and Streamlit** can be used to build an interactive financial/data analytics dashboard.

The project focuses on:

* Data cleaning
* Data filtering
* KPI calculation
* Business-rule implementation
* Transaction analysis
* Data visualization
* Interactive dashboard development

---

## 📚 Key Data Analytics Concepts Demonstrated

This project demonstrates practical knowledge of:

* Data ingestion
* CSV handling
* Data cleaning
* Date conversion
* Numeric conversion
* Filtering
* GroupBy operations
* Aggregation
* Conditional calculations
* KPI development
* Time-series analysis
* Data visualization
* Interactive dashboards

---

## 🏛️ References

The application includes references to:

* **Press Information Bureau — Ministry of Finance**
* **Department of Financial Services — Ministry of Finance**
* Merchant Discount Rate (MDR) information for selected UPI P2M transactions

The dashboard itself also clearly notes that the 0.4% calculation is an analytical estimate and should not be described as a Paytm-specific tax.

---

## ⚠️ Disclaimer

This project is intended for **educational and data-analysis purposes**.

The MDR values displayed by the dashboard are estimates calculated according to the rules implemented in the application. They should not be considered legal, tax, accounting, or payment-settlement advice.

---

## 👩‍💻 Author

**Aakansha Saxena**



## ⭐ Future Improvements

* Add downloadable filtered reports
* Add more payment applications
* Add advanced Plotly visualizations
* Add automated database connectivity
* Add real-time transaction analytics
* Add authentication
* Add deployment on Streamlit Cloud
* Add advanced financial KPIs
* Add monthly/yearly comparison
* Add Excel export functionality

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ **Star** on GitHub!

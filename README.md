# -Paytm-UPI-MDR-Interactive-Dashboard
# 💳 Paytm / UPI MDR Interactive Dashboard

## 📌 Project Overview

This project is an **interactive data analysis dashboard built using Python and Streamlit** to analyze UPI merchant transactions and estimate the **0.4% Merchant Discount Rate (MDR)** for eligible transactions.

The dashboard allows users to upload their own transaction CSV file and interactively explore transaction amounts, categories, dates, payment applications, and estimated MDR.

> **Important:** The 0.4% discussed in this dashboard represents **Merchant Discount Rate (MDR), not a government tax**. The dashboard is intended for data analysis and visualization and should not be treated as a legal or accounting calculation.

## 🎯 Objectives

* Analyze UPI/P2M transaction data.
* Calculate estimated MDR for eligible transactions.
* Identify transactions above the ₹2,000 threshold.
* Analyze transaction trends over time.
* Compare transaction values across categories.
* Provide an interactive dashboard for exploring transaction data.
* Allow users to upload and analyze their own CSV files.

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data cleaning and manipulation
* **NumPy** – Numerical calculations
* **Streamlit** – Interactive dashboard development
* **Matplotlib / Plotting Libraries** – Data visualization
* **CSV** – Transaction data source

## 📊 Dashboard Features

### 1. 📁 CSV File Upload

Users can upload their own transaction CSV file directly from the Streamlit sidebar.

The dashboard reads the uploaded data and automatically processes important columns such as:

* Date
* Transaction Amount
* Category
* Payment App
* Transaction Type

### 2. 🎛️ Interactive Filters

The dashboard provides filters that allow users to dynamically explore the data.

Users can filter by:

* Date range
* Transaction category
* Payment application
* Transaction type

All dashboard KPIs and charts update according to the selected filters.

### 3. 💰 KPI Cards

The dashboard displays important summary information such as:

* Total Transaction Value
* Number of Transactions
* Transactions Above ₹2,000
* Estimated MDR

These KPIs provide a quick overview of the selected dataset.

### 4. 📈 Monthly Transaction Trend

This chart displays transaction value over time.

**What it tells us:**
It helps identify months with higher or lower transaction activity and makes it easier to understand the overall transaction trend.

### 5. 📊 Category Analysis

The category chart compares transaction values across different categories such as:

* Grocery
* Restaurant
* Retail
* Fuel
* Telecom
* Travel
* Insurance

**What it tells us:**
It shows which transaction categories contribute more to the total transaction value.

### 6. 📉 MDR Trend

The MDR chart shows the estimated MDR amount over time.

**What it tells us:**
It helps users understand how the estimated MDR changes as transaction activity changes.

### 7. 🔎 Transaction-Level Analysis

The dashboard also displays the filtered transaction records in a table.

Additional calculated columns include:

* Eligible for 0.4% MDR
* Estimated MDR

This makes it possible to inspect individual transactions.

## 🧮 MDR Calculation

For an eligible transaction, the dashboard uses:

```text
Estimated MDR = Transaction Amount × 0.004
```

### Example

If the transaction amount is:

```text
₹10,000
```

Then:

```text
₹10,000 × 0.004 = ₹40
```

Therefore, the estimated MDR is:

```text
₹40
```

The dashboard also incorporates the ₹300 cap for transactions covered by the applicable 0.4% MDR framework.

## 📂 Project Structure

```text
Paytm-UPI-MDR-Dashboard/
│
├── app.py
│
├── paytm_mdr_sample.csv
│
└── README.md
```

### `app.py`

Main Streamlit application containing:

* Dashboard layout
* CSV upload
* Data cleaning
* Interactive filters
* MDR calculation
* KPI cards
* Charts
* Transaction table

### `paytm_mdr_sample.csv`

Sample transaction dataset that can be uploaded to test the dashboard.

## ▶️ How to Run the Project

### Step 1: Install Required Libraries

Open Command Prompt or PowerShell:

```bash
pip install streamlit pandas numpy
```

If your project uses additional visualization libraries, install them as required.

### Step 2: Open the Project Folder

For example:

```bash
cd "C:\Users\Lenovo\OneDrive\Desktop\python\streamlit"
```

### Step 3: Run the Streamlit Application

```bash
streamlit run app.py
```

### Step 4: Open the Dashboard

Streamlit will provide a local address such as:

```text
http://localhost:8501
```

Open this address in your browser.

## 📤 How to Use the Dashboard

1. Run `streamlit run app.py`.
2. Open the dashboard in your browser.
3. Upload your transaction CSV from the sidebar.
4. Select the required date range.
5. Select categories or transaction types.
6. Explore the KPI cards.
7. Analyze the charts.
8. View the filtered transaction table.

## 📋 Expected CSV Format

Your CSV should contain transaction-related information such as:

| Column         | Example    |
| -------------- | ---------- |
| Transaction_ID | TXN001     |
| Date           | 2026-09-01 |
| Category       | Grocery    |
| Amount         | 5000       |
| Payment_App    | Paytm      |
| Type           | P2M        |

The application also contains column-detection logic for commonly used column names.

## ⚠️ Important Note

This dashboard is created for **educational, analytical, and visualization purposes**.

The MDR calculation shown is an **estimated analytical calculation** based on the selected transaction data. Actual applicability can depend on the transaction category, payment rules, and applicable regulations.

The dashboard should therefore not be used as a legal, tax, or accounting determination.

## 📚 Data Source

The government information used to explain the MDR framework is based on official Government of India information regarding UPI merchant transactions and Merchant Discount Rate.

## 🚀 Future Improvements

Possible improvements include:

* 📌 Paytm-specific transaction categorization
* 📅 More advanced time-series analysis
* 📊 Additional dashboard visualizations
* 📥 Export filtered data to Excel/CSV
* 📈 Interactive Plotly charts
* 🔐 User authentication
* ☁️ Deployment on Streamlit Community Cloud
* 🗄️ Database integration
* 📱 Improved mobile responsiveness

## 👩‍💻 Author

**Aakansha Saxena**

### Skills Demonstrated

`Python` • `Pandas` • `NumPy` • `Streamlit` • `Data Cleaning` • `EDA` • `Data Visualization` • `Dashboard Development` • `Interactive Analytics`

---

⭐ If you find this project useful, consider giving the repository a star!

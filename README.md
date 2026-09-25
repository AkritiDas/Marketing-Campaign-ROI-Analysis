# 📊 Marketing Campaign ROI Analysis

An end-to-end, portfolio-grade **Business Analytics & Data Analytics** project analyzing marketing campaign performance across multiple digital marketing channels.

Built with **Python and Excel**, this project demonstrates data cleaning, KPI calculation, channel and campaign performance analysis, monthly trend analysis, data visualization, automated business insight generation, interactive Excel dashboards, and executive reporting.

---

## 🎯 Project Objective

The objective of this analysis is to evaluate marketing campaign performance across multiple channels, measure customer acquisition efficiency, analyze Return on Ad Spend (ROAS) and Return on Investment (ROI), identify performance differences across campaigns, and generate data-driven insights for marketing performance evaluation and budget optimization.

---

## 💼 Business Problem

Marketing organizations often struggle with fragmented performance metrics across different channels and campaigns.

This project addresses the following business questions:

1. Which marketing channels generate the highest revenue?

2. Which channels have the highest advertising costs?

3. Which channels provide better Return on Ad Spend (ROAS)?

4. Which channels have lower Customer Acquisition Cost (CAC)?

5. Which campaigns have strong conversion performance?

6. Which channels show relatively lower marketing efficiency?

7. How do marketing performance metrics change over time?

8. How can marketing data be transformed into actionable business insights?

---

## 📁 Dataset Description

The analysis uses a dataset containing **3,000 marketing campaign records** spanning 2025 across **8 marketing channels** and **16 unique campaigns**.

### Dataset Columns

| Column                | Description                                                                                                    |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Campaign_ID**       | Unique identifier for each campaign, e.g. `CMP_GGL_01`                                                         |
| **Campaign_Name**     | Descriptive campaign name, e.g. `Google_Search_Brand`                                                          |
| **Date**              | Campaign execution date in `YYYY-MM-DD` format                                                                 |
| **Marketing_Channel** | Marketing channel used for the campaign                                                                        |
| **Campaign_Type**     | Strategic campaign objective such as Awareness, Lead Generation, Conversion, Retargeting, or Product Promotion |
| **Region**            | Geographical territory                                                                                         |
| **Impressions**       | Total number of ad views                                                                                       |
| **Clicks**            | Number of user clicks                                                                                          |
| **Leads**             | Qualified potential leads                                                                                      |
| **Conversions**       | Completed conversion or purchase events                                                                        |
| **Ad_Spend ($)**      | Advertising expenditure                                                                                        |
| **Revenue ($)**       | Revenue generated from campaigns                                                                               |
| **Customers**         | Number of new paying customers acquired                                                                        |
| **Campaign_Duration** | Campaign duration in days                                                                                      |
| **Device_Type**       | Target device such as Desktop, Mobile, or Tablet                                                               |

### Marketing Channels

The dataset contains the following channels:

* Google Ads
* Facebook Ads
* Instagram Ads
* LinkedIn Ads
* YouTube Ads
* Email Marketing
* SEO
* Display Ads

---

## 🛠️ Tools & Technologies

* **Python 3.12** — Core programming and analytical language
* **Pandas** — Data cleaning, manipulation, aggregation, and analysis
* **NumPy** — Numerical calculations and vectorized operations
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical and analytical visualizations
* **OpenPyXL** — Excel workbook generation, formatting, formulas, and dashboards
* **ReportLab** — PDF executive report generation
* **Jupyter Notebook** — Interactive analytical walkthrough
* **Microsoft Excel** — Business analysis, spreadsheet modeling, dashboards, and reporting
* **Git & GitHub** — Version control and project repository management

---

## 🧹 Data Cleaning Process

The raw dataset is stored in:

```text
data/raw_marketing_data.csv
```

The data cleaning process is implemented using:

```text
python/data_cleaning.py
```

The major data preparation steps include:

### 1. Duplicate Removal

Duplicate records were identified and removed from the raw dataset.

### 2. Text Standardization

Marketing channel values were standardized by normalizing casing and removing unnecessary whitespace.

For example:

```text
"google ads "
"GOOGLE ADS"
"Google Ads"
```

were standardized to:

```text
"Google Ads"
```

### 3. Missing Value Imputation

Missing values were handled using appropriate statistical or business-based methods.

* **Device_Type** — Imputed using the mode
* **Campaign_Duration** — Imputed using the median
* **Leads** — Imputed using channel-specific click-to-lead conversion rates

### 4. Date Formatting

Mixed date formats were converted into a standard:

```text
YYYY-MM-DD
```

format.

### 5. Data Validation

Business and logical constraints were checked, including:

```text
Clicks <= Impressions
Conversions <= Clicks
Customers <= Conversions
```

Numeric columns were also converted to appropriate integer or floating-point data types.

The cleaned dataset is saved as:

```text
data/cleaned_marketing_data.csv
```

---

## 📊 KPI Definitions & Formulas

All metrics are calculated with **zero-division protection** to prevent calculation errors when the denominator is zero.

| Key Metric                          | Formula                                         | Business Purpose                                  |
| ----------------------------------- | ----------------------------------------------- | ------------------------------------------------- |
| **Click-Through Rate (CTR)**        | `CTR = (Clicks / Impressions) × 100`            | Measures ad creative engagement                   |
| **Conversion Rate (CR)**            | `CR = (Conversions / Clicks) × 100`             | Measures landing page and funnel effectiveness    |
| **Cost Per Click (CPC)**            | `CPC = Ad Spend / Clicks`                       | Measures media cost per click                     |
| **Cost Per Lead (CPL)**             | `CPL = Ad Spend / Leads`                        | Measures lead acquisition cost                    |
| **Customer Acquisition Cost (CAC)** | `CAC = Ad Spend / Customers`                    | Measures overall customer acquisition cost        |
| **Return on Ad Spend (ROAS)**       | `ROAS = Revenue / Ad Spend`                     | Measures revenue generated per advertising dollar |
| **Return on Investment (ROI)**      | `ROI = ((Revenue - Ad Spend) / Ad Spend) × 100` | Measures net return relative to advertising spend |

---

## 📈 Performance Analysis Summary

### Portfolio Totals

| Metric                       |             Value |
| ---------------------------- | ----------------: |
| **Total Ad Spend**           |   `$8,202,708.75` |
| **Total Revenue**            | `$129,938,821.72` |
| **Total Customers Acquired** |         `319,260` |
| **Portfolio ROAS**           |          `15.84x` |
| **Net Portfolio ROI**        |       `1,484.10%` |
| **Overall CAC**              |          `$25.69` |

### Channel Comparison

| Marketing Channel   | Total Spend ($) | Total Revenue ($) | Conversions | Customers |   CR (%) |   CAC ($) |  ROAS (x) |      ROI (%) |
| ------------------- | --------------: | ----------------: | ----------: | --------: | -------: | --------: | --------: | -----------: |
| **SEO**             |   `$392,405.30` |  `$41,080,559.97` |   `141,659` |  `92,233` | `13.11%` |   `$4.25` | `104.69x` | `10,368.91%` |
| **Email Marketing** |   `$430,646.34` |  `$38,674,035.89` |   `150,030` | `106,750` | `16.92%` |   `$4.03` |  `89.80x` |  `8,880.23%` |
| **Google Ads**      | `$2,056,606.20` |  `$18,379,019.24` |    `66,036` |  `46,428` | `10.99%` |  `$44.30` |   `8.94x` |    `793.66%` |
| **Facebook Ads**    | `$1,310,472.42` |  `$10,836,654.51` |    `42,752` |  `30,250` |  `8.29%` |  `$43.32` |   `8.27x` |    `726.93%` |
| **LinkedIn Ads**    | `$1,153,256.09` |   `$8,000,958.82` |    `12,852` |   `6,924` |  `9.70%` | `$166.56` |   `6.94x` |    `593.78%` |
| **Instagram Ads**   | `$1,412,825.49` |   `$8,065,302.39` |    `30,736` |  `22,990` |  `7.40%` |  `$61.46` |   `5.71x` |    `470.86%` |
| **YouTube Ads**     |   `$720,636.32` |   `$3,896,076.62` |    `18,728` |  `10,619` |  `3.99%` |  `$67.86` |   `5.41x` |    `440.64%` |
| **Display Ads**     |   `$725,860.59` |   `$1,006,214.28` |     `3,545` |   `3,066` |  `1.46%` | `$258.59` |   `1.39x` |     `38.62%` |

---

## 📊 Data Visualizations

The project generates multiple analytical charts to understand campaign and channel performance.

### Generated Visualizations

1. Revenue by Marketing Channel
2. Advertising Spend by Marketing Channel
3. ROAS by Marketing Channel
4. CAC by Marketing Channel
5. Conversion Rate by Marketing Channel
6. ROI by Marketing Channel
7. Monthly Revenue Trend
8. Monthly Advertising Spend Trend
9. Campaign Performance Comparison
10. Revenue vs Advertising Spend
11. Conversion Rate vs CAC
12. ROAS Campaign Comparison

All generated charts are stored inside:

```text
charts/
```

---

## 💡 Automated Dynamic Business Insights

Automated insight generation is implemented using:

```text
python/insights.py
```

The analysis identifies important performance patterns from the campaign data.

### Key Observations

1. **SEO Revenue Performance**

   SEO generated approximately `$41.08M` in revenue and recorded a calculated ROAS of `104.69x`.

2. **Email Marketing Acquisition Efficiency**

   Email Marketing recorded a CAC of approximately `$4.03` and a conversion rate of `16.92%`.

3. **Display Advertising Efficiency**

   Display Ads recorded a CAC of approximately `$258.59` and a ROAS of `1.39x`.

4. **Google Ads Spending**

   Google Ads accounted for approximately `25.1%` of total advertising spend, with approximately `$18.38M` in revenue and a ROAS of `8.94x`.

These observations are generated from the underlying dataset and KPI calculations.

---

## 🎯 Strategic Business Recommendations

Based on the calculated performance metrics, the project provides the following analytical recommendations:

### 1. Monitor High-ROAS Channels

Channels with comparatively high ROAS and lower acquisition costs can be evaluated for potential expansion while monitoring scalability and incremental returns.

### 2. Review Low-Efficiency Paid Channels

Channels with relatively high CAC and lower ROAS should be investigated for campaign targeting, creative performance, landing page effectiveness, and budget efficiency.

### 3. Optimize B2B Campaign Performance

LinkedIn campaigns can be evaluated using audience segmentation, bid optimization, and high-intent targeting to improve acquisition efficiency.

### 4. Improve Funnel Conversion

Landing page A/B testing and funnel optimization can be used to improve conversion performance, particularly for channels with comparatively lower conversion rates.

---

## 🗂️ Project Structure

```text
Marketing-Campaign-ROI-Analysis/
│
├── data/
│   ├── raw_marketing_data.csv
│   └── cleaned_marketing_data.csv
│
├── python/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── data_cleaning.py
│   ├── kpi_calculation.py
│   ├── campaign_analysis.py
│   ├── visualization.py
│   ├── insights.py
│   ├── generate_excel.py
│   ├── generate_pdf_report.py
│   └── generate_notebook.py
│
├── notebooks/
│   └── marketing_campaign_analysis.ipynb
│
├── excel/
│   └── Marketing_Campaign_ROI_Analysis.xlsx
│
├── reports/
│   ├── Marketing_Campaign_ROI_Report.pdf
│   └── Marketing_Campaign_ROI_Report.md
│
├── charts/
│   ├── 1_revenue_by_channel.png
│   ├── 2_spend_by_channel.png
│   ├── 3_roas_by_channel.png
│   ├── 4_cac_by_channel.png
│   ├── 5_conversion_rate_by_channel.png
│   ├── 6_roi_by_channel.png
│   ├── 7_monthly_revenue_trend.png
│   ├── 8_monthly_spend_trend.png
│   ├── 9_campaign_performance_comparison.png
│   ├── 10_revenue_vs_ad_spend.png
│   ├── 11_conversion_rate_vs_cac.png
│   └── 12_roas_campaign_comparison.png
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## ⚙️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/AkritiDas/Marketing-Campaign-ROI-Analysis.git
cd Marketing-Campaign-ROI-Analysis
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn openpyxl reportlab nbformat xlsxwriter
```

### 4. Run the Complete Analysis Pipeline

```bash
python main.py
```

The pipeline performs the required data processing and analysis tasks and generates the corresponding analytical outputs.

---

## 📊 Generated Outputs

After running the project, the following outputs are available:

### Cleaned Dataset

```text
data/cleaned_marketing_data.csv
```

### Excel Analysis

```text
excel/Marketing_Campaign_ROI_Analysis.xlsx
```

### Jupyter Notebook

```text
notebooks/marketing_campaign_analysis.ipynb
```

### PDF Executive Report

```text
reports/Marketing_Campaign_ROI_Report.pdf
```

### Markdown Report

```text
reports/Marketing_Campaign_ROI_Report.md
```

### Visualization Charts

```text
charts/
```

---

## 📝 Resume-Ready Project Description

### Marketing Campaign ROI Analysis | Python, Excel

* Analyzed **3,000 marketing campaign records** across multiple digital marketing channels using Python and Excel.
* Performed data cleaning, validation, aggregation, and KPI calculation using **Pandas and NumPy**.
* Calculated **CTR, Conversion Rate, CPC, CPL, CAC, ROAS, and ROI** to evaluate campaign and channel performance.
* Built **12 analytical visualizations** covering revenue, advertising spend, conversion efficiency, CAC, ROAS, ROI, and monthly trends.
* Developed an **interactive Excel analysis dashboard** with automated calculations, formatting, and business performance reporting.
* Generated automated business insights to identify channel-level performance patterns and marketing efficiency opportunities.
* Created an executive-level **PDF business report** and Jupyter Notebook for analytical documentation and presentation.

---

## 🔍 Key Skills Demonstrated

* Business Analytics
* Data Analytics
* Python
* Pandas
* NumPy
* Data Cleaning
* Exploratory Data Analysis
* KPI Analysis
* Marketing Analytics
* ROI Analysis
* ROAS Analysis
* Customer Acquisition Cost Analysis
* Excel Dashboard Development
* Data Visualization
* Business Intelligence
* Automated Reporting
* Business Insights
* Git & GitHub

---

## 👨‍💻 Author

**Akriti Das**

Marketing Campaign ROI Analysis Project

GitHub Repository:

https://github.com/AkritiDas/Marketing-Campaign-ROI-Analysis

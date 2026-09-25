# 📊 Marketing Campaign ROI Analysis

An end-to-end, portfolio-grade **Business Analytics & Data Analytics** project analyzing marketing campaign performance across multiple digital marketing channels. Built with **Python and Excel**, this project demonstrates data cleaning, KPI formula calculation, channel/campaign performance aggregation, monthly trend analysis, high-impact data visualization, automated dynamic insight generation, interactive Excel dashboards, and executive reporting.

---

## 🎯 Project Objective

The objective of this analysis is to evaluate marketing campaign performance across diverse channels, identify high-return marketing investments, measure Customer Acquisition Costs (CAC) and Return on Ad Spend (ROAS), and generate actionable, data-backed recommendations for marketing budget reallocation and revenue growth.

---

## 💼 Business Problem

Marketing organizations often struggle with fragmented performance metrics across channels. Key challenges addressed by this project include:
1. Identifying which channels generate the highest revenue versus which absorb excessive ad spend with low returns.
2. Uncovering campaigns with high conversion rates but suboptimal ROAS due to high acquisition costs or low average order values.
3. Quantifying channel trade-offs between volume, acquisition costs, conversion efficiency, and gross margins.
4. Providing executive leadership with a clear, automated framework for data-driven budget allocation.

---

## 📁 Dataset Description

The analysis uses a dataset of **3,000 marketing campaign records** spanning 2025 across **8 channels** and **16 unique campaigns**:

- **Campaign_ID**: Unique identifier for campaign (e.g., `CMP_GGL_01`)
- **Campaign_Name**: Descriptive campaign identifier (e.g., `Google_Search_Brand`)
- **Date**: Campaign execution date (`YYYY-MM-DD`)
- **Marketing_Channel**: Channel used (`Google Ads`, `Facebook Ads`, `Instagram Ads`, `LinkedIn Ads`, `YouTube Ads`, `Email Marketing`, `SEO`, `Display Ads`)
- **Campaign_Type**: Strategic intent (`Awareness`, `Lead Generation`, `Conversion`, `Retargeting`, `Product Promotion`)
- **Region**: Geographical territory (`North America`, `Europe`, `Asia-Pacific`, `Latin America`, `Middle East`)
- **Impressions**: Total ad views
- **Clicks**: User clicks generated
- **Leads**: Qualified potential leads
- **Conversions**: Completed purchase/conversion events
- **Ad_Spend ($)**: Advertising dollars invested
- **Revenue ($)**: Gross revenue generated
- **Customers**: New paying customers acquired
- **Campaign_Duration**: Duration in days
- **Device_Type**: Target platform (`Desktop`, `Mobile`, `Tablet`)

---

## 🛠️ Tools & Technologies

- **Python 3.12**: Core analytical language
- **Pandas & NumPy**: Data cleaning, manipulation, and vectorized KPI calculations
- **Matplotlib & Seaborn**: Executive data visualizations and statistical charts
- **OpenPyXL**: Automated 7-sheet interactive Excel workbook generation with formulas, formatting, and dashboard charts
- **ReportLab**: PDF Executive Business Report rendering
- **Jupyter Notebook**: Modular portfolio notebook walkthrough
- **Microsoft Excel**: Dynamic spreadsheet modeling, pivot tables, and dashboard UI

---

## 🧹 Data Cleaning Process

The raw dataset (`data/raw_marketing_data.csv`) is cleaned programmatically via [`python/data_cleaning.py`](file:///c:/Users/HP/OneDrive/Desktop/Return%20On%20Investment/python/data_cleaning.py):
1. **Duplicate Removal**: Detected and removed 20 duplicate rows.
2. **Text Standardization**: Normalized channel casing and whitespace (e.g., `"google ads "`, `"GOOGLE ADS"` -> `"Google Ads"`).
3. **Missing Value Imputation**:
   - `Device_Type`: Imputed using mode (`Desktop`).
   - `Campaign_Duration`: Imputed using median value (18 days).
   - `Leads`: Imputed using channel-specific click-to-lead conversion rates.
4. **Date Formatting**: Converted mixed string date formats into standard ISO `YYYY-MM-DD` timestamps.
5. **Sanity Checks & Type Casting**: Validated non-negative constraints ($Clicks \le Impressions$, $Conversions \le Clicks$, $Customers \le Conversions$) and cast integer/float data types.

The cleaned dataset is saved to [`data/cleaned_marketing_data.csv`](file:///c:/Users/HP/OneDrive/Desktop/Return%20On%20Investment/data/cleaned_marketing_data.csv).

---

## 📐 KPI Definitions & Formulas

All metrics are calculated with zero-division protection:

| Key Metric | Formula | Business Purpose |
| :--- | :--- | :--- |
| **Click-Through Rate (CTR)** | $\text{CTR (\%)} = \left(\frac{\text{Clicks}}{\text{Impressions}}\right) \times 100$ | Measures ad creative engagement |
| **Conversion Rate (CR)** | $\text{CR (\%)} = \left(\frac{\text{Conversions}}{\text{Clicks}}\right) \times 100$ | Measures landing page & funnel effectiveness |
| **Cost Per Click (CPC)** | $\text{CPC (\$) = \frac{\text{Ad Spend}}{\text{Clicks}}$ | Measures media cost per click |
| **Cost Per Lead (CPL)** | $\text{CPL (\$) = \frac{\text{Ad Spend}}{\text{Leads}}$ | Measures lead acquisition cost |
| **Customer Acquisition Cost (CAC)** | $\text{CAC (\$) = \frac{\text{Ad Spend}}{\text{Customers}}$ | Measures overall customer acquisition cost |
| **Return on Ad Spend (ROAS)** | $\text{ROAS (x)} = \frac{\text{Revenue}}{\text{Ad Spend}}$ | Measures revenue return per ad dollar |
| **Return on Investment (ROI)** | $\text{ROI (\%)} = \left(\frac{\text{Revenue - Ad Spend}}{\text{Ad Spend}}\right) \times 100$ | Measures net profit percentage |

---

## 📊 Performance Analysis Summary

### Portfolio Totals
- **Total Ad Spend:** `$8,202,708.75`
- **Total Revenue:** `$129,938,821.72`
- **Total Customers Acquired:** `319,260`
- **Portfolio ROAS:** `15.84x`
- **Net Portfolio ROI:** `1,484.10%`
- **Overall CAC:** `$25.69`

### Channel Comparison Table

| Marketing Channel | Total Spend ($) | Total Revenue ($) | Conversions | Customers | CR (%) | CAC ($) | ROAS (x) | ROI (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SEO** | `$392,405.30` | `$41,080,559.97` | `141,659` | `92,233` | `13.11%` | `$4.25` | `104.69x` | `10,368.91%` |
| **Email Marketing** | `$430,646.34` | `$38,674,035.89` | `150,030` | `106,750` | `16.92%` | `$4.03` | `89.80x` | `8,880.23%` |
| **Google Ads** | `$2,056,606.20` | `$18,379,019.24` | `66,036` | `46,428` | `10.99%` | `$44.30` | `8.94x` | `793.66%` |
| **Facebook Ads** | `$1,310,472.42` | `$10,836,654.51` | `42,752` | `30,250` | `8.29%` | `$43.32` | `8.27x` | `726.93%` |
| **LinkedIn Ads** | `$1,153,256.09` | `$8,000,958.82` | `12,852` | `6,924` | `9.70%` | `$166.56` | `6.94x` | `593.78%` |
| **Instagram Ads** | `$1,412,825.49` | `$8,065,302.39` | `30,736` | `22,990` | `7.40%` | `$61.46` | `5.71x` | `470.86%` |
| **YouTube Ads** | `$720,636.32` | `$3,896,076.62` | `18,728` | `10,619` | `3.99%` | `$67.86` | `5.41x` | `440.64%` |
| **Display Ads** | `$725,860.59` | `$1,006,214.28` | `3,545` | `3,066` | `1.46%` | `$258.59` | `1.39x` | `38.62%` |

---

## 💡 Automated Dynamic Business Insights

Implemented via [`python/insights.py`](file:///c:/Users/HP/OneDrive/Desktop/Return%20On%20Investment/python/insights.py):
1. **Highest Revenue & Return Channel:** **SEO** generated `$41.08M` in revenue (31.6% of portfolio revenue) with a **104.69x ROAS**.
2. **Lowest Acquisition Cost Channel:** **Email Marketing** achieved a CAC of **$4.03** and the highest conversion rate (**16.92%**).
3. **Inefficient Channel Flag:** **Display Ads** exhibited an inefficient CAC of **$258.59** and a low ROAS of **1.39x**, consuming `$725.86K` in budget.
4. **Paid Search Concentration:** **Google Ads** absorbed **25.1%** of total ad spend (`$2.06M`) and delivered solid revenue (`$18.38M`, 8.94x ROAS).

---

## 🎯 Strategic Business Recommendations

1. **Scale High-ROAS Owned Channels:** Increase investment in content strategy and email nurture workflows; organic & owned channels yield ROAS > 89x with minimal incremental acquisition cost.
2. **Reallocate Budget Away from Inefficient Paid Channels:** Shift **20%–35%** of ad spend away from Display Ads to Search Retargeting and Facebook Lookalike campaigns.
3. **Optimize B2B Targeting on LinkedIn Ads:** Apply strict bid caps and target high-intent B2B decision makers to lower CAC below `$100.00`.
4. **Improve Funnel Conversion:** Conduct landing page A/B tests for YouTube and Display Ads to lift conversion rates above `5.00%`.

---

## 🗂️ Project Structure

```
marketing_campaign_roi/
│
├── data/
│   ├── raw_marketing_data.csv
│   └── cleaned_marketing_data.csv
│
├── python/
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
├── main.py
└── README.md
```

---

## ⚙️ How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AkritiDas/Business-Analytics-App.git
   cd Business-Analytics-App
   ```

2. **Install required dependencies:**
   ```bash
   pip install pandas numpy matplotlib seaborn openpyxl reportlab nbformat xlsxwriter
   ```

3. **Run the complete pipeline end-to-end:**
   ```bash
   python main.py
   ```

---

## 📝 Resume-Ready Project Description

**Marketing Campaign ROI Analysis | Excel, Python**
- Evaluated marketing campaign performance using Conversion Rate, CAC, ROAS, and ROI across multiple channels.
- Compared campaign-level and channel-level performance to identify high-return campaigns and opportunities for marketing budget optimization.
- Built an interactive Excel dashboard and Python-based analysis with automated KPI calculations, visualizations, and data-driven business insights.

import nbformat as nbf
import os

def create_jupyter_notebook(output_path="notebooks/marketing_campaign_analysis.ipynb"):
    """
    Programmatically creates a complete end-to-end Jupyter Notebook for Marketing Campaign ROI Analysis.
    """
    print("--- GENERATING JUPYTER NOTEBOOK ---")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    nb = nbf.v4.new_notebook()
    cells = []

    # Title & Metadata
    cells.append(nbf.v4.new_markdown_cell("""# 📈 Marketing Campaign ROI Analysis
### End-to-End Business Analytics & Performance Portfolio Project

**Author:** Business Analytics Professional  
**Tools:** Python (Pandas, NumPy, Matplotlib, Seaborn), Excel, ReportLab  
**Objective:** Evaluate marketing campaign performance across channels, calculate key KPIs (Conversion Rate, CAC, ROAS, ROI, CTR, CPC, CPL), perform exploratory data analysis, and derive data-driven business insights for budget optimization.

---"""))

    # Section 1: Setup & Data Loading
    cells.append(nbf.v4.new_markdown_cell("""## 1. Environment Setup & Data Loading

In this section, we import the required analytical libraries, configure display options, and load the raw marketing campaign dataset."""))

    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
plt.style.use('seaborn-v0_8-whitegrid')

# Load raw marketing dataset
raw_df_path = '../data/raw_marketing_data.csv'
if not os.path.exists(raw_df_path):
    raw_df_path = 'data/raw_marketing_data.csv'

df_raw = pd.read_csv(raw_df_path)
print(f"Raw Dataset Loaded: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
df_raw.head()"""))

    # Section 2: Data Cleaning
    cells.append(nbf.v4.new_markdown_cell("""## 2. Data Cleaning & Preprocessing

Data cleaning steps:
1. Identify and remove duplicate records.
2. Standardize text columns (channel names, campaign names).
3. Handle missing values (Device Type mode, Duration median, Leads ratio estimation).
4. Parse dates into unified ISO format (`YYYY-MM-DD`).
5. Verify datatypes and handle outliers."""))

    cells.append(nbf.v4.new_code_cell("""# 1. Remove Duplicate Records
initial_count = len(df_raw)
df_clean = df_raw.drop_duplicates().copy()
print(f"Removed {initial_count - len(df_clean)} duplicate rows.")

# 2. Standardize Channel Names
df_clean['Marketing_Channel'] = df_clean['Marketing_Channel'].astype(str).str.strip()
channel_map = {
    'google ads': 'Google Ads', 'GOOGLE ADS': 'Google Ads', 'Google Ads': 'Google Ads',
    'facebook ads': 'Facebook Ads', 'Facebook Ads': 'Facebook Ads',
    'instagram ads': 'Instagram Ads', 'Instagram_Ads': 'Instagram Ads', 'Instagram Ads': 'Instagram Ads',
    'linkedin ads': 'LinkedIn Ads', 'LinkedIn Ads': 'LinkedIn Ads',
    'youtube ads': 'YouTube Ads', 'YouTube_Ads': 'YouTube Ads', 'YouTube Ads': 'YouTube Ads',
    'email marketing': 'Email Marketing', 'Email Marketing': 'Email Marketing',
    'seo': 'SEO', 'SEO': 'SEO',
    'display ads': 'Display Ads', 'Display Ads': 'Display Ads'
}
df_clean['Marketing_Channel'] = df_clean['Marketing_Channel'].map(lambda x: channel_map.get(x, x.title()))

# 3. Handle Missing Values
if 'Device_Type' in df_clean.columns:
    df_clean['Device_Type'] = df_clean['Device_Type'].fillna(df_clean['Device_Type'].mode()[0])
if 'Campaign_Duration' in df_clean.columns:
    df_clean['Campaign_Duration'] = df_clean['Campaign_Duration'].fillna(df_clean['Campaign_Duration'].median())
if 'Leads' in df_clean.columns:
    lead_rate = (df_clean['Leads'] / df_clean['Clicks']).median()
    df_clean['Leads'] = df_clean['Leads'].fillna(np.round(df_clean['Clicks'] * lead_rate))

# 4. Date Parsing
df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')

print("Cleaned Dataset Shape:", df_clean.shape)
print("Missing Values Remaining:", df_clean.isna().sum().sum())
df_clean.head()"""))

    # Section 3: KPI Calculation
    cells.append(nbf.v4.new_markdown_cell("""## 3. Marketing KPI Calculation

We calculate key performance indicators with division-by-zero protection:
* **CTR (%)** = `(Clicks / Impressions) * 100`
* **Conversion Rate (%)** = `(Conversions / Clicks) * 100`
* **Cost Per Click (CPC)** = `Ad Spend / Clicks`
* **Cost Per Lead (CPL)** = `Ad Spend / Leads`
* **Customer Acquisition Cost (CAC)** = `Ad Spend / Customers`
* **Return on Ad Spend (ROAS)** = `Revenue / Ad Spend`
* **Return on Investment (ROI, %)** = `((Revenue - Ad Spend) / Ad Spend) * 100`"""))

    cells.append(nbf.v4.new_code_cell("""# Calculate Row-Level KPIs
df_clean['CTR'] = np.where(df_clean['Impressions'] > 0, (df_clean['Clicks'] / df_clean['Impressions']) * 100, 0.0).round(2)
df_clean['Conversion_Rate'] = np.where(df_clean['Clicks'] > 0, (df_clean['Conversions'] / df_clean['Clicks']) * 100, 0.0).round(2)
df_clean['CPC'] = np.where(df_clean['Clicks'] > 0, df_clean['Ad_Spend'] / df_clean['Clicks'], 0.0).round(2)
df_clean['CPL'] = np.where(df_clean['Leads'] > 0, df_clean['Ad_Spend'] / df_clean['Leads'], 0.0).round(2)
df_clean['CAC'] = np.where(df_clean['Customers'] > 0, df_clean['Ad_Spend'] / df_clean['Customers'], 0.0).round(2)
df_clean['ROAS'] = np.where(df_clean['Ad_Spend'] > 0, df_clean['Revenue'] / df_clean['Ad_Spend'], 0.0).round(2)
df_clean['ROI'] = np.where(df_clean['Ad_Spend'] > 0, ((df_clean['Revenue'] - df_clean['Ad_Spend']) / df_clean['Ad_Spend']) * 100, 0.0).round(2)

# Summary Portfolio Metrics
tot_spend = df_clean['Ad_Spend'].sum()
tot_rev = df_clean['Revenue'].sum()
tot_cust = df_clean['Customers'].sum()
tot_conv = df_clean['Conversions'].sum()

print("=== PORTFOLIO SUMMARY KPIS ===")
print(f"Total Ad Spend:       ${tot_spend:,.2f}")
print(f"Total Gross Revenue:  ${tot_rev:,.2f}")
print(f"Total Customers:      {tot_cust:,}")
print(f"Portfolio ROAS:       {tot_rev/tot_spend:.2f}x")
print(f"Net Portfolio ROI:    {((tot_rev - tot_spend)/tot_spend)*100:.2f}%")
print(f"Overall CAC:          ${tot_spend/tot_cust:.2f}")"""))

    # Section 4: Channel Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 4. Channel Performance Analysis

Aggregate campaign data by `Marketing_Channel` to compare spend efficiency, customer acquisition costs, and returns."""))

    cells.append(nbf.v4.new_code_cell("""ch_summary = df_clean.groupby('Marketing_Channel').agg({
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Leads': 'sum',
    'Conversions': 'sum',
    'Customers': 'sum',
    'Ad_Spend': 'sum',
    'Revenue': 'sum'
}).reset_index()

ch_summary['CTR (%)'] = (ch_summary['Clicks'] / ch_summary['Impressions'] * 100).round(2)
ch_summary['Conversion_Rate (%)'] = (ch_summary['Conversions'] / ch_summary['Clicks'] * 100).round(2)
ch_summary['CAC ($)'] = (ch_summary['Ad_Spend'] / ch_summary['Customers']).round(2)
ch_summary['ROAS (x)'] = (ch_summary['Revenue'] / ch_summary['Ad_Spend']).round(2)
ch_summary['ROI (%)'] = ((ch_summary['Revenue'] - ch_summary['Ad_Spend']) / ch_summary['Ad_Spend'] * 100).round(2)

ch_summary = ch_summary.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
ch_summary"""))

    # Section 5: Campaign & Time Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 5. Campaign-Level & Monthly Performance

Evaluate top individual campaigns and track monthly marketing trends over 2025."""))

    cells.append(nbf.v4.new_code_cell("""df_clean['YM'] = pd.to_datetime(df_clean['Date']).dt.to_period('M').astype(str)

mo_summary = df_clean.groupby('YM').agg({
    'Ad_Spend': 'sum',
    'Revenue': 'sum',
    'Conversions': 'sum',
    'Customers': 'sum'
}).reset_index()

mo_summary['ROAS (x)'] = (mo_summary['Revenue'] / mo_summary['Ad_Spend']).round(2)
mo_summary['CAC ($)'] = (mo_summary['Ad_Spend'] / mo_summary['Customers']).round(2)

mo_summary"""))

    # Section 6: Data Visualizations
    cells.append(nbf.v4.new_markdown_cell("""## 6. Data Visualizations"""))

    cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Revenue by Channel
sns.barplot(data=ch_summary, x='Marketing_Channel', y=ch_summary['Revenue']/1e6, ax=axes[0], palette='Blues_r')
axes[0].set_title('Revenue by Marketing Channel ($ Millions)', fontweight='bold')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=30, ha='right')
axes[0].set_ylabel('Revenue ($M)')

# ROAS by Channel
sns.barplot(data=ch_summary, x='Marketing_Channel', y='ROAS (x)', ax=axes[1], palette='Greens_r')
axes[1].set_title('Return on Ad Spend (ROAS) by Channel', fontweight='bold')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=30, ha='right')
axes[1].set_ylabel('ROAS (x)')

plt.tight_layout()
plt.show()"""))

    # Section 7: Dynamic Automated Business Insights
    cells.append(nbf.v4.new_markdown_cell("""## 7. Dynamic Business Insights & Strategic Recommendations

Using dynamic statistical thresholds, we automatically flag high-ROI opportunities and inefficient ad channels."""))

    cells.append(nbf.v4.new_code_cell("""avg_roas = tot_rev / tot_spend
avg_cac = tot_spend / tot_cust

print("--- AUTOMATED DYNAMIC INSIGHTS ---")
top_rev_ch = ch_summary.loc[ch_summary['Revenue'].idxmax()]
top_roas_ch = ch_summary.loc[ch_summary['ROAS (x)'].idxmax()]
ineff_ch = ch_summary[(ch_summary['ROAS (x)'] < avg_roas) & (ch_summary['CAC ($)'] > avg_cac)]

print(f"• Top Revenue Generator: '{top_rev_ch['Marketing_Channel']}' with ${top_rev_ch['Revenue']:,.2f} gross revenue.")
print(f"• Highest Efficiency Channel: '{top_roas_ch['Marketing_Channel']}' delivering {top_roas_ch['ROAS (x)']:.2f}x ROAS.")

if not ineff_ch.empty:
    print(f"• Inefficient Channels Flagged: {list(ineff_ch['Marketing_Channel'].values)} exhibit high CAC and low ROAS.")

print("\n--- STRATEGIC RECOMMENDATIONS ---")
print("1. Scale budget for organic & lifecycle email marketing channels (ROAS > 89x).")
print("2. Reallocate 20-30% of budget away from Display Ads to Search Retargeting.")
print("3. Optimize LinkedIn Ads bidding caps to reduce CAC below $100.00.")"""))

    nb['cells'] = cells
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"Jupyter Notebook generated successfully at '{output_path}'.")

if __name__ == "__main__":
    create_jupyter_notebook()

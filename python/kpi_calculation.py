import pandas as pd
import numpy as np

def calculate_row_kpis(df):
    """
    Calculates marketing KPIs at the row level for a given DataFrame.
    Returns a copy of DataFrame with added KPI columns.
    
    KPIs:
    1. CTR (%) = (Clicks / Impressions) * 100
    2. Conversion Rate (%) = (Conversions / Clicks) * 100
    3. CPC ($) = Ad Spend / Clicks
    4. CPL ($) = Ad Spend / Leads
    5. CAC ($) = Ad Spend / Customers
    6. ROAS (x) = Revenue / Ad Spend
    7. ROI (%) = ((Revenue - Ad Spend) / Ad Spend) * 100
    """
    df_kpi = df.copy()

    # Safe division helpers
    df_kpi['CTR'] = np.where(df_kpi['Impressions'] > 0, (df_kpi['Clicks'] / df_kpi['Impressions']) * 100, 0.0)
    df_kpi['Conversion_Rate'] = np.where(df_kpi['Clicks'] > 0, (df_kpi['Conversions'] / df_kpi['Clicks']) * 100, 0.0)
    df_kpi['CPC'] = np.where(df_kpi['Clicks'] > 0, df_kpi['Ad_Spend'] / df_kpi['Clicks'], 0.0)
    df_kpi['CPL'] = np.where(df_kpi['Leads'] > 0, df_kpi['Ad_Spend'] / df_kpi['Leads'], 0.0)
    df_kpi['CAC'] = np.where(df_kpi['Customers'] > 0, df_kpi['Ad_Spend'] / df_kpi['Customers'], 0.0)
    df_kpi['ROAS'] = np.where(df_kpi['Ad_Spend'] > 0, df_kpi['Revenue'] / df_kpi['Ad_Spend'], 0.0)
    df_kpi['ROI'] = np.where(df_kpi['Ad_Spend'] > 0, ((df_kpi['Revenue'] - df_kpi['Ad_Spend']) / df_kpi['Ad_Spend']) * 100, 0.0)

    # Round financial and percentage metrics appropriately
    df_kpi['CTR'] = df_kpi['CTR'].round(2)
    df_kpi['Conversion_Rate'] = df_kpi['Conversion_Rate'].round(2)
    df_kpi['CPC'] = df_kpi['CPC'].round(2)
    df_kpi['CPL'] = df_kpi['CPL'].round(2)
    df_kpi['CAC'] = df_kpi['CAC'].round(2)
    df_kpi['ROAS'] = df_kpi['ROAS'].round(2)
    df_kpi['ROI'] = df_kpi['ROI'].round(2)

    return df_kpi

def calculate_summary_kpis(df):
    """
    Calculates overall dataset-level summary KPIs.
    Returns a dictionary of aggregate metrics.
    """
    total_impressions = df['Impressions'].sum()
    total_clicks = df['Clicks'].sum()
    total_leads = df['Leads'].sum()
    total_conversions = df['Conversions'].sum()
    total_customers = df['Customers'].sum()
    total_ad_spend = df['Ad_Spend'].sum()
    total_revenue = df['Revenue'].sum()

    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0.0
    cpc = (total_ad_spend / total_clicks) if total_clicks > 0 else 0.0
    cpl = (total_ad_spend / total_leads) if total_leads > 0 else 0.0
    cac = (total_ad_spend / total_customers) if total_customers > 0 else 0.0
    roas = (total_revenue / total_ad_spend) if total_ad_spend > 0 else 0.0
    roi = ((total_revenue - total_ad_spend) / total_ad_spend * 100) if total_ad_spend > 0 else 0.0

    return {
        "Total_Impressions": int(total_impressions),
        "Total_Clicks": int(total_clicks),
        "Total_Leads": int(total_leads),
        "Total_Conversions": int(total_conversions),
        "Total_Customers": int(total_customers),
        "Total_Ad_Spend": round(total_ad_spend, 2),
        "Total_Revenue": round(total_revenue, 2),
        "CTR (%)": round(ctr, 2),
        "Conversion_Rate (%)": round(conversion_rate, 2),
        "CPC ($)": round(cpc, 2),
        "CPL ($)": round(cpl, 2),
        "CAC ($)": round(cac, 2),
        "ROAS (x)": round(roas, 2),
        "ROI (%)": round(roi, 2)
    }

if __name__ == "__main__":
    df_clean = pd.read_csv("data/cleaned_marketing_data.csv")
    df_kpi = calculate_row_kpis(df_clean)
    summary = calculate_summary_kpis(df_clean)
    print("--- OVERALL MARKETING KPIS SUMMARY ---")
    for k, v in summary.items():
        print(f"{k}: {v}")

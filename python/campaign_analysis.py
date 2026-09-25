import pandas as pd
import numpy as np

def analyze_channel_performance(df):
    """
    Aggregates metrics by Marketing Channel and calculates true channel-level KPIs.
    """
    grouped = df.groupby('Marketing_Channel').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Leads': 'sum',
        'Conversions': 'sum',
        'Customers': 'sum',
        'Ad_Spend': 'sum',
        'Revenue': 'sum'
    }).reset_index()

    # Calculate Channel KPIs from aggregated sums
    grouped['CTR (%)'] = np.where(grouped['Impressions'] > 0, (grouped['Clicks'] / grouped['Impressions']) * 100, 0).round(2)
    grouped['Conversion_Rate (%)'] = np.where(grouped['Clicks'] > 0, (grouped['Conversions'] / grouped['Clicks']) * 100, 0).round(2)
    grouped['CPC ($)'] = np.where(grouped['Clicks'] > 0, grouped['Ad_Spend'] / grouped['Clicks'], 0).round(2)
    grouped['CPL ($)'] = np.where(grouped['Leads'] > 0, grouped['Ad_Spend'] / grouped['Leads'], 0).round(2)
    grouped['CAC ($)'] = np.where(grouped['Customers'] > 0, grouped['Ad_Spend'] / grouped['Customers'], 0).round(2)
    grouped['ROAS (x)'] = np.where(grouped['Ad_Spend'] > 0, grouped['Revenue'] / grouped['Ad_Spend'], 0).round(2)
    grouped['ROI (%)'] = np.where(grouped['Ad_Spend'] > 0, ((grouped['Revenue'] - grouped['Ad_Spend']) / grouped['Ad_Spend']) * 100, 0).round(2)

    # Sort by Revenue descending
    grouped = grouped.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
    return grouped

def analyze_campaign_performance(df):
    """
    Aggregates metrics by Campaign_Name and calculates campaign-level KPIs.
    """
    grouped = df.groupby(['Campaign_Name', 'Marketing_Channel', 'Campaign_Type']).agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Leads': 'sum',
        'Conversions': 'sum',
        'Customers': 'sum',
        'Ad_Spend': 'sum',
        'Revenue': 'sum'
    }).reset_index()

    grouped['CTR (%)'] = np.where(grouped['Impressions'] > 0, (grouped['Clicks'] / grouped['Impressions']) * 100, 0).round(2)
    grouped['Conversion_Rate (%)'] = np.where(grouped['Clicks'] > 0, (grouped['Conversions'] / grouped['Clicks']) * 100, 0).round(2)
    grouped['CPC ($)'] = np.where(grouped['Clicks'] > 0, grouped['Ad_Spend'] / grouped['Clicks'], 0).round(2)
    grouped['CPL ($)'] = np.where(grouped['Leads'] > 0, grouped['Ad_Spend'] / grouped['Leads'], 0).round(2)
    grouped['CAC ($)'] = np.where(grouped['Customers'] > 0, grouped['Ad_Spend'] / grouped['Customers'], 0).round(2)
    grouped['ROAS (x)'] = np.where(grouped['Ad_Spend'] > 0, grouped['Revenue'] / grouped['Ad_Spend'], 0).round(2)
    grouped['ROI (%)'] = np.where(grouped['Ad_Spend'] > 0, ((grouped['Revenue'] - grouped['Ad_Spend']) / grouped['Ad_Spend']) * 100, 0).round(2)

    grouped = grouped.sort_values(by='Revenue', ascending=False).reset_index(drop=True)
    return grouped

def analyze_monthly_performance(df):
    """
    Aggregates metrics by Month (YYYY-MM) to identify trends over time.
    """
    df_temp = df.copy()
    df_temp['Date'] = pd.to_datetime(df_temp['Date'])
    df_temp['Year_Month'] = df_temp['Date'].dt.to_period('M').astype(str)

    grouped = df_temp.groupby('Year_Month').agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Leads': 'sum',
        'Conversions': 'sum',
        'Customers': 'sum',
        'Ad_Spend': 'sum',
        'Revenue': 'sum'
    }).reset_index()

    grouped['CTR (%)'] = np.where(grouped['Impressions'] > 0, (grouped['Clicks'] / grouped['Impressions']) * 100, 0).round(2)
    grouped['Conversion_Rate (%)'] = np.where(grouped['Clicks'] > 0, (grouped['Conversions'] / grouped['Clicks']) * 100, 0).round(2)
    grouped['CPC ($)'] = np.where(grouped['Clicks'] > 0, grouped['Ad_Spend'] / grouped['Clicks'], 0).round(2)
    grouped['CPL ($)'] = np.where(grouped['Leads'] > 0, grouped['Ad_Spend'] / grouped['Leads'], 0).round(2)
    grouped['CAC ($)'] = np.where(grouped['Customers'] > 0, grouped['Ad_Spend'] / grouped['Customers'], 0).round(2)
    grouped['ROAS (x)'] = np.where(grouped['Ad_Spend'] > 0, grouped['Revenue'] / grouped['Ad_Spend'], 0).round(2)
    grouped['ROI (%)'] = np.where(grouped['Ad_Spend'] > 0, ((grouped['Revenue'] - grouped['Ad_Spend']) / grouped['Ad_Spend']) * 100, 0).round(2)

    grouped = grouped.sort_values(by='Year_Month').reset_index(drop=True)
    return grouped

if __name__ == "__main__":
    df_clean = pd.read_csv("data/cleaned_marketing_data.csv")
    ch_df = analyze_channel_performance(df_clean)
    cmp_df = analyze_campaign_performance(df_clean)
    mo_df = analyze_monthly_performance(df_clean)
    
    print("--- TOP 3 CHANNELS BY REVENUE ---")
    print(ch_df[['Marketing_Channel', 'Ad_Spend', 'Revenue', 'ROAS (x)', 'CAC ($)']].head(3))
    
    print("\n--- MONTHLY PERFORMANCE SUMMARY ---")
    print(mo_df[['Year_Month', 'Ad_Spend', 'Revenue', 'ROAS (x)', 'Conversion_Rate (%)']].head(3))

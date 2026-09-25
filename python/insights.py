import sys
import os

# Ensure both workspace root and python folder are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import numpy as np

try:
    from python.campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance
    from python.kpi_calculation import calculate_summary_kpis
except ImportError:
    from campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance
    from kpi_calculation import calculate_summary_kpis




def generate_automated_insights(df):
    """
    Dynamically generates data-driven business insights and recommendations
    based on calculated KPIs and statistical thresholds.
    """
    summary = calculate_summary_kpis(df)
    ch_df = analyze_channel_performance(df)
    cmp_df = analyze_campaign_performance(df)
    mo_df = analyze_monthly_performance(df)

    insights = {
        "executive_highlights": [],
        "channel_insights": [],
        "campaign_insights": [],
        "trend_insights": [],
        "recommendations": []
    }

    # 1. Executive Highlights
    avg_roas = summary['ROAS (x)']
    avg_cac = summary['CAC ($)']
    avg_cr = summary['Conversion_Rate (%)']
    
    insights["executive_highlights"].append(
        f"Total portfolio spend of ${summary['Total_Ad_Spend']:,.2f} generated ${summary['Total_Revenue']:,.2f} "
        f"in total revenue, yielding an overall ROAS of {avg_roas:.2f}x and an ROI of {summary['ROI (%)']:.2f}%."
    )
    insights["executive_highlights"].append(
        f"Acquired {summary['Total_Customers']:,} new customers at an average Customer Acquisition Cost (CAC) of ${avg_cac:.2f} "
        f"and an overall conversion rate of {avg_cr:.2f}%."
    )

    # 2. Channel Level Insights (Dynamic Thresholds)
    top_revenue_channel = ch_df.loc[ch_df['Revenue'].idxmax()]
    top_roas_channel = ch_df.loc[ch_df['ROAS (x)'].idxmax()]
    lowest_cac_channel = ch_df.loc[ch_df['CAC ($)'].idxmin()]
    highest_spend_channel = ch_df.loc[ch_df['Ad_Spend'].idxmax()]
    highest_cr_channel = ch_df.loc[ch_df['Conversion_Rate (%)'].idxmax()]
    
    # Inefficient channels: High spend or CAC above average with below-average ROAS
    inefficient_channels = ch_df[(ch_df['ROAS (x)'] < avg_roas) & (ch_df['CAC ($)'] > avg_cac)]

    insights["channel_insights"].append(
        f"Highest Revenue Generator: '{top_revenue_channel['Marketing_Channel']}' generated the highest revenue "
        f"(${top_revenue_channel['Revenue']:,.2f}), representing {(top_revenue_channel['Revenue']/summary['Total_Revenue'])*100:.1f}% of total portfolio revenue."
    )
    insights["channel_insights"].append(
        f"Highest Efficiency (ROAS): '{top_roas_channel['Marketing_Channel']}' delivered the highest Return on Ad Spend ({top_roas_channel['ROAS (x)']:.2f}x) "
        f"with a very low CAC of ${top_roas_channel['CAC ($)']:.2f}."
    )
    insights["channel_insights"].append(
        f"Lowest CAC Channel: '{lowest_cac_channel['Marketing_Channel']}' acquired customers at the lowest cost (${lowest_cac_channel['CAC ($)']:.2f} per customer)."
    )
    insights["channel_insights"].append(
        f"Highest Conversion Rate Channel: '{highest_cr_channel['Marketing_Channel']}' achieved a lead-to-conversion efficiency of {highest_cr_channel['Conversion_Rate (%)']:.2f}%."
    )
    insights["channel_insights"].append(
        f"Highest Ad Spend Concentration: '{highest_spend_channel['Marketing_Channel']}' absorbed ${highest_spend_channel['Ad_Spend']:,.2f} "
        f"({(highest_spend_channel['Ad_Spend']/summary['Total_Ad_Spend'])*100:.1f}% of total ad spend)."
    )

    if not inefficient_channels.empty:
        for _, ch in inefficient_channels.iterrows():
            insights["channel_insights"].append(
                f"ATTENTION REQUIRED: '{ch['Marketing_Channel']}' exhibits inefficiency — high CAC of ${ch['CAC ($)']:.2f} "
                f"and below-average ROAS of {ch['ROAS (x)']:.2f}x despite high spend (${ch['Ad_Spend']:,.2f})."
            )

    # 3. Campaign Level Insights (Dynamic Rule Evaluation)
    top_cmp_roas = cmp_df.loc[cmp_df['ROAS (x)'].idxmax()]
    high_cac_cmps = cmp_df[cmp_df['CAC ($)'] > avg_cac * 1.5]
    high_cr_low_roas_cmps = cmp_df[(cmp_df['Conversion_Rate (%)'] > avg_cr) & (cmp_df['ROAS (x)'] < avg_roas)]

    insights["campaign_insights"].append(
        f"Star Campaign: '{top_cmp_roas['Campaign_Name']}' ({top_cmp_roas['Marketing_Channel']}) generated an outstanding ROAS of {top_cmp_roas['ROAS (x)']:.2f}x "
        f"and ROI of {top_cmp_roas['ROI (%)']:.2f}%."
    )

    if not high_cac_cmps.empty:
        high_cac_names = ", ".join(high_cac_cmps['Campaign_Name'].head(3).tolist())
        insights["campaign_insights"].append(
            f"High Acquisition Cost Warning: Campaigns [{high_cac_names}] have CACs significantly higher than average (>1.5x portfolio average). "
            f"These require audience targeting refinement or landing page optimization."
        )

    if not high_cr_low_roas_cmps.empty:
        cmp_sample = high_cr_low_roas_cmps.iloc[0]
        insights["campaign_insights"].append(
            f"High Volume / Low Margin Anomaly: Campaign '{cmp_sample['Campaign_Name']}' converts users effectively ({cmp_sample['Conversion_Rate (%)']:.2f}% CR), "
            f"but generates comparatively low ROAS ({cmp_sample['ROAS (x)']:.2f}x) due to low order value or high ad costs."
        )

    # 4. Trend Analysis Insights
    revenue_growth = ((mo_df.iloc[-1]['Revenue'] - mo_df.iloc[0]['Revenue']) / mo_df.iloc[0]['Revenue']) * 100
    spend_growth = ((mo_df.iloc[-1]['Ad_Spend'] - mo_df.iloc[0]['Ad_Spend']) / mo_df.iloc[0]['Ad_Spend']) * 100

    insights["trend_insights"].append(
        f"Monthly Performance Trajectory: From Jan to Dec 2025, revenue grew by {revenue_growth:+.2f}% "
        f"while advertising spend changed by {spend_growth:+.2f}%."
    )
    peak_revenue_month = mo_df.loc[mo_df['Revenue'].idxmax()]
    insights["trend_insights"].append(
        f"Peak Performance Month: {peak_revenue_month['Year_Month']} reached peak monthly revenue of ${peak_revenue_month['Revenue']:,.2f} "
        f"with a ROAS of {peak_revenue_month['ROAS (x)']:.2f}x."
    )

    # 5. Data-Backed Actionable Recommendations
    insights["recommendations"].append(
        f"1. Scalability Opportunity: Scale budget allocation for top-performing organic & low-CAC channels ('{top_roas_channel['Marketing_Channel']}' and '{lowest_cac_channel['Marketing_Channel']}'), "
        f"as they yield ROAS > {top_roas_channel['ROAS (x)']:.1f}x with minimal incremental acquisition cost."
    )
    if not inefficient_channels.empty:
        ineff_name = inefficient_channels.iloc[0]['Marketing_Channel']
        insights["recommendations"].append(
            f"2. Budget Reallocation: Reallocate 15-25% of advertising budget away from '{ineff_name}' (CAC: ${inefficient_channels.iloc[0]['CAC ($)']:.2f}) "
            f"to high-converting paid search & social retargeting campaigns."
        )
    insights["recommendations"].append(
        f"3. Conversion & Pricing Optimization: For high-conversion / low-ROAS campaigns, test upselling, cross-selling, or increasing price points to boost Average Order Value (AOV)."
    )
    insights["recommendations"].append(
        f"4. B2B & Retargeting Focus: Maintain strict bid caps on LinkedIn Ads and Display Ads to prevent runaway CPCs while improving lead lead-nurturing workflows."
    )

    return insights

def print_insights_report(df):
    insights = generate_automated_insights(df)
    print("=" * 70)
    print("      DYNAMIC AUTOMATED MARKETING BUSINESS INSIGHTS REPORT")
    print("=" * 70)
    
    for section_name, items in insights.items():
        print(f"\n--- {section_name.replace('_', ' ').upper()} ---")
        for item in items:
            print(f"• {item}")
    print("=" * 70)

if __name__ == "__main__":
    df_clean = pd.read_csv("data/cleaned_marketing_data.csv")
    print_insights_report(df_clean)

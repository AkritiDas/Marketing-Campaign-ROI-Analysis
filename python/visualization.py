import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure both workspace root and python folder are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from python.campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance
except ImportError:
    from campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance





# Set high visual quality styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

PRIMARY_COLOR = '#1E88E5'    # Vibrant Blue
SECONDARY_COLOR = '#43A047'  # Emerald Green
ACCENT_COLOR = '#E53935'     # Coral Red
NEUTRAL_DARK = '#263238'     # Dark Slate
PALETTE = sns.color_palette("muted")

def format_currency(val, pos=None):
    if val >= 1e6:
        return f"${val*1e-6:.1f}M"
    elif val >= 1e3:
        return f"${val*1e-3:.0f}K"
    else:
        return f"${val:.0f}"

def generate_all_charts(df, output_dir="charts"):
    """
    Generates 12 professional marketing charts and saves them into the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    ch_df = analyze_channel_performance(df)
    cmp_df = analyze_campaign_performance(df)
    mo_df = analyze_monthly_performance(df)

    # -------------------------------------------------------------
    # 1. Revenue by Marketing Channel
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(ch_df['Marketing_Channel'], ch_df['Revenue'] / 1e6, color='#1565C0', width=0.6, edgecolor='none')
    ax.set_title('Total Revenue by Marketing Channel ($ Millions)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Revenue ($ Millions)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_xticklabels(ch_df['Marketing_Channel'], rotation=30, ha='right')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:.2f}M',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_revenue_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 2. Advertising Spend by Channel
    # -------------------------------------------------------------
    ch_spend = ch_df.sort_values(by='Ad_Spend', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(ch_spend['Marketing_Channel'], ch_spend['Ad_Spend'] / 1e3, color='#D84315', width=0.6)
    ax.set_title('Total Advertising Spend by Marketing Channel ($ Thousands)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Ad Spend ($ Thousands)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_xticklabels(ch_spend['Marketing_Channel'], rotation=30, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:.0f}K',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_spend_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 3. ROAS by Channel
    # -------------------------------------------------------------
    ch_roas = ch_df.sort_values(by='ROAS (x)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.barh(ch_roas['Marketing_Channel'], ch_roas['ROAS (x)'], color='#2E7D32', height=0.6)
    ax.set_title('Return on Ad Spend (ROAS) by Marketing Channel', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('ROAS (x Ratio)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.invert_yaxis()

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:.1f}x',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_roas_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 4. Customer Acquisition Cost (CAC) by Channel
    # -------------------------------------------------------------
    ch_cac = ch_df.sort_values(by='CAC ($)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(ch_cac['Marketing_Channel'], ch_cac['CAC ($)'], color='#C62828', width=0.6)
    ax.set_title('Customer Acquisition Cost (CAC) by Marketing Channel ($)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('CAC ($)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_xticklabels(ch_cac['Marketing_Channel'], rotation=30, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_cac_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 5. Conversion Rate by Channel
    # -------------------------------------------------------------
    ch_cr = ch_df.sort_values(by='Conversion_Rate (%)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(ch_cr['Marketing_Channel'], ch_cr['Conversion_Rate (%)'], color='#6A1B9A', width=0.6)
    ax.set_title('Conversion Rate by Marketing Channel (%)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Conversion Rate (%)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_xticklabels(ch_cr['Marketing_Channel'], rotation=30, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_conversion_rate_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 6. ROI by Channel
    # -------------------------------------------------------------
    ch_roi = ch_df.sort_values(by='ROI (%)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(ch_roi['Marketing_Channel'], ch_roi['ROI (%)'], color='#00838F', width=0.6)
    ax.set_title('Return on Investment (ROI) by Marketing Channel (%)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Marketing Channel', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('ROI (%)', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_xticklabels(ch_roi['Marketing_Channel'], rotation=30, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=NEUTRAL_DARK)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '6_roi_by_channel.png'))
    plt.close()

    # -------------------------------------------------------------
    # 7. Monthly Revenue Trend
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    ax.plot(mo_df['Year_Month'], mo_df['Revenue'] / 1e6, marker='o', linewidth=2.5, color='#1B5E20', label='Monthly Revenue')
    ax.set_title('Monthly Revenue Trend (2025)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Month', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Revenue ($ Millions)', fontsize=11, fontweight='bold', labelpad=10)
    plt.xticks(rotation=45)
    
    for i, txt in enumerate(mo_df['Revenue'] / 1e6):
        ax.annotate(f'${txt:.2f}M', (mo_df['Year_Month'][i], txt), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '7_monthly_revenue_trend.png'))
    plt.close()

    # -------------------------------------------------------------
    # 8. Monthly Spend Trend
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    ax.plot(mo_df['Year_Month'], mo_df['Ad_Spend'] / 1e3, marker='s', linewidth=2.5, color='#B71C1C', label='Monthly Spend')
    ax.set_title('Monthly Advertising Spend Trend (2025)', fontsize=14, fontweight='bold', pad=15, color=NEUTRAL_DARK)
    ax.set_xlabel('Month', fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel('Ad Spend ($ Thousands)', fontsize=11, fontweight='bold', labelpad=10)
    plt.xticks(rotation=45)

    for i, txt in enumerate(mo_df['Ad_Spend'] / 1e3):
        ax.annotate(f'${txt:.0f}K', (mo_df['Year_Month'][i], txt), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '8_monthly_spend_trend.png'))
    plt.close()

    # -------------------------------------------------------------
    # 9. Campaign Performance Comparison (Revenue & Spend Top 10)
    # -------------------------------------------------------------
    top10_cmp = cmp_df.head(10)
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    x = np.arange(len(top10_cmp))
    width = 0.35

    ax.bar(x - width/2, top10_cmp['Revenue'] / 1e6, width, label='Revenue ($M)', color='#1E88E5')
    ax.bar(x + width/2, top10_cmp['Ad_Spend'] / 1e6, width, label='Ad Spend ($M)', color='#FF7043')

    ax.set_title('Top 10 Campaigns: Revenue vs. Advertising Spend ($ Millions)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(top10_cmp['Campaign_Name'], rotation=40, ha='right', fontsize=9)
    ax.set_ylabel('Amount ($ Millions)', fontsize=11, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '9_campaign_performance_comparison.png'))
    plt.close()

    # -------------------------------------------------------------
    # 10. Revenue vs Ad Spend (Scatter Plot with Regression line)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.regplot(data=df, x='Ad_Spend', y='Revenue', ax=ax,
                scatter_kws={'alpha':0.4, 'color':'#0288D1', 's':25},
                line_kws={'color':'#D32F2F', 'linewidth':2, 'label':'Linear Trendline'})
    ax.set_title('Campaign Record Level: Revenue vs. Advertising Spend', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Ad Spend ($)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '10_revenue_vs_ad_spend.png'))
    plt.close()

    # -------------------------------------------------------------
    # 11. Conversion Rate vs CAC by Campaign
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.scatterplot(data=cmp_df, x='CAC ($)', y='Conversion_Rate (%)', hue='Marketing_Channel', s=120, palette='Set2', ax=ax)
    
    avg_cac = cmp_df['CAC ($)'].mean()
    avg_cr = cmp_df['Conversion_Rate (%)'].mean()
    ax.axvline(avg_cac, color='gray', linestyle='--', alpha=0.7)
    ax.axhline(avg_cr, color='gray', linestyle='--', alpha=0.7)
    
    ax.set_title('Campaign Efficiency Matrix: Conversion Rate vs. CAC', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('CAC ($)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Conversion Rate (%)', fontsize=11, fontweight='bold')
    ax.legend(title='Channel', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Annotate quadrants
    ax.text(avg_cac*0.3, avg_cr*1.4, 'HIGH CR / LOW CAC\n(Optimal Scale)', fontsize=9, fontweight='bold', color='green', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", lw=1))
    ax.text(avg_cac*1.2, avg_cr*0.5, 'LOW CR / HIGH CAC\n(Needs Audit)', fontsize=9, fontweight='bold', color='red', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '11_conversion_rate_vs_cac.png'))
    plt.close()

    # -------------------------------------------------------------
    # 12. ROAS Comparison Across Campaigns (Top & Bottom)
    # -------------------------------------------------------------
    cmp_roas_sorted = cmp_df.sort_values(by='ROAS (x)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.barh(cmp_roas_sorted['Campaign_Name'], cmp_roas_sorted['ROAS (x)'], color='#388E3C', height=0.6)
    ax.set_title('ROAS Across All Campaigns', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('ROAS (x Ratio)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Campaign Name', fontsize=11, fontweight='bold')
    ax.invert_yaxis()

    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:.1f}x',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(4, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '12_roas_campaign_comparison.png'))
    plt.close()

    print(f"All 12 charts successfully generated and saved to '{output_dir}/'.")

if __name__ == "__main__":
    df_clean = pd.read_csv("data/cleaned_marketing_data.csv")
    generate_all_charts(df_clean)

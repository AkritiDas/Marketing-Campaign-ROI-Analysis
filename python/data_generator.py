import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_marketing_data(num_records=3000, random_seed=42):
    """
    Generates a realistic raw marketing campaign dataset.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)

    channels = [
        "Google Ads", "Facebook Ads", "Instagram Ads", "LinkedIn Ads",
        "YouTube Ads", "Email Marketing", "SEO", "Display Ads"
    ]
    
    # Inconsistent variations for raw data cleaning demonstration
    channel_raw_variations = {
        "Google Ads": ["Google Ads", "google ads", "Google Ads ", "GOOGLE ADS"],
        "Facebook Ads": ["Facebook Ads", "facebook ads", " Facebook Ads"],
        "Instagram Ads": ["Instagram Ads", "instagram ads", "Instagram_Ads"],
        "LinkedIn Ads": ["LinkedIn Ads", "linkedin ads", "LinkedIn Ads "],
        "YouTube Ads": ["YouTube Ads", "youtube ads", "YouTube_Ads"],
        "Email Marketing": ["Email Marketing", "email marketing", "Email Marketing "],
        "SEO": ["SEO", "seo", " SEO "],
        "Display Ads": ["Display Ads", "display ads", "Display Ads"]
    }

    campaign_types = ["Awareness", "Lead Generation", "Conversion", "Retargeting", "Product Promotion"]
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"]
    device_types = ["Desktop", "Mobile", "Tablet"]

    campaign_pool = [
        ("CMP_GGL_01", "Google_Search_Brand", "Google Ads", "Conversion"),
        ("CMP_GGL_02", "Google_NonBrand_Generic", "Google Ads", "Lead Generation"),
        ("CMP_FB_01", "FB_Retargeting_Q1", "Facebook Ads", "Retargeting"),
        ("CMP_FB_02", "FB_Lookalike_Prospecting", "Facebook Ads", "Awareness"),
        ("CMP_IG_01", "IG_Influencer_Promos", "Instagram Ads", "Product Promotion"),
        ("CMP_IG_02", "IG_Stories_Conversion", "Instagram Ads", "Conversion"),
        ("CMP_LI_01", "LI_B2B_Executive_Leads", "LinkedIn Ads", "Lead Generation"),
        ("CMP_LI_02", "LI_Whitepaper_Downloads", "LinkedIn Ads", "Lead Generation"),
        ("CMP_YT_01", "YT_Video_Awareness_V1", "YouTube Ads", "Awareness"),
        ("CMP_YT_02", "YT_TrueView_Product_Demo", "YouTube Ads", "Product Promotion"),
        ("CMP_EM_01", "EM_Weekly_Newsletter", "Email Marketing", "Product Promotion"),
        ("CMP_EM_02", "EM_Abandoned_Cart_Nurture", "Email Marketing", "Conversion"),
        ("CMP_SEO_01", "SEO_Organic_Blog_Content", "SEO", "Awareness"),
        ("CMP_SEO_02", "SEO_High_Intent_Landing", "SEO", "Conversion"),
        ("CMP_DSP_01", "DSP_Programmatic_Banner", "Display Ads", "Awareness"),
        ("CMP_DSP_02", "DSP_Dynamic_Retargeting", "Display Ads", "Retargeting")
    ]

    start_date = datetime(2025, 1, 1)
    
    data = []

    for i in range(num_records):
        cmp_id, cmp_name, main_channel, cmp_type = random.choice(campaign_pool)
        
        # Select raw variation of channel name
        raw_channel = random.choice(channel_raw_variations[main_channel])
        region = random.choice(regions)
        device = random.choice(device_types)
        
        # Random date within 2025
        days_offset = random.randint(0, 364)
        rec_date = start_date + timedelta(days=days_offset)
        
        # String date formats with slight variation
        if random.random() < 0.15:
            date_str = rec_date.strftime("%Y/%m/%d")
        else:
            date_str = rec_date.strftime("%Y-%m-%d")
            
        duration = random.randint(7, 30)

        # Baseline stats per channel to reflect realistic ROI behavior
        if main_channel == "Google Ads":
            impressions = random.randint(10000, 50000)
            ctr = random.uniform(0.035, 0.065)
            cpc = random.uniform(2.5, 4.5)
            conv_rate = random.uniform(0.08, 0.14)
            val_per_conv = random.uniform(220, 350)
            cust_ratio = random.uniform(0.6, 0.85)

        elif main_channel == "Facebook Ads":
            impressions = random.randint(15000, 65000)
            ctr = random.uniform(0.025, 0.050)
            cpc = random.uniform(1.5, 3.2)
            conv_rate = random.uniform(0.06, 0.11)
            val_per_conv = random.uniform(180, 280)
            cust_ratio = random.uniform(0.55, 0.75)

        elif main_channel == "Instagram Ads":
            impressions = random.randint(12000, 55000)
            ctr = random.uniform(0.030, 0.055)
            cpc = random.uniform(1.8, 3.5)
            conv_rate = random.uniform(0.05, 0.10)
            val_per_conv = random.uniform(160, 260)
            cust_ratio = random.uniform(0.50, 0.70)

        elif main_channel == "LinkedIn Ads":
            impressions = random.randint(5000, 25000)
            ctr = random.uniform(0.015, 0.035)
            cpc = random.uniform(6.0, 11.0)
            conv_rate = random.uniform(0.07, 0.13)
            val_per_conv = random.uniform(450, 750)
            cust_ratio = random.uniform(0.40, 0.65)

        elif main_channel == "YouTube Ads":
            impressions = random.randint(25000, 90000)
            ctr = random.uniform(0.010, 0.025)
            cpc = random.uniform(1.2, 2.5)
            conv_rate = random.uniform(0.03, 0.07)
            val_per_conv = random.uniform(150, 250)
            cust_ratio = random.uniform(0.45, 0.65)

        elif main_channel == "Email Marketing":
            impressions = random.randint(8000, 30000)
            ctr = random.uniform(0.08, 0.15)
            cpc = random.uniform(0.3, 0.8) # low direct ad cost
            conv_rate = random.uniform(0.12, 0.22)
            val_per_conv = random.uniform(200, 380)
            cust_ratio = random.uniform(0.70, 0.90)

        elif main_channel == "SEO":
            impressions = random.randint(15000, 70000)
            ctr = random.uniform(0.040, 0.080)
            cpc = random.uniform(0.2, 0.6) # low direct cost
            conv_rate = random.uniform(0.09, 0.16)
            val_per_conv = random.uniform(250, 420)
            cust_ratio = random.uniform(0.65, 0.85)

        else:  # Display Ads
            impressions = random.randint(20000, 100000)
            ctr = random.uniform(0.005, 0.018)
            cpc = random.uniform(1.8, 3.8)
            conv_rate = random.uniform(0.015, 0.04)
            val_per_conv = random.uniform(110, 190)
            cust_ratio = random.uniform(0.35, 0.55)

        clicks = max(10, int(impressions * ctr))
        ad_spend = round(clicks * cpc, 2)
        leads = max(2, int(clicks * random.uniform(0.25, 0.55)))
        conversions = max(1, int(clicks * conv_rate))
        revenue = round(conversions * val_per_conv, 2)
        customers = max(1, int(conversions * cust_ratio))

        # Intentionally introduce missing values for data cleaning testing
        dev_val = device if random.random() > 0.02 else np.nan
        dur_val = duration if random.random() > 0.015 else np.nan
        leads_val = leads if random.random() > 0.015 else np.nan

        data.append({
            "Campaign_ID": cmp_id,
            "Campaign_Name": cmp_name,
            "Date": date_str,
            "Marketing_Channel": raw_channel,
            "Campaign_Type": cmp_type,
            "Region": region,
            "Impressions": impressions,
            "Clicks": clicks,
            "Leads": leads_val,
            "Conversions": conversions,
            "Ad_Spend": ad_spend,
            "Revenue": revenue,
            "Customers": customers,
            "Campaign_Duration": dur_val,
            "Device_Type": dev_val
        })

    df = pd.DataFrame(data)

    # Append 20 duplicate rows to demonstrate duplicate removal in cleaning
    duplicates = df.iloc[:20].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle dataframe
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df_raw = generate_marketing_data(num_records=3000)
    output_path = "data/raw_marketing_data.csv"
    df_raw.to_csv(output_path, index=False)
    print(f"Generated raw dataset with {len(df_raw)} records at '{output_path}'.")

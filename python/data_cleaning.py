import pandas as pd
import numpy as np
import os

def clean_marketing_data(input_csv="data/raw_marketing_data.csv", output_csv="data/cleaned_marketing_data.csv"):
    """
    Cleans the raw marketing campaign dataset and saves the cleaned dataset.
    
    Steps:
    1. Load raw dataset
    2. Inspect dataset (shape, missing values, duplicates)
    3. Remove duplicate records
    4. Standardize text fields (Marketing_Channel, Campaign_Name, etc.)
    5. Convert Date column to standard datetime format (YYYY-MM-DD)
    6. Handle missing values appropriately
    7. Ensure non-negative numerical data and correct data types
    8. Save cleaned dataset
    """
    print("--- STEP 2: DATA CLEANING ---")
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file '{input_csv}' not found.")
        
    df = pd.read_csv(input_csv)
    initial_shape = df.shape
    print(f"Initial raw dataset shape: {initial_shape[0]} rows, {initial_shape[1]} columns")

    # 1. Identify Duplicates
    dup_count = df.duplicated().sum()
    print(f"Duplicate records found: {dup_count}")
    if dup_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Removed duplicates. New shape: {df.shape[0]} rows")

    # 2. Standardize Channel Names & Whitespace
    df['Marketing_Channel'] = df['Marketing_Channel'].astype(str).str.strip()
    
    # Mapping dictionary to unify variations
    channel_mapping = {
        'google ads': 'Google Ads',
        'GOOGLE ADS': 'Google Ads',
        'Google Ads': 'Google Ads',
        'facebook ads': 'Facebook Ads',
        'Facebook Ads': 'Facebook Ads',
        'instagram ads': 'Instagram Ads',
        'Instagram_Ads': 'Instagram Ads',
        'Instagram Ads': 'Instagram Ads',
        'linkedin ads': 'LinkedIn Ads',
        'LinkedIn Ads': 'LinkedIn Ads',
        'youtube ads': 'YouTube Ads',
        'YouTube_Ads': 'YouTube Ads',
        'YouTube Ads': 'YouTube Ads',
        'email marketing': 'Email Marketing',
        'Email Marketing': 'Email Marketing',
        'seo': 'SEO',
        'SEO': 'SEO',
        'display ads': 'Display Ads',
        'Display Ads': 'Display Ads'
    }
    
    # Apply mapping dynamically (fall back to title case if not in mapping)
    df['Marketing_Channel'] = df['Marketing_Channel'].map(lambda x: channel_mapping.get(x, channel_mapping.get(x.lower(), x.title())))

    # Standardize string fields
    df['Campaign_Name'] = df['Campaign_Name'].astype(str).str.strip()
    df['Campaign_Type'] = df['Campaign_Type'].astype(str).str.strip()
    df['Region'] = df['Region'].astype(str).str.strip()

    # 3. Convert Date Column
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    missing_dates = df['Date'].isna().sum()
    if missing_dates > 0:
        df['Date'] = df['Date'].fillna(method='ffill')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    # 4. Handle Missing Values
    print("\nMissing values before imputation:")
    print(df.isna().sum()[df.isna().sum() > 0])

    # Fill missing Device_Type with Mode
    if 'Device_Type' in df.columns and df['Device_Type'].isna().sum() > 0:
        mode_device = df['Device_Type'].mode()[0] if not df['Device_Type'].mode().empty else 'Desktop'
        df['Device_Type'] = df['Device_Type'].fillna(mode_device)

    # Fill missing Campaign_Duration with Median
    if 'Campaign_Duration' in df.columns and df['Campaign_Duration'].isna().sum() > 0:
        median_dur = df['Campaign_Duration'].median()
        df['Campaign_Duration'] = df['Campaign_Duration'].fillna(median_dur)

    # Fill missing Leads using Clicks * estimated lead rate per channel
    if 'Leads' in df.columns and df['Leads'].isna().sum() > 0:
        avg_lead_rate = (df['Leads'] / df['Clicks']).median()
        df['Leads'] = df['Leads'].fillna(np.round(df['Clicks'] * avg_lead_rate))

    # 5. Type Casting & Sanity Checks
    integer_cols = ['Impressions', 'Clicks', 'Leads', 'Conversions', 'Customers', 'Campaign_Duration']
    for col in integer_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)

    float_cols = ['Ad_Spend', 'Revenue']
    for col in float_cols:
        if col in df.columns:
            df[col] = df[col].round(2)

    # Sanity checks: Clicks <= Impressions, Conversions <= Clicks
    df['Clicks'] = np.minimum(df['Clicks'], df['Impressions'])
    df['Conversions'] = np.minimum(df['Conversions'], df['Clicks'])
    df['Customers'] = np.minimum(df['Customers'], df['Conversions'])

    # 6. Sort by Date
    df = df.sort_values(by=['Date', 'Campaign_ID']).reset_index(drop=True)

    print("\nMissing values after cleaning:")
    print(df.isna().sum().sum())

    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"\nCleaned dataset saved successfully to '{output_csv}' with {df.shape[0]} rows and {df.shape[1]} columns.")
    
    return df

if __name__ == "__main__":
    df_clean = clean_marketing_data()

import os
import sys

# Add current workspace root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from python.data_generator import generate_marketing_data
from python.data_cleaning import clean_marketing_data
from python.kpi_calculation import calculate_row_kpis, calculate_summary_kpis
from python.campaign_analysis import (
    analyze_channel_performance,
    analyze_campaign_performance,
    analyze_monthly_performance
)
from python.visualization import generate_all_charts
from python.insights import print_insights_report
from python.generate_excel import create_excel_workbook
from python.generate_pdf_report import generate_pdf_report
from python.generate_notebook import create_jupyter_notebook


def run_full_pipeline():
    print("=" * 70)
    print("MARKETING CAMPAIGN ROI ANALYSIS -- FULL PIPELINE EXECUTION")
    print("=" * 70)

    # Step 1: Generate Data
    print("\n[Step 1/9] Generating Raw Marketing Dataset...")
    df_raw = generate_marketing_data(num_records=3000)
    df_raw.to_csv("data/raw_marketing_data.csv", index=False)

    # Step 2: Clean Data
    print("\n[Step 2/9] Cleaning & Standardizing Dataset...")
    df_clean = clean_marketing_data("data/raw_marketing_data.csv", "data/cleaned_marketing_data.csv")

    # Step 3: Calculate KPIs
    print("\n[Step 3/9] Calculating Marketing KPIs...")
    df_kpi = calculate_row_kpis(df_clean)
    summary = calculate_summary_kpis(df_clean)

    # Step 4: Perform Analysis
    print("\n[Step 4/9] Performing Channel, Campaign & Time-Series Aggregations...")
    ch_df = analyze_channel_performance(df_clean)
    cmp_df = analyze_campaign_performance(df_clean)
    mo_df = analyze_monthly_performance(df_clean)

    # Step 5: Visualizations
    print("\n[Step 5/9] Rendering 12 Professional Charts...")
    generate_all_charts(df_clean, output_dir="charts")

    # Step 6: Automated Insights
    print("\n[Step 6/9] Generating Automated Dynamic Business Insights...")
    print_insights_report(df_clean)

    # Step 7: Interactive Excel Workbook
    print("\n[Step 7/9] Generating 7-Sheet Excel Workbook with Formulas & Dashboard...")
    create_excel_workbook()

    # Step 8: Executive PDF Business Report
    print("\n[Step 8/9] Generating PDF Executive Business Report...")
    generate_pdf_report()

    # Step 9: Jupyter Notebook
    print("\n[Step 9/9] Generating Portfolio Jupyter Notebook...")
    create_jupyter_notebook()

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY! ALL DELIVERABLES READY.")
    print("=" * 70)


if __name__ == "__main__":
    run_full_pipeline()

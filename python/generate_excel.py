import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
import os

def create_excel_workbook(raw_path="data/raw_marketing_data.csv", cleaned_path="data/cleaned_marketing_data.csv", output_xlsx="excel/Marketing_Campaign_ROI_Analysis.xlsx"):
    """
    Generates a complete 7-sheet interactive Excel workbook for Marketing Campaign ROI Analysis.
    """
    print("--- STEP 8: EXCEL WORKBOOK GENERATION ---")
    os.makedirs(os.path.dirname(output_xlsx), exist_ok=True)

    df_raw = pd.read_csv(raw_path)
    df_clean = pd.read_csv(cleaned_path)

    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Remove default sheet

    # Theme colors
    HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Dark Navy
    HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    CARD_FILL = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    BORDER_THIN = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC')
    )

    # -------------------------------------------------------------
    # SHEET 1: Raw Data
    # -------------------------------------------------------------
    ws_raw = wb.create_sheet(title="Raw Data")
    ws_raw.views.sheetView[0].showGridLines = True
    
    ws_raw.append(list(df_raw.columns))
    for r in df_raw.itertuples(index=False):
        ws_raw.append(list(r))

    for col_idx in range(1, len(df_raw.columns) + 1):
        cell = ws_raw.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # -------------------------------------------------------------
    # SHEET 2: Cleaned Data
    # -------------------------------------------------------------
    ws_clean = wb.create_sheet(title="Cleaned Data")
    ws_clean.views.sheetView[0].showGridLines = True
    
    ws_clean.append(list(df_clean.columns))
    for r in df_clean.itertuples(index=False):
        ws_clean.append(list(r))

    for col_idx in range(1, len(df_clean.columns) + 1):
        cell = ws_clean.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # -------------------------------------------------------------
    # SHEET 3: KPI Calculation (Using Excel Formulas)
    # -------------------------------------------------------------
    ws_kpi = wb.create_sheet(title="KPI Calculation")
    ws_kpi.views.sheetView[0].showGridLines = True
    
    kpi_cols = list(df_clean.columns) + ["CTR (%)", "Conversion Rate (%)", "CPC ($)", "CPL ($)", "CAC ($)", "ROAS (x)", "ROI (%)"]
    ws_kpi.append(kpi_cols)

    for row_idx, r in enumerate(df_clean.itertuples(index=False), start=2):
        row_data = list(r)
        # Excel Formulas
        # G: Impressions, H: Clicks, I: Leads, J: Conversions, K: Ad_Spend, L: Revenue, M: Customers
        ctr_formula = f"=IFERROR(H{row_idx}/G{row_idx}*100, 0)"
        cr_formula = f"=IFERROR(J{row_idx}/H{row_idx}*100, 0)"
        cpc_formula = f"=IFERROR(K{row_idx}/H{row_idx}, 0)"
        cpl_formula = f"=IFERROR(K{row_idx}/I{row_idx}, 0)"
        cac_formula = f"=IFERROR(K{row_idx}/M{row_idx}, 0)"
        roas_formula = f"=IFERROR(L{row_idx}/K{row_idx}, 0)"
        roi_formula = f"=IFERROR((L{row_idx}-K{row_idx})/K{row_idx}*100, 0)"

        row_data.extend([ctr_formula, cr_formula, cpc_formula, cpl_formula, cac_formula, roas_formula, roi_formula])
        ws_kpi.append(row_data)

    for col_idx in range(1, len(kpi_cols) + 1):
        cell = ws_kpi.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx in range(2, len(df_clean) + 2):
        ws_kpi.cell(row=r_idx, column=11).number_format = '"$"#,##0.00'
        ws_kpi.cell(row=r_idx, column=12).number_format = '"$"#,##0.00'
        ws_kpi.cell(row=r_idx, column=16).number_format = '0.00"%"'
        ws_kpi.cell(row=r_idx, column=17).number_format = '0.00"%"'
        ws_kpi.cell(row=r_idx, column=18).number_format = '"$"#,##0.00'
        ws_kpi.cell(row=r_idx, column=19).number_format = '"$"#,##0.00'
        ws_kpi.cell(row=r_idx, column=20).number_format = '"$"#,##0.00'
        ws_kpi.cell(row=r_idx, column=21).number_format = '0.00"x"'
        ws_kpi.cell(row=r_idx, column=22).number_format = '0.00"%"'

    # -------------------------------------------------------------
    # SHEET 4: Channel Analysis
    # -------------------------------------------------------------
    ws_ch = wb.create_sheet(title="Channel Analysis")
    ws_ch.views.sheetView[0].showGridLines = True
    
    ch_headers = [
        "Marketing Channel", "Total Impressions", "Total Clicks", "Total Leads",
        "Total Conversions", "Total Customers", "Total Ad Spend", "Total Revenue",
        "CTR (%)", "Conversion Rate (%)", "CPC ($)", "CPL ($)", "CAC ($)", "ROAS (x)", "ROI (%)"
    ]
    ws_ch.append(ch_headers)

    channels = sorted(df_clean['Marketing_Channel'].unique())

    for idx, ch in enumerate(channels, start=2):
        imp_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$G:$G)"
        clk_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$H:$H)"
        led_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$I:$I)"
        cnv_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$J:$J)"
        cst_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$M:$M)"
        spd_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$K:$K)"
        rev_f = f"=SUMIF('Cleaned Data'!$D:$D, A{idx}, 'Cleaned Data'!$L:$L)"
        
        ctr_f = f"=IFERROR(C{idx}/B{idx}*100, 0)"
        cr_f = f"=IFERROR(E{idx}/C{idx}*100, 0)"
        cpc_f = f"=IFERROR(G{idx}/C{idx}, 0)"
        cpl_f = f"=IFERROR(G{idx}/D{idx}, 0)"
        cac_f = f"=IFERROR(G{idx}/F{idx}, 0)"
        roas_f = f"=IFERROR(H{idx}/G{idx}, 0)"
        roi_f = f"=IFERROR((H{idx}-G{idx})/G{idx}*100, 0)"

        ws_ch.append([ch, imp_f, clk_f, led_f, cnv_f, cst_f, spd_f, rev_f, ctr_f, cr_f, cpc_f, cpl_f, cac_f, roas_f, roi_f])

    for col_idx in range(1, len(ch_headers) + 1):
        cell = ws_ch.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx in range(2, len(channels) + 2):
        ws_ch.cell(row=r_idx, column=2).number_format = '#,##0'
        ws_ch.cell(row=r_idx, column=3).number_format = '#,##0'
        ws_ch.cell(row=r_idx, column=4).number_format = '#,##0'
        ws_ch.cell(row=r_idx, column=5).number_format = '#,##0'
        ws_ch.cell(row=r_idx, column=6).number_format = '#,##0'
        ws_ch.cell(row=r_idx, column=7).number_format = '"$"#,##0.00'
        ws_ch.cell(row=r_idx, column=8).number_format = '"$"#,##0.00'
        ws_ch.cell(row=r_idx, column=9).number_format = '0.00"%"'
        ws_ch.cell(row=r_idx, column=10).number_format = '0.00"%"'
        ws_ch.cell(row=r_idx, column=11).number_format = '"$"#,##0.00'
        ws_ch.cell(row=r_idx, column=12).number_format = '"$"#,##0.00'
        ws_ch.cell(row=r_idx, column=13).number_format = '"$"#,##0.00'
        ws_ch.cell(row=r_idx, column=14).number_format = '0.00"x"'
        ws_ch.cell(row=r_idx, column=15).number_format = '0.00"%"'

    # -------------------------------------------------------------
    # SHEET 5: Campaign Analysis
    # -------------------------------------------------------------
    ws_cmp = wb.create_sheet(title="Campaign Analysis")
    ws_cmp.views.sheetView[0].showGridLines = True
    
    cmp_headers = [
        "Campaign Name", "Channel", "Total Spend", "Total Revenue", "Total Conversions",
        "Total Customers", "Conversion Rate (%)", "CAC ($)", "ROAS (x)", "ROI (%)"
    ]
    ws_cmp.append(cmp_headers)

    campaign_df = df_clean[['Campaign_Name', 'Marketing_Channel']].drop_duplicates().sort_values(by='Campaign_Name')
    
    for idx, r in enumerate(campaign_df.itertuples(index=False), start=2):
        c_name, c_chan = r.Campaign_Name, r.Marketing_Channel
        spd_f = f"=SUMIF('Cleaned Data'!$B:$B, A{idx}, 'Cleaned Data'!$K:$K)"
        rev_f = f"=SUMIF('Cleaned Data'!$B:$B, A{idx}, 'Cleaned Data'!$L:$L)"
        cnv_f = f"=SUMIF('Cleaned Data'!$B:$B, A{idx}, 'Cleaned Data'!$J:$J)"
        cst_f = f"=SUMIF('Cleaned Data'!$B:$B, A{idx}, 'Cleaned Data'!$M:$M)"
        clk_f = f"SUMIF('Cleaned Data'!$B:$B, A{idx}, 'Cleaned Data'!$H:$H)"
        
        cr_f = f"=IFERROR(E{idx}/{clk_f}*100, 0)"
        cac_f = f"=IFERROR(C{idx}/F{idx}, 0)"
        roas_f = f"=IFERROR(D{idx}/C{idx}, 0)"
        roi_f = f"=IFERROR((D{idx}-C{idx})/C{idx}*100, 0)"

        ws_cmp.append([c_name, c_chan, spd_f, rev_f, cnv_f, cst_f, cr_f, cac_f, roas_f, roi_f])

    for col_idx in range(1, len(cmp_headers) + 1):
        cell = ws_cmp.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx in range(2, len(campaign_df) + 2):
        ws_cmp.cell(row=r_idx, column=3).number_format = '"$"#,##0.00'
        ws_cmp.cell(row=r_idx, column=4).number_format = '"$"#,##0.00'
        ws_cmp.cell(row=r_idx, column=5).number_format = '#,##0'
        ws_cmp.cell(row=r_idx, column=6).number_format = '#,##0'
        ws_cmp.cell(row=r_idx, column=7).number_format = '0.00"%"'
        ws_cmp.cell(row=r_idx, column=8).number_format = '"$"#,##0.00'
        ws_cmp.cell(row=r_idx, column=9).number_format = '0.00"x"'
        ws_cmp.cell(row=r_idx, column=10).number_format = '0.00"%"'

    # -------------------------------------------------------------
    # SHEET 6: Monthly Analysis
    # -------------------------------------------------------------
    ws_mo = wb.create_sheet(title="Monthly Analysis")
    ws_mo.views.sheetView[0].showGridLines = True
    
    mo_headers = [
        "Year-Month", "Monthly Spend", "Monthly Revenue", "Conversions",
        "Customers", "Conversion Rate (%)", "CAC ($)", "ROAS (x)", "ROI (%)"
    ]
    ws_mo.append(mo_headers)

    df_clean['YM'] = pd.to_datetime(df_clean['Date']).dt.to_period('M').astype(str)
    months = sorted(df_clean['YM'].unique())

    for idx, ym in enumerate(months, start=2):
        spd_f = f"=SUMIFS('Cleaned Data'!$K:$K, 'Cleaned Data'!$C:$C, \">={ym}-01\", 'Cleaned Data'!$C:$C, \"<={ym}-31\")"
        rev_f = f"=SUMIFS('Cleaned Data'!$L:$L, 'Cleaned Data'!$C:$C, \">={ym}-01\", 'Cleaned Data'!$C:$C, \"<={ym}-31\")"
        cnv_f = f"=SUMIFS('Cleaned Data'!$J:$J, 'Cleaned Data'!$C:$C, \">={ym}-01\", 'Cleaned Data'!$C:$C, \"<={ym}-31\")"
        cst_f = f"=SUMIFS('Cleaned Data'!$M:$M, 'Cleaned Data'!$C:$C, \">={ym}-01\", 'Cleaned Data'!$C:$C, \"<={ym}-31\")"
        clk_f = f"SUMIFS('Cleaned Data'!$H:$H, 'Cleaned Data'!$C:$C, \">={ym}-01\", 'Cleaned Data'!$C:$C, \"<={ym}-31\")"

        cr_f = f"=IFERROR(D{idx}/{clk_f}*100, 0)"
        cac_f = f"=IFERROR(B{idx}/E{idx}, 0)"
        roas_f = f"=IFERROR(C{idx}/B{idx}, 0)"
        roi_f = f"=IFERROR((C{idx}-B{idx})/B{idx}*100, 0)"

        ws_mo.append([ym, spd_f, rev_f, cnv_f, cst_f, cr_f, cac_f, roas_f, roi_f])

    for col_idx in range(1, len(mo_headers) + 1):
        cell = ws_mo.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx in range(2, len(months) + 2):
        ws_mo.cell(row=r_idx, column=2).number_format = '"$"#,##0.00'
        ws_mo.cell(row=r_idx, column=3).number_format = '"$"#,##0.00'
        ws_mo.cell(row=r_idx, column=4).number_format = '#,##0'
        ws_mo.cell(row=r_idx, column=5).number_format = '#,##0'
        ws_mo.cell(row=r_idx, column=6).number_format = '0.00"%"'
        ws_mo.cell(row=r_idx, column=7).number_format = '"$"#,##0.00'
        ws_mo.cell(row=r_idx, column=8).number_format = '0.00"x"'
        ws_mo.cell(row=r_idx, column=9).number_format = '0.00"%"'

    # -------------------------------------------------------------
    # SHEET 7: Executive Dashboard
    # -------------------------------------------------------------
    ws_dash = wb.create_sheet(title="Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("A1:N2")
    title_cell = ws_dash["A1"]
    title_cell.value = "MARKETING CAMPAIGN ROI EXECUTIVE DASHBOARD"
    title_cell.font = Font(name="Calibri", size=18, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="0B2F64", end_color="0B2F64", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    # Filter / Slicer bar banner
    ws_dash.merge_cells("A3:N3")
    filter_cell = ws_dash["A3"]
    filter_cell.value = "Interactive Filters: [Marketing Channel] | [Campaign Type] | [Region] | [Date Range]"
    filter_cell.font = Font(name="Calibri", size=10, italic=True, color="1F4E78")
    filter_cell.fill = PatternFill(start_color="E6EEF8", end_color="E6EEF8", fill_type="solid")
    filter_cell.alignment = Alignment(horizontal="center", vertical="center")

    cards_detail = [
        ("TOTAL AD SPEND", "=SUM('Cleaned Data'!K:K)", '"$"#,##0.00', 5, 2), # B5:C6
        ("TOTAL REVENUE", "=SUM('Cleaned Data'!L:L)", '"$"#,##0.00', 5, 5), # E5:F6
        ("TOTAL CUSTOMERS", "=SUM('Cleaned Data'!M:M)", '#,##0', 5, 8), # H5:I6
        ("TOTAL CONVERSIONS", "=SUM('Cleaned Data'!J:J)", '#,##0', 5, 11), # K5:L6
        ("CONVERSION RATE", "=IFERROR(SUM('Cleaned Data'!J:J)/SUM('Cleaned Data'!H:H)*100,0)", '0.00"%"', 8, 2), # B8:C9
        ("CAC", "=IFERROR(SUM('Cleaned Data'!K:K)/SUM('Cleaned Data'!M:M),0)", '"$"#,##0.00', 8, 5), # E8:F9
        ("ROAS", "=IFERROR(SUM('Cleaned Data'!L:L)/SUM('Cleaned Data'!K:K),0)", '0.00"x"', 8, 8), # H8:I9
        ("PORTFOLIO ROI", "=IFERROR((SUM('Cleaned Data'!L:L)-SUM('Cleaned Data'!K:K))/SUM('Cleaned Data'!K:K)*100,0)", '0.00"%"', 8, 11) # K8:L9
    ]

    for label, formula, fmt, r, c in cards_detail:
        r1, c1 = r, c
        r2, c2 = r + 1, c + 1
        
        # Write values to top-left cells BEFORE merging
        lbl_cell = ws_dash.cell(row=r1, column=c1, value=label)
        val_cell = ws_dash.cell(row=r2, column=c1, value=formula)

        # Now merge cells
        ws_dash.merge_cells(start_row=r1, start_column=c1, end_row=r1, end_column=c2)
        ws_dash.merge_cells(start_row=r2, start_column=c1, end_row=r2, end_column=c2)

        lbl_cell.font = Font(name="Calibri", size=9, bold=True, color="595959")
        lbl_cell.fill = SUBHEADER_FILL
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")

        val_cell.font = Font(name="Calibri", size=16, bold=True, color="1F4E78")
        val_cell.fill = CARD_FILL
        val_cell.number_format = fmt
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Apply borders to card box
        for row in ws_dash.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
            for cell in row:
                cell.border = BORDER_THIN

    # Add Charts to Dashboard Sheet
    # Chart 1: Revenue by Channel (BarChart)
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Revenue by Marketing Channel ($)"
    chart1.y_axis.title = "Revenue ($)"
    chart1.x_axis.title = "Channel"
    
    data_ref1 = Reference(ws_ch, min_col=8, min_row=1, max_row=len(channels)+1)
    cats_ref1 = Reference(ws_ch, min_col=1, min_row=2, max_row=len(channels)+1)
    chart1.add_data(data_ref1, titles_from_data=True)
    chart1.set_categories(cats_ref1)
    chart1.width = 16
    chart1.height = 10
    ws_dash.add_chart(chart1, "B12")

    # Chart 2: ROAS by Channel (BarChart)
    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 11
    chart2.title = "ROAS by Marketing Channel (x)"
    chart2.y_axis.title = "ROAS (x)"
    chart2.x_axis.title = "Channel"
    
    data_ref2 = Reference(ws_ch, min_col=14, min_row=1, max_row=len(channels)+1)
    chart2.add_data(data_ref2, titles_from_data=True)
    chart2.set_categories(cats_ref1)
    chart2.width = 16
    chart2.height = 10
    ws_dash.add_chart(chart2, "H12")

    # Chart 3: Monthly Revenue & Spend Trend (LineChart)
    chart3 = LineChart()
    chart3.title = "Monthly Revenue vs Ad Spend Trend"
    chart3.style = 13
    chart3.y_axis.title = "Amount ($)"
    chart3.x_axis.title = "Month"
    
    data_ref3 = Reference(ws_mo, min_col=2, min_row=1, max_col=3, max_row=len(months)+1)
    cats_ref3 = Reference(ws_mo, min_col=1, min_row=2, max_row=len(months)+1)
    chart3.add_data(data_ref3, titles_from_data=True)
    chart3.set_categories(cats_ref3)
    chart3.width = 22
    chart3.height = 11
    ws_dash.add_chart(chart3, "B26")

    # Adjust Column Widths Across Sheets
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if not val_str.startswith('='):
                    max_len = max(max_len, len(val_str))
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    for col_let in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']:
        ws_dash.column_dimensions[col_let].width = 14

    wb.save(output_xlsx)
    print(f"Excel workbook generated successfully at '{output_xlsx}'.")

if __name__ == "__main__":
    create_excel_workbook()

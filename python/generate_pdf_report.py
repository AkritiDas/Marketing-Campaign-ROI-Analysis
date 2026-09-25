import sys
import os

# Ensure both workspace root and python folder are in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

try:
    from python.kpi_calculation import calculate_summary_kpis
    from python.campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance
    from python.insights import generate_automated_insights
except ImportError:
    from kpi_calculation import calculate_summary_kpis
    from campaign_analysis import analyze_channel_performance, analyze_campaign_performance, analyze_monthly_performance
    from insights import generate_automated_insights




def generate_pdf_report(cleaned_path="data/cleaned_marketing_data.csv", output_pdf="reports/Marketing_Campaign_ROI_Report.pdf"):
    """
    Generates a professional executive PDF business report using ReportLab.
    """
    print("--- STEP 11: PDF REPORT GENERATION ---")
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    df = pd.read_csv(cleaned_path)
    
    summary = calculate_summary_kpis(df)
    ch_df = analyze_channel_performance(df)
    cmp_df = analyze_campaign_performance(df)
    mo_df = analyze_monthly_performance(df)
    insights = generate_automated_insights(df)

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0B2F64"),
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#595959"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1F4E78"),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#262626"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#262626"),
        leftIndent=12,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#262626"),
        alignment=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("Marketing Campaign ROI Analysis", title_style))
    story.append(Paragraph("Executive Performance & Portfolio Business Report | 2025 Annual Review", subtitle_style))
    story.append(Spacer(1, 6))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    exec_summary_text = (
        f"This report presents a quantitative evaluation of marketing campaign performance across {len(ch_df)} major channels "
        f"and {len(cmp_df)} active campaigns during 2025. Across a total portfolio ad spend of <b>${summary['Total_Ad_Spend']:,.2f}</b>, "
        f"the marketing organization generated <b>${summary['Total_Revenue']:,.2f}</b> in revenue, achieving an overall Return on Ad Spend (ROAS) of "
        f"<b>{summary['ROAS (x)']:.2f}x</b> and a Net Portfolio ROI of <b>{summary['ROI (%)']:.2f}%</b>. "
        f"A total of <b>{summary['Total_Customers']:,}</b> new customers were acquired at a portfolio Customer Acquisition Cost (CAC) of <b>${summary['CAC ($)']:.2f}</b>."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 8))

    # 2. Key Performance Indicators (KPI) Summary Table
    story.append(Paragraph("2. Key Performance Indicators (KPI Summary)", h1_style))
    
    kpi_data = [
        [Paragraph("Metric", table_header_style), Paragraph("Total / Average Value", table_header_style), Paragraph("Benchmark / Target", table_header_style)],
        [Paragraph("Total Ad Spend", table_cell_style), Paragraph(f"${summary['Total_Ad_Spend']:,.2f}", table_cell_style), Paragraph("Budget Cap: $8.50M", table_cell_style)],
        [Paragraph("Total Revenue", table_cell_style), Paragraph(f"${summary['Total_Revenue']:,.2f}", table_cell_style), Paragraph("Target: $100.0M+", table_cell_style)],
        [Paragraph("Total Customers Acquired", table_cell_style), Paragraph(f"{summary['Total_Customers']:,}", table_cell_style), Paragraph("Target: 250,000+", table_cell_style)],
        [Paragraph("Portfolio ROAS", table_cell_style), Paragraph(f"{summary['ROAS (x)']:.2f}x", table_cell_style), Paragraph("Target: > 4.00x", table_cell_style)],
        [Paragraph("Net Portfolio ROI", table_cell_style), Paragraph(f"{summary['ROI (%)']:.2f}%", table_cell_style), Paragraph("Target: > 300%", table_cell_style)],
        [Paragraph("Customer Acquisition Cost (CAC)", table_cell_style), Paragraph(f"${summary['CAC ($)']:.2f}", table_cell_style), Paragraph("Target: < $35.00", table_cell_style)],
        [Paragraph("Conversion Rate", table_cell_style), Paragraph(f"{summary['Conversion_Rate (%)']:.2f}%", table_cell_style), Paragraph("Target: > 8.00%", table_cell_style)]
    ]

    t_kpi = Table(kpi_data, colWidths=[2.5*inch, 2.5*inch, 2.3*inch])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F4E78")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 12))

    # 3. Channel Performance Table
    story.append(Paragraph("3. Marketing Channel Performance Breakdown", h1_style))
    
    ch_headers = [
        Paragraph("Channel", table_header_style),
        Paragraph("Ad Spend ($)", table_header_style),
        Paragraph("Revenue ($)", table_header_style),
        Paragraph("Conv Rate (%)", table_header_style),
        Paragraph("CAC ($)", table_header_style),
        Paragraph("ROAS (x)", table_header_style)
    ]
    ch_rows = [ch_headers]

    for idx, r in ch_df.iterrows():
        ch_rows.append([
            Paragraph(r['Marketing_Channel'], table_cell_style),
            Paragraph(f"${r['Ad_Spend']:,.2f}", table_cell_style),
            Paragraph(f"${r['Revenue']:,.2f}", table_cell_style),
            Paragraph(f"{r['Conversion_Rate (%)']:.2f}%", table_cell_style),
            Paragraph(f"${r['CAC ($)']:.2f}", table_cell_style),
            Paragraph(f"{r['ROAS (x)']:.2f}x", table_cell_style),
        ])

    t_ch = Table(ch_rows, colWidths=[1.5*inch, 1.3*inch, 1.5*inch, 1.0*inch, 1.0*inch, 1.0*inch])
    t_ch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F4E78")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ch)
    story.append(Spacer(1, 14))

    # 4. Embedded Visualizations Section
    story.append(Paragraph("4. Key Visualizations", h1_style))
    img1_path = "charts/1_revenue_by_channel.png"
    img3_path = "charts/3_roas_by_channel.png"
    
    if os.path.exists(img1_path) and os.path.exists(img3_path):
        img_table_data = [[
            Image(img1_path, width=3.5*inch, height=2.1*inch),
            Image(img3_path, width=3.5*inch, height=2.1*inch)
        ]]
        t_img = Table(img_table_data, colWidths=[3.6*inch, 3.6*inch])
        t_img.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_img)
    story.append(Spacer(1, 12))

    # 5. Key Findings
    story.append(Paragraph("5. Data-Driven Key Findings", h1_style))
    for highlight in insights["channel_insights"]:
        story.append(Paragraph(f"• {highlight}", bullet_style))
    for cmp_insight in insights["campaign_insights"]:
        story.append(Paragraph(f"• {cmp_insight}", bullet_style))
    story.append(Spacer(1, 10))

    # 6. Strategic Recommendations
    story.append(Paragraph("6. Business Recommendations", h1_style))
    for rec in insights["recommendations"]:
        story.append(Paragraph(f"• {rec}", bullet_style))

    doc.build(story)
    print(f"PDF Executive Business Report generated successfully at '{output_pdf}'.")

if __name__ == "__main__":
    generate_pdf_report()

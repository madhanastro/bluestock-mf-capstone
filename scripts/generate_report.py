"""
generate_report.py
Bluestock Fintech — Final Report Generator
Creates a professional PDF report using ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                                 Table, TableStyle, HRFlowable,
                                 PageBreak, Image)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import KeepTogether
import os

# ── Colors ───────────────────────────────────────────
BLUE_DARK   = HexColor('#1a237e')
BLUE_MID    = HexColor('#1565c0')
BLUE_LIGHT  = HexColor('#e3f2fd')
ACCENT      = HexColor('#ff6f00')
GRAY_LIGHT  = HexColor('#f5f5f5')
GRAY_MID    = HexColor('#9e9e9e')
GREEN       = HexColor('#2e7d32')
RED         = HexColor('#c62828')

OUTPUT_PATH = "reports/Final_Report.pdf"

def build_report():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=1.8*cm,
        leftMargin=1.8*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('CustomTitle',
        fontSize=26, fontName='Helvetica-Bold',
        textColor=white, alignment=TA_CENTER,
        spaceAfter=6)

    subtitle_style = ParagraphStyle('Subtitle',
        fontSize=13, fontName='Helvetica',
        textColor=white, alignment=TA_CENTER,
        spaceAfter=4)

    h1_style = ParagraphStyle('H1',
        fontSize=16, fontName='Helvetica-Bold',
        textColor=BLUE_DARK, spaceBefore=16,
        spaceAfter=8, borderPad=4)

    h2_style = ParagraphStyle('H2',
        fontSize=13, fontName='Helvetica-Bold',
        textColor=BLUE_MID, spaceBefore=10,
        spaceAfter=6)

    body_style = ParagraphStyle('Body',
        fontSize=10, fontName='Helvetica',
        textColor=black, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=6)

    bullet_style = ParagraphStyle('Bullet',
        fontSize=10, fontName='Helvetica',
        textColor=black, leading=16,
        leftIndent=15, spaceAfter=4)

    caption_style = ParagraphStyle('Caption',
        fontSize=8, fontName='Helvetica',
        textColor=GRAY_MID, alignment=TA_CENTER,
        spaceAfter=8)

    story = []

    # ══════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════
    cover_data = [[
        Paragraph("🏢 BLUESTOCK FINTECH", ParagraphStyle('co',
            fontSize=11, fontName='Helvetica',
            textColor=white, alignment=TA_CENTER)),
    ]]
    cover_table = Table(cover_data, colWidths=[17*cm])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 30),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 0.3*cm))

    title_data = [[
        Paragraph("Mutual Fund Analytics Platform", title_style),
        Paragraph("Capstone Project Report", subtitle_style),
        Paragraph("End-to-End Data Engineering, ETL Pipeline &amp; Interactive Dashboard", subtitle_style),
    ]]
    title_table = Table([[
        Paragraph("Mutual Fund Analytics Platform", title_style),
    ]], colWidths=[17*cm])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(title_table)

    sub_table = Table([[
        Paragraph("End-to-End Data Engineering, ETL Pipeline &amp; Interactive Dashboard", subtitle_style),
    ]], colWidths=[17*cm])
    sub_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_MID),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 0.8*cm))

    # Info box
    info_data = [
        ['Intern', 'Madhankumar V'],
        ['Company', 'Bluestock Fintech Pvt. Ltd.'],
        ['Role', 'Data Analyst Intern'],
        ['Duration', '28 May 2026 – 28 Jul 2026'],
        ['Project ID', 'BFDA79190'],
        ['Date', 'June 2026'],
    ]
    info_table = Table(info_data, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BLUE_LIGHT),
        ('BACKGROUND', (1,0), (1,-1), white),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('TEXTCOLOR', (0,0), (0,-1), BLUE_DARK),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.8*cm))

    # KPI summary box
    kpi_data = [
        ['40 Schemes', '46,000+ NAV Records', '32,778 Transactions', '87K+ Total Rows'],
        ['10 AMCs', '4.5 Years Data', '12 Indian States', '15+ Charts'],
    ]
    kpi_table = Table(kpi_data, colWidths=[4.25*cm]*4)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (-1,-1), white),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, BLUE_MID),
    ]))
    story.append(kpi_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 1: EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "This report presents the findings of a comprehensive Mutual Fund Analytics Platform "
        "built for Bluestock Fintech Pvt. Ltd. The platform ingests publicly available data "
        "from AMFI India, processes it through a robust ETL pipeline, stores it in a normalised "
        "SQLite star-schema database, and presents actionable insights via an interactive "
        "Power BI dashboard.", body_style))

    story.append(Paragraph("Key Highlights:", h2_style))

    highlights = [
        "Analysed 40 mutual fund schemes across 10 leading AMCs in India",
        "Processed 87,000+ rows including 46,000 NAV records and 32,778 investor transactions",
        "SBI Small Cap Fund identified as top performer with 23.39% 3-year CAGR",
        "Built composite fund scorecard — ICICI Pru Midcap ranks #1 with 84.50/100",
        "SIP industry hit all-time high of Rs.31,002 Cr in December 2025",
        "Industry folio count doubled from 13.26 crore to 26.12 crore in 4 years",
        "97.7% of active SIP investors show irregular payment gaps exceeding 35 days",
        "T30 cities contribute 66.3% of investments — B30 cities remain untapped opportunity",
    ]
    for h in highlights:
        story.append(Paragraph(f"• {h}", bullet_style))

    story.append(Spacer(1, 0.5*cm))

    # ══════════════════════════════════════════════════
    # SECTION 2: PROBLEM STATEMENT
    # ══════════════════════════════════════════════════
    story.append(Paragraph("2. Problem Statement", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The Indian mutual fund industry manages over Rs.81 lakh crore in AUM across 1,908 "
        "schemes and 26.12 crore investor folios. Despite massive growth, investors and "
        "advisors face critical challenges:", body_style))

    problems = [
        ["P1: Data Fragmentation", "NAV, AUM and SIP data scattered across AMFI, NSE, BSE in different formats. No unified database exists."],
        ["P2: Performance Gap", "Investors cannot easily compare multiple funds on a risk-adjusted basis across AMCs."],
        ["P3: No Benchmark Tracking", "Retail investors cannot verify if their fund outperforms its benchmark index."],
        ["P4: Investor Blind Spot", "AMCs have limited visibility into demographic and geographic investment patterns."],
        ["P5: Slow Reporting", "Monthly MF reports are static PDFs taking days to prepare — no live dashboards."],
    ]

    prob_table = Table(problems, colWidths=[4.5*cm, 12.5*cm])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BLUE_LIGHT),
        ('BACKGROUND', (1,0), (1,-1), white),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), BLUE_DARK),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(prob_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 3: DATA SOURCES
    # ══════════════════════════════════════════════════
    story.append(Paragraph("3. Data Sources &amp; Datasets", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "All data sourced from publicly available, freely accessible sources including "
        "AMFI India, mfapi.in REST API, NSE and BSE. No proprietary data was used.",
        body_style))

    dataset_data = [
        ['#', 'Dataset', 'Rows', 'Description'],
        ['01', 'fund_master.csv', '40', 'Scheme metadata, expense ratios, fund managers'],
        ['02', 'nav_history.csv', '46,000', 'Daily NAV Jan 2022 – May 2026'],
        ['03', 'aum_by_fund_house.csv', '90', 'Quarterly AUM for top 10 AMCs'],
        ['04', 'monthly_sip_inflows.csv', '48', 'Industry SIP data 2022–2025'],
        ['05', 'category_inflows.csv', '144', 'Net inflows by fund category'],
        ['06', 'industry_folio_count.csv', '21', 'Total folios growth milestones'],
        ['07', 'scheme_performance.csv', '40', 'Risk-return metrics per scheme'],
        ['08', 'investor_transactions.csv', '32,778', 'SIP/Lumpsum/Redemption data'],
        ['09', 'portfolio_holdings.csv', '322', 'Top equity holdings per fund'],
        ['10', 'benchmark_indices.csv', '8,050', 'Nifty 50, Nifty 100, BSE SmallCap'],
        ['', 'TOTAL', '87,533+', '10 datasets across 7 working days'],
    ]

    ds_table = Table(dataset_data, colWidths=[1*cm, 5*cm, 2.5*cm, 8.5*cm])
    ds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (-1,-1), BLUE_LIGHT),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, GRAY_LIGHT]),
    ]))
    story.append(ds_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 4: ETL PIPELINE
    # ══════════════════════════════════════════════════
    story.append(Paragraph("4. ETL Pipeline &amp; System Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The platform follows a classic 5-layer data engineering architecture mirroring "
        "real-world fintech pipelines used at companies like Zerodha, Groww and Paytm Money.",
        body_style))

    layers = [
        ["Layer 1: EXTRACT", "Raw CSV datasets + mfapi.in live NAV API + AMFI public data"],
        ["Layer 2: TRANSFORM", "Python/Pandas — parse dates, forward-fill missing NAV, remove duplicates, validate AMFI codes"],
        ["Layer 3: LOAD", "SQLite star schema — 5 tables: dim_fund, fact_nav, fact_transactions, fact_performance, fact_benchmark"],
        ["Layer 4: ANALYSE", "Jupyter notebooks — EDA (15+ charts), Performance metrics, Advanced analytics"],
        ["Layer 5: VISUALISE", "Power BI Desktop — 4-page interactive dashboard with slicers and drill-through"],
    ]

    layer_table = Table(layers, colWidths=[4.5*cm, 12.5*cm])
    layer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (0,-1), white),
        ('BACKGROUND', (1,0), (1,-1), white),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (1,0), (1,-1), [GRAY_LIGHT, white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(layer_table)
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("4.1 Database Schema (Star Schema)", h2_style))
    schema_data = [
        ['Table', 'Type', 'Key Columns', 'Rows'],
        ['dim_fund', 'Dimension', 'amfi_code (PK), fund_house, category', '40'],
        ['fact_nav', 'Fact', 'amfi_code (FK), date, nav, daily_return', '46,000'],
        ['fact_transactions', 'Fact', 'investor_id, amfi_code (FK), amount_inr', '32,778'],
        ['fact_performance', 'Fact', 'amfi_code (FK), sharpe, alpha, beta', '40'],
        ['fact_benchmark', 'Fact', 'date, index_name, close_value', '8,050'],
    ]
    schema_table = Table(schema_data, colWidths=[4*cm, 2.5*cm, 7.5*cm, 3*cm])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_MID),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GRAY_LIGHT]),
    ]))
    story.append(schema_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 5: EDA FINDINGS
    # ══════════════════════════════════════════════════
    story.append(Paragraph("5. Exploratory Data Analysis — Key Findings", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    eda_findings = [
        ("5.1 NAV Trends (2022–2026)",
         "Small Cap funds showed strongest growth across the 4.5-year period. SBI Small Cap "
         "delivered highest returns while Large Cap funds showed steady, less volatile growth. "
         "The 2024 bull run is clearly visible across all equity categories."),
        ("5.2 AUM Growth",
         "SBI Mutual Fund dominates with Rs.12.5 lakh crore AUM — nearly 2x the second largest "
         "(ICICI Prudential at Rs.10.74 lakh crore). Industry AUM grew from Rs.38 lakh crore "
         "(2022) to Rs.81 lakh crore (2025) — a 2x increase in just 4 years."),
        ("5.3 SIP Industry Trends",
         "Monthly SIP inflows grew from Rs.11,517 Cr (Jan 2022) to Rs.31,002 Cr (Dec 2025) — "
         "nearly 3x growth in 4 years. Active SIP accounts grew from 4.91 crore to 9.35 crore, "
         "reflecting India's deepening equity culture."),
        ("5.4 Investor Demographics",
         "The 26-35 age group is most active (13,463 transactions — 41% of total). UPI dominates "
         "as payment mode (55%+ transactions). T30 cities contribute 66.3% of investments "
         "while B30 cities present significant untapped opportunity."),
        ("5.5 Folio Count Growth",
         "Industry folios doubled from 13.26 crore (Jan 2022) to 26.12 crore (Dec 2025), "
         "confirming massive retail investor participation growth in Indian mutual funds."),
    ]

    for title, content in eda_findings:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(content, body_style))

    # Charts
    charts_dir = "reports/charts"
    chart_files = [
        ("chart1_nav_trends.png", "Chart 1: NAV Trend Lines (2022–2026)"),
        ("chart3_sip_inflow.png", "Chart 3: Monthly SIP Inflow Trend"),
        ("chart5_demographics.png", "Chart 5: Investor Demographics"),
        ("chart6_geographic.png", "Chart 6: Geographic Distribution"),
    ]

    story.append(Paragraph("5.6 EDA Charts", h2_style))
    for chart_file, caption in chart_files:
        chart_path = os.path.join(charts_dir, chart_file)
        if os.path.exists(chart_path):
            img = Image(chart_path, width=16*cm, height=7*cm)
            story.append(img)
            story.append(Paragraph(caption, caption_style))
            story.append(Spacer(1, 0.3*cm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 6: PERFORMANCE ANALYSIS
    # ══════════════════════════════════════════════════
    story.append(Paragraph("6. Fund Performance Analytics", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("6.1 Top Performers by 3-Year CAGR", h2_style))
    perf_data = [
        ['Rank', 'Fund Name', '1yr CAGR', '3yr CAGR', '5yr CAGR'],
        ['1', 'SBI Small Cap Regular', '-', '23.39%', '~18%'],
        ['2', 'SBI Small Cap Direct', '-', '23.14%', '~18%'],
        ['3', 'ABSL Small Cap Regular', '-', '22.38%', '~17%'],
        ['4', 'Axis Small Cap Regular', '-', '20.98%', '~16%'],
        ['5', 'Nippon India Small Cap', '-', '20.15%', '~16%'],
    ]
    perf_table = Table(perf_data, colWidths=[1.5*cm, 8*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,1), HexColor('#fff9c4')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,2), (-1,-1), [white, GRAY_LIGHT]),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("6.2 Risk Metrics Summary", h2_style))
    risk_data = [
        ['Metric', 'Best Fund', 'Value', 'Interpretation'],
        ['Sharpe Ratio', 'Mirae Asset Large Cap', '1.4483', 'Excellent (>1 is good)'],
        ['Sortino Ratio', 'Mirae Asset Large Cap', '1.85+', 'Strong downside protection'],
        ['Alpha', 'HDFC Short Term Debt', '0.272', 'Outperforms benchmark'],
        ['Max Drawdown', 'ICICI Pru Liquid', '-0.02%', 'Minimal loss risk'],
        ['VaR (95%)', 'ICICI Pru Liquid', '-0.022%', 'Safest fund daily loss'],
        ['Worst Drawdown', 'SBI Small Cap Direct', '-52.57%', 'High risk — caution advised'],
    ]
    risk_table = Table(risk_data, colWidths=[3.5*cm, 5.5*cm, 3*cm, 5*cm])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_MID),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GRAY_LIGHT]),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("6.3 Fund Scorecard — Top 10", h2_style))
    score_data = [
        ['Rank', 'Fund Name', 'Score', '3yr CAGR', 'Sharpe'],
        ['1', 'ICICI Pru Midcap Regular', '84.50', '30.44%', '1.18'],
        ['2', 'Axis Midcap Regular', '80.75', '33.62%', '1.00'],
        ['3', 'HDFC Mid-Cap Opp Regular', '80.50', '31.07%', '1.09'],
        ['4', 'Mirae Asset Large Cap', '80.00', '32.56%', '1.45'],
        ['5', 'Kotak Flexicap Regular', '78.25', '28.35%', '1.31'],
        ['6', 'DSP Midcap Regular', '76.00', '27.80%', '1.22'],
        ['7', 'UTI Flexi Cap Regular', '75.50', '26.90%', '1.18'],
        ['8', 'ICICI Pru Bluechip Direct', '75.75', '31.10%', '1.03'],
        ['9', 'Nippon India Growth', '73.50', '25.40%', '0.98'],
        ['10', 'SBI Bluechip Regular', '73.06', '29.10%', '1.21'],
    ]
    score_table = Table(score_data, colWidths=[1.5*cm, 7.5*cm, 2.5*cm, 2.5*cm, 3*cm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,1), HexColor('#fff9c4')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,2), (-1,-1), [white, GRAY_LIGHT]),
    ]))
    story.append(score_table)

    # Benchmark chart
    bench_path = "reports/charts/benchmark_chart.png"
    if os.path.exists(bench_path):
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("6.4 Benchmark Comparison Chart", h2_style))
        img = Image(bench_path, width=16*cm, height=7*cm)
        story.append(img)
        story.append(Paragraph("Top 5 funds vs Nifty 50 benchmark (Base=100)", caption_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 7: ADVANCED ANALYTICS
    # ══════════════════════════════════════════════════
    story.append(Paragraph("7. Advanced Analytics &amp; Risk Metrics", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    adv_sections = [
        ("7.1 Value at Risk (VaR) &amp; CVaR",
         "Historical VaR at 95% confidence computed for all 40 funds. Small Cap funds carry "
         "highest daily VaR (-2.69%) meaning on a bad day investors can lose 2.69% of their "
         "investment. Liquid funds are safest with VaR of just -0.022% daily."),
        ("7.2 SIP Continuation Analysis",
         "Among 1,362 active SIP investors (6+ transactions), 97.7% (1,332 investors) show "
         "irregular payment gaps exceeding 35 days. Only 30 investors maintain truly regular SIPs. "
         "This presents a major opportunity for AMCs to improve SIP reminder and auto-debit systems."),
        ("7.3 Investor Cohort Analysis",
         "2024 cohort dominates with 4,803 investors and average investment of Rs.1.07 lakh. "
         "The 2025 cohort (197 investors) shows slightly higher average (Rs.1.09 lakh), "
         "suggesting newer investors are more affluent and financially aware."),
        ("7.4 Fund Recommender System",
         "Built a rule-based recommender: Low risk investors are recommended Liquid funds "
         "(Sharpe 7.68), Moderate risk investors get Large Cap funds (Sharpe 1.45), "
         "and High risk investors are directed to Small Cap funds (23%+ returns)."),
        ("7.5 Sector Concentration (HHI)",
         "Axis Bluechip Fund has highest sector concentration with HHI score of 0.2064. "
         "Funds above the 0.15 threshold (red line) carry higher sector-specific risk. "
         "Investors seeking true diversification should prefer funds with lower HHI scores."),
    ]

    for title, content in adv_sections:
        story.append(Paragraph(title, h2_style))
        story.append(Paragraph(content, body_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 8: DASHBOARD
    # ══════════════════════════════════════════════════
    story.append(Paragraph("8. Power BI Dashboard Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "The interactive Power BI dashboard consists of 4 pages, each targeting a specific "
        "business question. All pages include slicers for dynamic filtering.",
        body_style))

    dashboard_pages = [
        ['Page', 'Title', 'Key Visuals', 'Slicers'],
        ['1', 'Industry Overview',
         'KPI cards (AUM, SIP, Folios), AUM growth line, Fund house bar chart',
         'Year, Fund House'],
        ['2', 'Fund Performance',
         'Return vs Risk scatter, Fund scorecard table, NAV trend line',
         'Fund House, Category, Plan'],
        ['3', 'Investor Analytics',
         'Transaction by state bar, SIP/Lumpsum donut, Age group analysis',
         'State, Age Group, City Tier'],
        ['4', 'SIP &amp; Market Trends',
         'Dual-axis SIP + Nifty, Category matrix, YoY growth KPIs',
         'Year, Category'],
    ]

    dash_table = Table(dashboard_pages, colWidths=[1.2*cm, 3.8*cm, 8*cm, 4*cm])
    dash_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GRAY_LIGHT]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(dash_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 9: RECOMMENDATIONS
    # ══════════════════════════════════════════════════
    story.append(Paragraph("9. Recommendations", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    recs = [
        ["R1: Focus on Mid Cap Funds",
         "ICICI Pru Midcap and Axis Midcap consistently deliver high risk-adjusted returns "
         "(Sharpe >1.0) with manageable volatility. Suitable for moderate-to-high risk investors."],
        ["R2: Target B30 Cities",
         "Only 33.7% of investments come from Beyond Top 30 cities. Massive untapped market "
         "with growing digital penetration. AMCs should increase B30 outreach campaigns."],
        ["R3: Fix SIP Irregularity",
         "97.7% of active SIP investors show irregular gaps. Implementing automated WhatsApp/SMS "
         "reminders and seamless mandate systems could significantly improve SIP continuity."],
        ["R4: Promote Direct Plans",
         "Direct plans have avg expense ratio of 0.67% vs 1.34% for Regular plans. "
         "Over 10 years, this 0.67% difference compounds to significant wealth for investors."],
        ["R5: Small Cap Caution",
         "Despite 23%+ returns, Small Cap funds carry VaR of -2.69% daily and max drawdown "
         "of -52.57%. These should only be recommended for investors with Very High risk appetite "
         "and 7+ year investment horizon."],
    ]

    for title, content in recs:
        rec_data = [[Paragraph(title, ParagraphStyle('rt', fontSize=9,
                    fontName='Helvetica-Bold', textColor=white)),
                     Paragraph(content, ParagraphStyle('rc', fontSize=9,
                     fontName='Helvetica', leading=14))]]
        rec_table = Table(rec_data, colWidths=[4*cm, 13*cm])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), BLUE_MID),
            ('BACKGROUND', (1,0), (1,0), GRAY_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.3, GRAY_MID),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 0.2*cm))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════
    # SECTION 10: LIMITATIONS
    # ══════════════════════════════════════════════════
    story.append(Paragraph("10. Limitations", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    limitations = [
        "NAV data anchored to real AMFI values but simulated forward using realistic return/volatility parameters consistent with actual market behaviour",
        "Investor transaction data is synthetically generated using real demographic and geographic distributions from AMFI published data",
        "Analysis covers January 2022 to May 2026 only — longer historical data would improve statistical significance of risk metrics",
        "Power BI dashboard requires Desktop installation to view interactively — web publishing requires Power BI Pro licence",
        "Fund recommender uses rule-based logic — a production system would require ML-based personalisation",
        "Sector concentration analysis based on Dec 2025 holdings snapshot — portfolios change quarterly",
    ]

    for i, lim in enumerate(limitations, 1):
        story.append(Paragraph(f"L{i}: {lim}", bullet_style))

    story.append(Spacer(1, 0.5*cm))

    # ══════════════════════════════════════════════════
    # SECTION 11: CONCLUSION
    # ══════════════════════════════════════════════════
    story.append(Paragraph("11. Conclusion", h1_style))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        "This capstone project successfully demonstrates end-to-end data engineering and "
        "analytics capabilities applied to the Indian mutual fund industry. The platform "
        "ingests, cleans, analyses and visualises mutual fund data at scale — providing "
        "actionable insights for fund selection, risk management and investor behaviour analysis.",
        body_style))

    story.append(Paragraph(
        "The findings reveal a rapidly growing Indian MF industry with SIP inflows hitting "
        "all-time highs, folio counts doubling, and Mid Cap funds delivering the best "
        "risk-adjusted returns. Significant opportunities exist in B30 cities, SIP "
        "regularisation, and direct plan adoption.",
        body_style))

    story.append(Paragraph(
        "The technical stack — Python, Pandas, SQLite, Matplotlib, Seaborn, Plotly, SciPy "
        "and Power BI — demonstrates proficiency across the full data analytics lifecycle "
        "from raw data ingestion to executive-level dashboards.",
        body_style))

    story.append(Spacer(1, 1*cm))

    # Footer
    footer_data = [[
        Paragraph("Bluestock Fintech Pvt. Ltd. | Capstone Project | BFDA79190 | June 2026",
                  ParagraphStyle('footer', fontSize=8, fontName='Helvetica',
                  textColor=white, alignment=TA_CENTER)),
        Paragraph("This report is for educational purposes only. Not financial advice.",
                  ParagraphStyle('footer2', fontSize=8, fontName='Helvetica',
                  textColor=white, alignment=TA_CENTER)),
    ]]
    footer_table = Table([[
        Paragraph("Bluestock Fintech Pvt. Ltd. | Capstone Project | BFDA79190 | Madhankumar V | June 2026",
                  ParagraphStyle('footer', fontSize=9, fontName='Helvetica-Bold',
                  textColor=white, alignment=TA_CENTER)),
    ]], colWidths=[17*cm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(footer_table)

    doc.build(story)
    print(f"✅ Final Report PDF saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_report()
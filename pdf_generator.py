from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

class PDFReportGenerator:
    def create_report(self, analysis_text, basic_info=None, financial_goals=None, filename='financial_report.pdf'):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        # Define custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1a365d')
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.HexColor('#2c5282')
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=10,
            textColor=colors.HexColor('#2b6cb0')
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.HexColor('#2d3748')
        )
        
        # Add title
        content.append(Paragraph("Financial Advisory Report", title_style))
        
        if basic_info:
            content.append(Paragraph("Personal Profile", heading1_style))
            content.append(Spacer(1, 10))
            
            data = [
                ["Name", basic_info['name']],
                ["Age", str(basic_info['age'])],
                ["Occupation", basic_info['occupation']],
                ["Marital Status", basic_info['marital_status']],
                ["Dependents", str(basic_info['dependents'])],
                ["Monthly Income", f"${basic_info['salary']:,.2f}"],
                ["Monthly Savings", f"${basic_info['savings']:,.2f}"],
                ["Monthly Expenses", f"${basic_info['spendings']:,.2f}"]
            ]
            
            table = Table(data, colWidths=[200, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2d3748')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            content.append(table)
            content.append(Spacer(1, 20))

        if financial_goals:
            content.append(Paragraph("Financial Goals", heading1_style))
            
            # Short-term goals
            content.append(Paragraph("Short-term Goals", heading2_style))
            goals_data = [
                ["Goals", ", ".join(financial_goals['short_term'])],
                ["Target Amount", f"${financial_goals['short_term_amount']:,.2f}"],
                ["Timeline", f"{financial_goals['short_term_timeline']} months"]
            ]
            
            table = Table(goals_data, colWidths=[200, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            content.append(table)
            content.append(Spacer(1, 15))
            
            # Long-term goals
            content.append(Paragraph("Long-term Goals", heading2_style))
            goals_data = [
                ["Goals", ", ".join(financial_goals['long_term'])],
                ["Target Amount", f"${financial_goals['long_term_amount']:,.2f}"],
                ["Timeline", f"{financial_goals['long_term_timeline']} years"]
            ]
            
            table = Table(goals_data, colWidths=[200, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            content.append(table)
            content.append(Spacer(1, 20))

        content.append(Paragraph("Financial Analysis & Recommendations", heading1_style))
        
        # Extract the raw text from CrewOutput
        if hasattr(analysis_text, 'raw'):
            report_text = analysis_text.raw
        else:
            report_text = str(analysis_text)
            
        # Process sections
        sections = report_text.split('\n\n')
        for section in sections:
            if section.strip():
                if ':' in section:
                    title, content_text = section.split(':', 1)
                    content.append(Paragraph(title.strip(), heading2_style))
                    content.append(Paragraph(content_text.strip(), normal_style))
                else:
                    content.append(Paragraph(section.strip(), normal_style))
                content.append(Spacer(1, 8))
        
        doc.build(content)
        return filename
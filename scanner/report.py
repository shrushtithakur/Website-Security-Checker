from fpdf import FPDF
from datetime import datetime
import os


class SecurityReportPDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Website Security Audit Report", ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.set_text_color(120)
        self.cell(0, 10, "Developed by Shrushti Thakur", align="C")


def generate_pdf(
    url,
    score,
    ssl_ok,
    https_ok,
    headers,
    cookies,
    screenshot,
    output_path
):
    pdf = SecurityReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ---------------- Meta Information ----------------
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Target Website: {url}", ln=True)
    pdf.cell(
        0,
        8,
        f"Scan Date & Time: {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        ln=True,
    )
    pdf.ln(4)

    # ---------------- Security Score ----------------
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 120)
    pdf.cell(0, 10, f"Overall Security Score: {score} / 100", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # ---------------- Executive Summary ----------------
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Executive Summary", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", size=11)
    if score >= 70:
        summary = (
            "The website follows good basic security practices. "
            "Only minor improvements are recommended."
        )
    elif score >= 40:
        summary = (
            "The website has moderate security risks. "
            "Some configurations should be improved."
        )
    else:
        summary = (
            "The website is vulnerable and requires immediate "
            "security configuration fixes."
        )

    pdf.multi_cell(0, 8, summary)
    pdf.ln(6)

    # ---------------- Security Findings Table ----------------
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Detailed Security Findings", ln=True)
    pdf.ln(3)

    # Table Header
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(55, 8, "Security Check", border=1, fill=True)
    pdf.cell(95, 8, "Description", border=1, fill=True)
    pdf.cell(40, 8, "Result", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Arial", size=11)

    # SSL
    pdf.cell(55, 8, "SSL Certificate", border=1)
    pdf.cell(95, 8, "Validates SSL/TLS certificate availability", border=1)
    pdf.cell(40, 8, "PASS" if ssl_ok else "FAIL", border=1)
    pdf.ln()

    # HTTPS
    pdf.cell(55, 8, "HTTPS Enforcement", border=1)
    pdf.cell(95, 8, "Checks automatic redirection to HTTPS", border=1)
    pdf.cell(40, 8, "PASS" if https_ok else "FAIL", border=1)
    pdf.ln()

    # Security Headers
    for header, present in headers.items():
        pdf.cell(55, 8, header, border=1)
        pdf.cell(95, 8, f"Checks presence of {header}", border=1)
        pdf.cell(40, 8, "PASS" if present else "FAIL", border=1)
        pdf.ln()

    # Cookies
    cookie_status = "PASS" if cookies else "INFO"
    pdf.cell(55, 8, "Cookie Security", border=1)
    pdf.cell(95, 8, "Analyzes Secure and HttpOnly cookie flags", border=1)
    pdf.cell(40, 8, cookie_status, border=1)
    pdf.ln()

    pdf.ln(6)

    # ---------------- Screenshot Evidence ----------------
    if os.path.exists(screenshot):
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Audit Evidence (Website Screenshot)", ln=True)
        pdf.ln(3)
        pdf.image(screenshot, x=10, w=190)

    # ---------------- Save ----------------
    pdf.output(output_path)
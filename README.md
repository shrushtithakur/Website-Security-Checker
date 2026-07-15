# 🔐 Website Security Checker

A Streamlit-based application that performs automated website security audits by identifying common configuration-level vulnerabilities and generating a professional PDF security report with visual evidence.

## Features
- SSL certificate validation
- HTTPS redirection enforcement
- HTTP security header analysis
- Cookie security inspection (Secure & HttpOnly flags)
- Automated website screenshot capture
- Security scoring with risk classification
- Downloadable PDF security audit report

## Tech Stack
Python, Streamlit, Requests, Selenium, Plotly, FPDF, Pillow, WebDriver Manager

## Usage
```bash
pip install -r requirements.txt
streamlit run app.py

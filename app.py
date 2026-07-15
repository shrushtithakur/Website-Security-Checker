import streamlit as st
import plotly.graph_objects as go
from urllib.parse import urlparse
from datetime import datetime
from PIL import Image
import os
import tempfile
import uuid

from scanner.ssl_check import validate_ssl
from scanner.https_redirect import check_https_redirect
from scanner.headers_check import analyze_headers
from scanner.cookies_check import check_cookies
from scanner.scorer import calculate_score
from scanner.screenshot import capture_screenshot
from scanner.report import generate_pdf

# ===================== SESSION STATE INITIALIZATION =====================
if 'scan_completed' not in st.session_state:
    st.session_state.scan_completed = False
if 'scan_data' not in st.session_state:
    st.session_state.scan_data = {}
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'screenshot_path' not in st.session_state:
    st.session_state.screenshot_path = None


# ---------------- Utility ----------------
def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def risk_level(score):
    if score >= 70:
        return "Good", "Low risk – website follows basic security practices."
    elif score >= 40:
        return "Moderate", "Medium risk – improvements are recommended."
    else:
        return "Critical", "High risk – immediate fixes are required."


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Website Security Checker",
    layout="wide"
)

# ---------------- Global UI Styling ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.section-card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}
.subtle-text {
    color: #6b7280;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("<h1 style='text-align:center;'>Website Security Checker</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtle-text' style='text-align:center;'>"
    "Automated audit tool for common website security misconfigurations"
    "</p>",
    unsafe_allow_html=True
)

st.write("")

# ===================== SECTION 1: INPUT =====================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Website Input</div>", unsafe_allow_html=True)

st.write(
    "Enter a website URL to perform an automated security audit. "
    "This tool evaluates essential security configurations typically "
    "reviewed in academic and basic compliance audits."
)

raw_url = st.text_input("Website URL", placeholder="example.com")

st.markdown("""
**Security checks performed:**
- SSL certificate validation  
- HTTPS redirection enforcement  
- HTTP security headers  
- Cookie security attributes  
- Screenshot-based audit evidence  
""")

scan_btn = st.button("Run Security Scan", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ===================== SECTION 2: SCAN =====================
if scan_btn:
    if not raw_url.strip():
        st.error("Please enter a valid website URL.")
    else:
        try:
            with st.spinner("Running security audit..."):
                url = normalize_url(raw_url)
                domain = urlparse(url).netloc

                ssl_data = validate_ssl(domain)
                https_ok = check_https_redirect(url)
                headers = analyze_headers(url)
                cookies = check_cookies(url)

                score = calculate_score(
                    ssl_data.get("status", False),
                    https_ok,
                    headers,
                    cookies
                )

                # ===== Generate Unique Temporary Files =====
                temp_dir = tempfile.gettempdir()
                unique_id = uuid.uuid4().hex
                screenshot_path = os.path.join(temp_dir, f"{unique_id}_screenshot.png")
                pdf_path = os.path.join(temp_dir, f"{unique_id}_security_report.pdf")

                capture_screenshot(url, screenshot_path)
                generate_pdf(
                    url,
                    score,
                    ssl_data.get("status", False),
                    https_ok,
                    headers,
                    cookies,
                    screenshot_path,
                    pdf_path
                )

                # ===== Save to Session State =====
                st.session_state.scan_data = {
                    "domain": domain,
                    "score": score,
                    "level": risk_level(score),
                    "ssl_status": ssl_data.get("status", False),
                    "https_ok": https_ok,
                    "headers": headers,
                    "cookies": cookies,
                    "timestamp": datetime.now().strftime('%d %b %Y, %I:%M %p')
                }
                st.session_state.screenshot_path = screenshot_path
                st.session_state.pdf_path = pdf_path
                st.session_state.scan_completed = True

        except Exception as e:
            st.error(f"An unexpected error occurred during the scan: {str(e)}")
            st.stop()

# ===================== SECTION 3: DISPLAY RESULTS =====================
if st.session_state.scan_completed:
    data = st.session_state.scan_data

    st.success("Security audit completed successfully.")

    # ===================== SUMMARY =====================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Scan Summary</div>", unsafe_allow_html=True)

    level, interpretation = data["level"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Target Website", data["domain"])
    col2.metric("Security Score", f"{data['score']} / 100")
    col3.metric("Risk Level", level)

    st.write(f"**Interpretation:** {interpretation}")
    st.write(f"**Scan Time:** {data['timestamp']}")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["score"],
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1f2937"},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ===================== FINDINGS =====================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Detailed Security Findings</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**SSL Certificate**")
        st.write("Valid" if data["ssl_status"] else "Invalid or Missing")

        st.markdown("**HTTPS Enforcement**")
        st.write("Enabled" if data["https_ok"] else "Not Enforced")

    with col2:
        st.markdown("**Security Headers**")
        for h, v in data["headers"].items():
            st.write(f"{h}: {'Present' if v else 'Missing'}")

        st.markdown("**Cookie Security**")
        st.write(f"Cookies Detected: {len(data['cookies'])}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================== EVIDENCE =====================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Audit Evidence</div>", unsafe_allow_html=True)

    st.write(
        "The screenshot below serves as visual confirmation of the scanned website "
        "and is included in the generated PDF audit report."
    )

    if os.path.exists(st.session_state.screenshot_path):
        st.image(
            Image.open(st.session_state.screenshot_path),
            caption="Captured Website Screenshot",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================== RECOMMENDATIONS =====================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>General Recommendations</div>", unsafe_allow_html=True)

    st.markdown("""
- Enforce HTTPS redirection at the server level  
- Enable all essential HTTP security headers  
- Use Secure and HttpOnly flags for cookies  
- Regularly monitor SSL certificate expiry  
""")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================== REPORT =====================
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Export Report</div>", unsafe_allow_html=True)

    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        with open(st.session_state.pdf_path, "rb") as pdf:
            st.download_button(
                "Download PDF Security Audit Report",
                pdf,
                file_name="Website_Security_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.error("PDF file was not generated correctly. Please scan again.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown(
    "<div class='footer'>Developed by <b>Shrushti Thakur</b></div>",
    unsafe_allow_html=True
)
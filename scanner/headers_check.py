import requests

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]

def analyze_headers(url):
    r = requests.get(url, timeout=5)
    return {h: h in r.headers for h in SECURITY_HEADERS}
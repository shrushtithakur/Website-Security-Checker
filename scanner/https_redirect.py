import requests

def check_https_redirect(url):
    try:
        r = requests.get(url, allow_redirects=False, timeout=5)
        return r.status_code in [301, 302] and "https://" in r.headers.get("Location", "")
    except:
        return False
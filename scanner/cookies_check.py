import requests

def check_cookies(url):
    # Added timeout=5 to prevent the app from freezing on unresponsive sites
    r = requests.get(url, timeout=5)
    cookies = []

    for c in r.cookies:
        cookies.append({
            "name": c.name,
            "secure": c.secure,
            "httponly": c.has_nonstandard_attr("HttpOnly")
        })

    return cookies
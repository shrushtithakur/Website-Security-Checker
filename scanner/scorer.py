def calculate_score(ssl_ok, https_ok, headers, cookies):
    score = 0

    if ssl_ok:
        score += 40
    if https_ok:
        score += 20

    score += (sum(headers.values()) / len(headers)) * 30

    if cookies:
        secure = sum(1 for c in cookies if c["secure"] and c["httponly"])
        score += (secure / len(cookies)) * 10

    return round(score, 2)
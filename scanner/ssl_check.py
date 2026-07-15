import ssl, socket
from datetime import datetime

def validate_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()

        expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        valid = expiry > datetime.utcnow()

        return {
            "status": valid,
            "issuer": cert['issuer'][0][0][1],
            "expiry": expiry.strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"status": False, "error": str(e)}
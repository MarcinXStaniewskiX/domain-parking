from flask import Flask, request, render_template_string
import requests
import random

app = Flask(__name__)

OFFERS = [
    {"geo": "RU", "url": "https://cpa1.com/offer?id=123", "title": "Binance — бонус 100$"},
    {"geo": "US", "url": "https://cpa2.com/offer?id=456", "title": "VPN Express — скидка 49%"},
    {"geo": "default", "url": "https://cpa-global.com/offer", "title": "Заработок в крипте"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #16213e; padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; }
        h1 { color: #00d4ff; }
        .btn { display: inline-block; margin-top: 20px; padding: 15px 30px; background: #00d4ff; color: #000; border-radius: 30px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ title }}</h1>
        <p>Этот сайт больше не работает, но у нас есть предложение.</p>
        <a href="{{ offer_url }}" class="btn">Перейти →</a>
    </div>
</body>
</html>
"""

def get_user_geo(ip):
    try:
        resp = requests.get(f"https://ipapi.co/{ip}/country/", timeout=2)
        return resp.text.strip() if resp.status_code == 200 else "default"
    except:
        return "default"

def get_offer_by_geo(geo):
    for offer in OFFERS:
        if offer["geo"] == geo:
            return offer
    return OFFERS[-1]

@app.route('/')
def index():
    user_ip = request.headers.get('CF-Connecting-IP') or request.remote_addr
    geo = get_user_geo(user_ip)
    offer = get_offer_by_geo(geo)
    return render_template_string(HTML_TEMPLATE, title=offer['title'], offer_url=offer['url'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
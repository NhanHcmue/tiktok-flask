from flask import Flask, request, jsonify
import requests, re, time

app = Flask(__name__)

COOKIE = "paste_your_cookie_here"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT, "Cookie": COOKIE}

def get_tiktok_views(url, max_retry=3, delay=3):
    for attempt in range(1, max_retry + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                time.sleep(delay)
                continue
            match = re.search(r'"playCount":(\d+)', r.text)
            if match:
                return int(match.group(1))
            time.sleep(delay)
        except requests.RequestException:
            time.sleep(delay)
    return None

@app.route("/get_views", methods=["POST"])
def get_views_api():
    data = request.json
    urls = data.get("urls", [])
    result = {url: get_tiktok_views(url) for url in urls}
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

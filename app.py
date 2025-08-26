from flask import Flask, request, jsonify
import requests, re, time, os

app = Flask(__name__)

# --- Cấu hình ---
COOKIE = "tt_csrf_token=elEn6owq-nIwTLNi0TqM60uZPxbH601E4nRw; tt_chain_token=QPMsm5ktRw3A+JxFrlLb/A==; delay_guest_mode_vid=8; passport_csrf_token=d4746bdc5ef7628595c4ef291085748f; passport_csrf_token_default=d4746bdc5ef7628595c4ef291085748f; fbm_1862952583919182=base_domain=.www.tiktok.com; s_v_web_id=verify_met2md3j_l3jqfjV5_aFzT_4FkB_B2FD_ZQkWB31VXKdw; multi_sids=7194288964244177947%3Afd7df6552c0c7f02d44939edd058f09a; cmpl_token=AgQQAPOFF-RO0rPp0RWle10i8s-w6BaIv4MOYN06Ig; passport_auth_status=c14be790b472cd71efa27de8f023c7a9%2C; passport_auth_status_ss=c14be790b472cd71efa27de8f023c7a9%2C; uid_tt=924aa0a4365fb21b4b67f399167c77349e29cd696af4f75deb6a72d7abd26c2c; uid_tt_ss=924aa0a4365fb21b4b67f399167c77349e29cd696af4f75deb6a72d7abd26c2c; sid_tt=fd7df6552c0c7f02d44939edd058f09a; sessionid=fd7df6552c0c7f02d44939edd058f09a; sessionid_ss=fd7df6552c0c7f02d44939edd058f09a; store-idc=alisg; store-country-code=vn; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=j36th5dt2kOx3qXFAvU8lXl1ffMzLppU5KXRkWgOoMsc9iG5nPOaSrl01ee2UxlB9haptJf1WDdvg4IbdyKEQPJXLNqLyANtr4oQUNdLl2vw9xMo6dCJN55kXz0OBEp1RSSQOfe2_Emnf-hczydgo889AGH_y-uQZ8y0dxouWZV2fX4pQe9SZ7zydxXJ_3FspFaHMoFdhoe_kCSosdtPzm-P6jLRbtm2b8x9rTqSK4Cj2PA5-uzFD6b9-uym7CkGxhA1FsUKHT1-nCBxtvugW1Aj-q4StHrdXygfirz5B1vDzab-i5OcoRgyVyex9ltWrQkxUcdYxyTsLt7r6arKYLFFxQA9ee300rvqChwjEKIYpVEVC6N-nwzxfPcAEmUCltLpofw7tbaHPMMOWmgpOie-9Auq6ybxZTVE7gyLOhAuOHCaR8HKBOnI43haiuMYx3B5mTKRQC7KmZxGEm6fs2OkzdUvqIEB3Vh-2Qe5JSVhkP2mKvJ8YNyObpHimCPn; last_login_method=google; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; sid_guard=fd7df6552c0c7f02d44939edd058f09a%7C1756244586%7C15551987%7CSun%2C+22-Feb-2026+21%3A42%3A53+GMT; sid_ucp_v1=1.0.0-KDJkMTFkOTdjZDE1NjZiMGJkNjcyOWI1ZTAzMDBhMzBhM2RmMjM1YzIKGQibiKbqovbP62MQ6tS4xQYYsws4CEASSAQQAxoDc2cxIiBmZDdkZjY1NTJjMGM3ZjAyZDQ0OTM5ZWRkMDU4ZjA5YQ; ssid_ucp_v1=1.0.0-KDJkMTFkOTdjZDE1NjZiMGJkNjcyOWI1ZTAzMDBhMzBhM2RmMjM1YzIKGQibiKbqovbP62MQ6tS4xQYYsws4CEASSAQQAxoDc2cxIiBmZDdkZjY1NTJjMGM3ZjAyZDQ0OTM5ZWRkMDU4ZjA5YQ; passport_fe_beating_status=true; perf_feed_cache={%22expireTimestamp%22:1758841200000%2C%22itemIds%22:[%227542724144736079122%22%2C%227529482274161708295%22%2C%227541768154716917009%22]}; ttwid=1%7CV3yOZGU5_oLycOpSzDGrZ82c8ZPlCDQOhWQ6XnJPQHc%7C1756251425%7C34e3c72e640c3eb675756e85b9fe5aab3670edfffd607294f7064aac2e817927; store-country-sign=MEIEDKz7SNlAQpiE8wQaUgQg5dBCcmHCggOJXpnOdlObhQMH_WifmJFcnvYc_PKNoQcEEO7OjkLbEFoWd22sA7pKxfM; odin_tt=6e2aa21365b32d549f1feaf9d49b3143edc2bbc61cf7752b41b9143864c535e12e8c51dff3f4b3902a267994a12b0d27719668be50e0a359aa7a19676c19d9349bcda05b5b28cb9e6eb6f7ca51355ad8; msToken=ZBoiEW-04GncRsg_XkWIi2d-xNLwp9WJa4r1NeEzeMcuwB97vnoKJXGUt392bgsoKDsiSV6MujqApvJr-58cWmCoSQQsTBhy8DGLhbKeZTafOEkLvV16rFra6XbyLNSX1JzxhgF9sWHETlo2PTEhVqEa; msToken=TVuC0BYZjN1pPqa_a8GRI5LlPjp6cwajA3C7_WhO9V-l3dTAmR8W45nDpnyXFaqse2tPjxgWOb90E6UWGUOaxmqlSrOX9lFUxpAKe3D34KkBw2FMvCj7MFpEAz02lnFidnBvuURu5Pd3Tx095rjpVQqI"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT, "Cookie": COOKIE}

# --- Hàm lấy view ---
def get_tiktok_views(url, max_retry=3, delay=3):
    """Lấy số view của video TikTok. Retry max_retry lần nếu thất bại."""
    for attempt in range(1, max_retry + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                print(f"[Attempt {attempt}] Request thất bại: {r.status_code}")
                time.sleep(delay)
                continue

            match = re.search(r'"playCount":(\d+)', r.text)
            if match:
                print(f"[Attempt {attempt}] Lấy được view: {match.group(1)}")
                return int(match.group(1))
            else:
                print(f"[Attempt {attempt}] Không tìm thấy view trong HTML")
                time.sleep(delay)
        except requests.RequestException as e:
            print(f"[Attempt {attempt}] Lỗi request: {e}")
            time.sleep(delay)
    return None

# --- API route ---
@app.route("/get_views", methods=["POST"])
def get_views_api():
    data = request.json
    urls = data.get("urls", [])
    if not urls:
        return jsonify({"error": "Không có urls"}), 400

    result = {}
    for url in urls:
        views = get_tiktok_views(url)
        result[url] = views
    return jsonify(result)

# --- Chạy app ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sẽ gán PORT động
    app.run(host="0.0.0.0", port=port)

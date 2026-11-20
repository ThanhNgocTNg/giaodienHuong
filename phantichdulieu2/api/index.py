from http.server import BaseHTTPRequestHandler
import os


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        target_url = os.environ.get("STREAMLIT_APP_URL", "")
        if target_url:
            self.send_response(302)
            self.send_header("Location", target_url)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Insight — Kết nối ứng dụng</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f6f8fc; color: #192b45; margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px; line-height: 1.75; }
        main { max-width: 720px; background: white; border: 1px solid #e2e8f1; border-radius: 20px; padding: clamp(24px, 5vw, 48px); box-shadow: 0 16px 44px #192b4508; }
        .brand { font-size: 20px; font-weight: 750; letter-spacing: -.5px; margin-bottom: 32px; display: flex; align-items: center; gap: 12px; }
        .mark { background: #2563eb; color: white; font-size: 14px; padding: 4px 10px; border-radius: 9px; }
        .badge { display: inline-block; background: #edf3ff; color: #3067c7; border: 1px solid #dce8fe; border-radius: 6px; padding: 4px 10px; font-size: 12px; font-weight: 650; }
        h1 { font-size: clamp(26px, 4vw, 34px); line-height: 1.3; letter-spacing: -1px; margin: 16px 0; }
        p { color: #63718a; }
        .step-box { border: 1px solid #e2e8f1; background: #f8faff; border-radius: 12px; padding: 20px; margin: 20px 0; }
        .step-box strong { display: block; margin-bottom: 8px; }
        ol { padding-left: 22px; color: #536782; margin-bottom: 0; }
        code { background: #eaf1ff; color: #2656a4; padding: 2px 6px; border-radius: 4px; overflow-wrap: anywhere; }
        a { color: #2159bf; text-underline-offset: 3px; }
        .btn { display: inline-block; color: white; background: #2563eb; border: 1px solid #2563eb; border-radius: 9px; padding: 11px 20px; text-decoration: none; font-weight: 600; transition: background-color 160ms; }
        .btn:hover { background: #1d55d2; }
        a:focus-visible { outline: 3px solid #88b1ff; outline-offset: 4px; }
        @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
    </style>
</head>
<body>
    <main>
        <div class="brand"><span class="mark" aria-hidden="true">DI</span>Data Insight</div>
        <span class="badge">KẾT NỐI KHÔNG GIAN PHÂN TÍCH</span>
        <h1>Thêm một bước để khám phá dữ liệu.</h1>
        <p>Địa chỉ ứng dụng chưa được cấu hình. Hãy triển khai ứng dụng Streamlit và kết nối địa chỉ của ứng dụng để sử dụng đầy đủ quy trình nhập, làm sạch và tạo báo cáo.</p>
        <div class="step-box">
            <strong>Triển khai với Streamlit Community Cloud</strong>
            <ol>
                <li>Đăng nhập <a href="https://share.streamlit.io" target="_blank" rel="noopener noreferrer">Streamlit Community Cloud</a> bằng GitHub.</li>
                <li>Chọn kho mã nguồn này và file chính <code>app.py</code>, sau đó chọn Deploy.</li>
                <li>Thêm địa chỉ ứng dụng vào biến <code>STREAMLIT_APP_URL</code> trên Vercel để bật chuyển hướng tự động.</li>
            </ol>
        </div>
        <div class="step-box">
            <strong>Chạy trên Render hoặc Railway</strong>
            Kết nối kho GitHub với dịch vụ. Dự án đã có <code>Procfile</code> và <code>requirements.txt</code> để chạy ứng dụng Streamlit.
        </div>
        <a class="btn" href="https://share.streamlit.io" target="_blank" rel="noopener noreferrer">Mở Streamlit Community Cloud</a>
    </main>
</body>
</html>"""
        self.wfile.write(html.encode("utf-8"))


# Data Insight — Phân tích dữ liệu

Ứng dụng Streamlit để nhập dữ liệu, duyệt làm sạch và tạo báo cáo trực quan. Mã nguồn được clone từ [phantichdulieu2](https://github.com/nguyenhuong27012007-glitch/phantichdulieu2).

## Chạy tại máy

Yêu cầu Python 3.9 trở lên.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Mở địa chỉ localhost được in trong terminal, thông thường là `http://localhost:8501`.

Cấu hình Gemini qua biến môi trường `GEMINI_API_KEY` hoặc mục **Cài đặt API** ở thanh bên. Có thể kiểm tra dữ liệu, làm sạch và tạo Dashboard thống kê mà không cần gọi Gemini.

## Giao diện mới

- Trang tổng quan với nút bắt đầu Streamlit gốc, truy cập được bằng bàn phím.
- Thanh bên thu vào mép trái, mở khi rê chuột hoặc đưa tiêu điểm bàn phím vào điều hướng. Trên thiết bị cảm ứng, dùng nút menu để mở.
- Chọn mô hình và cấu hình API nằm trong mục **Cài đặt AI** ở đầu trang, không còn chiếm diện tích sidebar.
- Thanh tiến trình hiển thị bước đang làm; các bước sau mở khi dữ liệu đã được duyệt.
- Các khung nhập dữ liệu, bảng, nút và thông báo dùng cùng một hệ màu xanh, nền sáng và khoảng cách nhất quán.
- Chuyển động ngắn, nhẹ; tự tắt khi thiết bị bật chế độ giảm chuyển động. Các bảng làm việc không phóng to khi rê chuột.
- Bố cục co giãn trên điện thoại; báo cáo HTML tải xuống có bố cục thích ứng và bảng cuộn ngang.
- Bối cảnh doanh nghiệp được giữ khi chuyển giữa các bước.
- Giao diện dùng nhãn chữ, bỏ emoji trang trí. Biểu mẫu bối cảnh chia thông tin doanh nghiệp và mục tiêu thành hai vùng; tìm kiếm/sắp xếp nằm cùng hàng, bộ lọc nâng cao được thu gọn.
- Gợi ý bối cảnh cập nhật trực tiếp từ session state, không còn cảnh báo trùng giá trị mặc định của widget `biz_type`.

Hình biểu đồ trên trang tổng quan được ghi rõ là **dữ liệu minh họa**. Dashboard ở bước 3 được tính từ tệp người dùng nạp.

## Các chức năng được giữ

Nhập nhiều tệp CSV/TSV/Excel và Google Sheets công khai; tìm kiếm, lọc, sắp xếp, chọn cột và sửa bảng trực tiếp; gợi ý bối cảnh; phát hiện dữ liệu thiếu, trùng lặp, khoảng trắng và số âm; duyệt cách sửa, xem trước, hoàn tác; tải CSV đã làm sạch; chọn chỉ số và chiều phân tích; chỉnh báo cáo và bảng tổng hợp; tải báo cáo HTML.

Các module `agents/`, `utils/` và quy tắc tính thống kê không thay đổi trong đợt chỉnh giao diện này. Chức năng Google Sheets và Gemini cần quyền truy cập mạng/cấu hình phù hợp.

## Kiểm tra

```sh
GEMINI_API_KEY='' .venv/bin/python -m unittest discover -s tests -v
```

Các kiểm tra chạy qua Streamlit AppTest: điều hướng và phê duyệt, CSV/Excel, tìm kiếm/sắp xếp/chọn cột, sửa và khôi phục dữ liệu, tạo và chỉnh báo cáo, giữ bối cảnh khi chuyển trang. Không gọi Gemini hoặc Google Sheets bên ngoài.

Đã kiểm tra trực tiếp trên trình duyệt: tải CSV mẫu, chuyển qua ba bước, tạo Dashboard, tải báo cáo HTML và bố cục điện thoại.

## Cấu trúc giao diện

- `app.py`: quy trình ba bước và xử lý hiện có.
- `ui.py`: trang tổng quan, thương hiệu và tiêu đề.
- `assets/styles.css`: hệ màu, bố cục, tương tác và hỗ trợ giảm chuyển động.
- `.streamlit/config.toml`: theme gốc của các widget Streamlit.
- `api/index.py`: giữ vai trò chuyển hướng Vercel đến `STREAMLIT_APP_URL`; nếu chưa cấu hình thì hiển thị hướng dẫn kết nối.

Entry point vẫn là `app.py`; `Procfile` và cấu hình Vercel được giữ nguyên.

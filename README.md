# Product Service API

REST API quản lý sản phẩm được xây dựng bằng **Django** và **Django REST Framework**. Dữ liệu được lưu trong PostgreSQL và các API yêu cầu xác thực bằng JWT (JSON Web Token).

## 1. Chức năng

- Lấy danh sách sản phẩm.
- Xem thông tin chi tiết một sản phẩm.
- Thêm sản phẩm mới.
- Cập nhật thông tin sản phẩm.
- Xóa sản phẩm.
- Xác thực request bằng JWT với header `Authorization: Bearer <token>`.
- Kiểm tra dữ liệu: giá và số lượng không được âm.

## 2. Công nghệ sử dụng

- Python
- Django
- Django REST Framework
- PostgreSQL
- PyJWT

## 3. Cấu trúc dự án

```text
product_service/
├── manage.py
├── config/
│   ├── settings.py       # Cấu hình Django và cơ sở dữ liệu
│   ├── urls.py           # URL chính
│   ├── asgi.py
│   └── wsgi.py
└── products/
    ├── models.py         # Model Product
    ├── serializers.py    # Tuần tự hóa và kiểm tra dữ liệu
    ├── views.py          # Xử lý API
    ├── urls.py           # Các endpoint sản phẩm
    └── authentication.py # Xác thực JWT
```

## 4. Yêu cầu

- Python 3.10 trở lên (nên sử dụng phiên bản tương thích với phiên bản Django đang cài).
- PostgreSQL đang chạy.
- Các thư viện: `Django`, `djangorestframework`, `psycopg` hoặc `psycopg2`, `PyJWT`.

## 5. Cài đặt và chạy dự án

Mở terminal tại thư mục `product_service`.

### Bước 1: Tạo và kích hoạt môi trường ảo

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### Bước 2: Cài thư viện

```bash
pip install Django djangorestframework PyJWT psycopg2-binary
```

Nếu môi trường của bạn dùng driver PostgreSQL khác, hãy cài driver tương ứng. Nên bổ sung các phiên bản thư viện đã kiểm thử vào `requirements.txt` để dễ tái tạo môi trường.

### Bước 3: Cấu hình PostgreSQL

Trong `config/settings.py`, dự án hiện được cấu hình với các giá trị mặc định sau:

| Tham số | Giá trị hiện tại |
|---|---|
| Database | `product_db` |
| User | `postgres` |
| Host | `localhost` |
| Port | `5432` |

Tạo database `product_db` trong PostgreSQL và điều chỉnh `DATABASES` trong `config/settings.py` cho phù hợp với môi trường của bạn. Không nên lưu mật khẩu hoặc khóa bí mật trực tiếp trong mã nguồn khi triển khai thực tế; hãy sử dụng biến môi trường.

### Bước 4: Tạo bảng và chạy server

```bash
python manage.py migrate
python manage.py runserver
```

Mặc định, server chạy tại `http://127.0.0.1:8000/`.

> Lưu ý: cấu hình REST Framework đặt quyền mặc định là `IsAuthenticated`. Vì vậy, các endpoint sản phẩm cần token JWT hợp lệ. Dự án này xác thực token nhưng không có endpoint cấp token được định nghĩa trong các URL hiện tại; hãy lấy token từ hệ thống xác thực phù hợp.

## 6. API endpoints

Tất cả endpoint dưới đây sử dụng đường dẫn tương đối với địa chỉ server, ví dụ `http://127.0.0.1:8000`.

| Phương thức | Endpoint | Mô tả | Thành công |
|---|---|---|---|
| `GET` | `/products` | Lấy danh sách sản phẩm | `200 OK` |
| `POST` | `/products` | Tạo sản phẩm | `201 Created` |
| `GET` | `/products/<id>` | Lấy chi tiết sản phẩm | `200 OK` |
| `PUT` | `/products/<id>` | Cập nhật toàn bộ thông tin sản phẩm | `200 OK` |
| `DELETE` | `/products/<id>` | Xóa sản phẩm | `204 No Content` |

### Header xác thực

```http
Authorization: Bearer <token>
Content-Type: application/json
```

Token được giải mã bằng thuật toán `HS256` và khóa `JWT_SECRET` cấu hình trong `config/settings.py`. Payload token cần tương thích với định dạng mà hệ thống xác thực phát hành.

### Ví dụ: tạo sản phẩm

Request:

```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "name": "Bàn phím cơ",
  "description": "Bàn phím cơ dùng cho máy tính",
  "price": "850000.00",
  "quantity": 10
}
```

Ví dụ dữ liệu trả về khi tạo thành công:

```json
{
  "id": 1,
  "name": "Bàn phím cơ",
  "description": "Bàn phím cơ dùng cho máy tính",
  "price": "850000.00",
  "quantity": 10,
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z"
}
```

Thời gian và ID trong ví dụ chỉ mang tính minh họa.

### Ví dụ: lấy danh sách sản phẩm

```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/products
```

### Ví dụ: xóa sản phẩm

```bash
curl -X DELETE \
  -H "Authorization: Bearer <token>" \
  http://127.0.0.1:8000/products/1
```

## 7. Mô hình dữ liệu Product

| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `id` | AutoField | Khóa chính, tự tăng |
| `name` | CharField(255) | Tên sản phẩm |
| `description` | TextField | Mô tả sản phẩm |
| `price` | DecimalField(10, 2) | Giá sản phẩm, không âm |
| `quantity` | IntegerField | Số lượng, không âm |
| `created_at` | DateTimeField | Thời điểm tạo, tự động thiết lập |
| `updated_at` | DateTimeField | Thời điểm cập nhật gần nhất, tự động cập nhật |

## 8. Mã trạng thái thường gặp

- `200 OK`: request thành công.
- `201 Created`: tạo sản phẩm thành công.
- `204 No Content`: xóa thành công, không có nội dung trả về.
- `400 Bad Request`: dữ liệu không hợp lệ, chẳng hạn giá hoặc số lượng âm.
- `401 Unauthorized`: thiếu token hợp lệ, token sai định dạng hoặc hết hạn.
- `404 Not Found`: không tìm thấy sản phẩm theo ID.

## 9. Kiểm thử

Chạy các bài kiểm thử của ứng dụng bằng lệnh:

```bash
python manage.py test products
```

## 10. Lưu ý bảo mật

- Không đưa `SECRET_KEY`, `JWT_SECRET` hoặc mật khẩu cơ sở dữ liệu thật lên Git.
- Tắt `DEBUG` và cấu hình `ALLOWED_HOSTS` phù hợp trước khi triển khai.
- Nên đọc cấu hình nhạy cảm từ biến môi trường.
- Chỉ sử dụng HTTPS khi triển khai để bảo vệ token trong quá trình truyền tải.

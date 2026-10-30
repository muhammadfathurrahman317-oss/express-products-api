# Express.js REST API - Daftar Produk

Tugas Praktikum Pemrograman Web (Week 9: Materi ExpressJS) - Institut Teknologi Sepuluh Nopember (ITS).

Proyek ini mengimplementasikan RESTful API sederhana menggunakan **Express.js** untuk mengelola data produk menggunakan penyimpanan memori (*in-memory array*, tanpa database). Arsitektur proyek telah menerapkan prinsip pemisahan tanggung jawab (**separation of concerns**) dengan memisahkan *routes* dan *controllers*.

---

## 📁 Struktur Direktori

```text
express-products-api/
├── controllers/
│   └── productController.js   # Logika bisnis (handling request & response)
├── data/
│   └── products.js            # Data awal in-memory array produk
├── routes/
│   └── productRoutes.js       # Pemetaan rute HTTP ke controller
├── app.js                     # Konfigurasi aplikasi Express & middleware
├── index.js                   # Entry point server (listen ke port)
├── package.json               # Konfigurasi dependensi dan script npm
├── test.js                    # Script pengujian otomatis seluruh skenario
└── README.md                  # Dokumentasi proyek & bukti pengujian
```

---

## 🚀 Petunjuk Menjalankan Proyek

### 1. Prasyarat
- **Node.js** (v18 atau lebih baru)
- **npm**

### 2. Instalasi Dependensi
Buka terminal dan masuk ke folder proyek:
```bash
cd express-products-api
npm install
```

### 3. Menjalankan Server
Jalankan perintah:
```bash
npm start
```
Server akan aktif di: `http://localhost:3000`

---

## 📡 Daftar Endpoint API

| No | Metode | Endpoint | Deskripsi | Status Code |
|---|---|---|---|---|
| 1 | `GET` | `/products` | Mengambil seluruh data produk | `200 OK` |
| 2 | `GET` | `/products/:id` | Mengambil data produk berdasarkan ID | `200 OK` (jika ada) / `404 Not Found` |
| 3 | `POST` | `/products` | Menambahkan produk baru | `201 Created` |

---

## 📝 Detail & Contoh Request/Response

### 1. GET `/products`
- **Tujuan**: Mengambil array semua produk.
- **Request**:
  ```bash
  curl -X GET http://localhost:3000/products
  ```
- **Response** (`200 OK`):
  ```json
  [
    {
      "id": 1,
      "name": "Buku",
      "price": 15000
    },
    {
      "id": 2,
      "name": "Pulpen",
      "price": 5000
    }
  ]
  ```

---

### 2. GET `/products/:id` (Ditemukan)
- **Tujuan**: Mengambil produk dengan ID tertentu.
- **Request**:
  ```bash
  curl -X GET http://localhost:3000/products/1
  ```
- **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "name": "Buku",
    "price": 15000
  }
  ```

---

### 3. GET `/products/:id` (Tidak Ditemukan)
- **Tujuan**: Menguji penanganan ketika produk tidak tersedia.
- **Request**:
  ```bash
  curl -X GET http://localhost:3000/products/999
  ```
- **Response** (`404 Not Found`):
  ```json
  {
    "message": "Produk tidak ditemukan"
  }
  ```

---

### 4. POST `/products`
- **Tujuan**: Menambahkan produk baru dengan ID otomatis.
- **Request**:
  ```bash
  curl -X POST http://localhost:3000/products \
    -H "Content-Type: application/json" \
    -d '{"name": "Penggaris", "price": 3000}'
  ```
- **Response** (`201 Created`):
  ```json
  {
    "id": 3,
    "name": "Penggaris",
    "price": 3000
  }
  ```

---

## 🧪 Bukti Pengujian

Pengujian dapat dijalankan secara otomatis menggunakan:
```bash
npm test
```

### Log Output Pengujian Terminal:
```text
> express-products-api@1.0.0 test
> node test.js

Test server running on port 3001

==============================================
1. Uji GET /products
==============================================
HTTP Status: 200
Response JSON:
[
  {
    "id": 1,
    "name": "Buku",
    "price": 15000
  },
  {
    "id": 2,
    "name": "Pulpen",
    "price": 5000
  }
]

==============================================
2. Uji GET /products/1
==============================================
HTTP Status: 200
Response JSON:
{
  "id": 1,
  "name": "Buku",
  "price": 15000
}

==============================================
3. Uji GET /products/999
==============================================
HTTP Status: 404
Response JSON:
{
  "message": "Produk tidak ditemukan"
}

==============================================
4. Uji POST /products
==============================================
Request Body: {"name":"Penggaris","price":3000}
HTTP Status: 201
Response JSON:
{
  "id": 3,
  "name": "Penggaris",
  "price": 3000
}

==============================================
5. Uji GET /products setelah POST (Verifikasi)
==============================================
HTTP Status: 200
Response JSON:
[
  {
    "id": 1,
    "name": "Buku",
    "price": 15000
  },
  {
    "id": 2,
    "name": "Pulpen",
    "price": 5000
  },
  {
    "id": 3,
    "name": "Penggaris",
    "price": 3000
  }
]

==============================================
HASIL PENGUJIAN: SEMUA TARGET BERHASIL TERPENUHI!
==============================================
```

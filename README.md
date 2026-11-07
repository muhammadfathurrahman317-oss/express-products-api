# Express.js REST API Produk dengan Prisma ORM

Proyek ini merupakan implementasi RESTful API untuk mengelola data produk menggunakan **Express.js** dan **Prisma ORM** dengan database engine **SQLite**. Proyek menerapkan pemisahan tanggung jawab (*separation of concerns*) dengan membagi kode ke dalam lapisan *routes*, *controllers*, dan *database models*.

- **Nama:** Muhammad Rifqi Fathurrahman
- **NRP:** 5027251029
- **Mata Kuliah:** Pemrograman Web (Week 10: Integrasi Prisma ORM)

---

## 📁 Struktur Direktori

```text
express-products-api/
├── controllers/
│   └── productController.js   # Logika bisnis & manipulasi database via Prisma
├── lib/
│   └── prisma.js              # Instance Prisma Client singleton
├── prisma/
│   ├── dev.db                 # Database SQLite (dibuat otomatis oleh Prisma)
│   ├── schema.prisma          # Skema model Prisma (Model Product)
│   └── seed.js                # Script seeding data awal (Buku & Pulpen)
├── routes/
│   └── productRoutes.js       # Pemetaan rute HTTP (GET, POST, PUT, DELETE)
├── evidence/                  # Bukti screenshot pengujian Postman & Database
├── scripts/
│   └── generate_evidence.py   # Script otomasi pembuatan gambar evidence
├── app.js                     # Inisialisasi Express & middleware
├── index.js                   # Entry point server (Port 3000)
├── test.js                    # Script pengujian otomatis 12 skenario pengujian
├── LAPORAN_EVIDENCE.md        # Laporan lengkap hasil pengujian & bukti gambar
├── package.json               # Dependensi & script NPM
└── .env.example               # Contoh konfigurasi environment variables
```

---

## 🚀 Petunjuk Menjalankan Proyek

### 1. Prasyarat
- **Node.js** (v18 atau lebih baru)
- **npm**

### 2. Instalasi Dependensi
```bash
npm install
```

### 3. Konfigurasi Environment Variables
Salin file konfigurasi environment:
```bash
cp .env.example .env
```
Isi file `.env`:
```env
DATABASE_URL="file:./dev.db"
PORT=3000
```

### 4. Sinkronisasi Database & Seeding
Jalankan perintah berikut untuk mensinkronisasi schema ke database dan mengisi data awal:
```bash
# Push schema Prisma ke database SQLite
npx prisma db push

# Generate Prisma Client
npx prisma generate

# Seed data awal (ID 1: Buku, ID 2: Pulpen)
npm run seed
```

### 5. Menjalankan Server
```bash
npm start
```
Server akan aktif di `http://localhost:3000`.

### 6. Menjalankan Prisma Studio (Database GUI)
Untuk melihat dan mengelola data langsung di antarmuka browser:
```bash
npm run studio
```

### 7. Menjalankan Pengujian Otomatis
```bash
npm test
```

---

## 📡 Daftar Endpoint API

| No | Metode | Endpoint | Deskripsi | Status Code |
|---|---|---|---|---|
| 1 | `GET` | `/products` | Menampilkan seluruh data produk | `200 OK` |
| 2 | `GET` | `/products/:id` | Mengambil data produk berdasarkan ID | `200 OK` / `404 Not Found` |
| 3 | `POST` | `/products` | Membuat data produk baru | `201 Created` / `400 Bad Request` |
| 4 | `PUT` | `/products` | Mengupdate produk (Body sama dg POST + ID) | `200 OK` / `400 Bad Request` / `404 Not Found` |
| 5 | `PUT` | `/products/:id` | Mengupdate produk melalui parameter ID | `200 OK` / `400 Bad Request` / `404 Not Found` |
| 6 | `DELETE` | `/products/:id` | Menghapus data produk berdasarkan ID | `200 OK` / `404 Not Found` |

---

## 📝 Format Request & Response

### 1. GET `/products`
- **Request:**
  ```bash
  curl -X GET http://localhost:3000/products
  ```
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "name": "Buku",
      "price": 15000,
      "createdAt": "2026-11-07T08:19:42.447Z",
      "updatedAt": "2026-11-07T08:19:42.447Z"
    },
    {
      "id": 2,
      "name": "Pulpen",
      "price": 5000,
      "createdAt": "2026-11-07T08:19:42.447Z",
      "updatedAt": "2026-11-07T08:19:42.447Z"
    }
  ]
  ```

---

### 2. POST `/products`
- **Request:**
  ```bash
  curl -X POST http://localhost:3000/products \
    -H "Content-Type: application/json" \
    -d '{"name": "Penggaris", "price": 3000}'
  ```
- **Response (`201 Created`):**
  ```json
  {
    "id": 3,
    "name": "Penggaris",
    "price": 3000,
    "createdAt": "2026-11-07T08:19:42.486Z",
    "updatedAt": "2026-11-07T08:19:42.486Z"
  }
  ```

---

### 3. PUT `/products` (Body Sama dengan POST namun ada Tambahan ID)
- **Request:**
  ```bash
  curl -X PUT http://localhost:3000/products \
    -H "Content-Type: application/json" \
    -d '{"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000}'
  ```
- **Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Buku Tulis Sinar Dunia",
    "price": 18000,
    "createdAt": "2026-11-07T08:19:42.447Z",
    "updatedAt": "2026-11-07T08:19:42.490Z"
  }
  ```

---

### 4. DELETE `/products/:id`
- **Request:**
  ```bash
  curl -X DELETE http://localhost:3000/products/2
  ```
- **Response (`200 OK`):**
  ```json
  {
    "message": "Produk berhasil dihapus",
    "data": {
      "id": 2,
      "name": "Pulpen",
      "price": 5000,
      "createdAt": "2026-11-07T08:19:42.447Z",
      "updatedAt": "2026-11-07T08:19:42.447Z"
    }
  }
  ```

---

## 🧪 Laporan Evidence & Pengujian

Dokumentasi lengkap bukti pengujian API client (Postman/Hoppscotch) dan screenshot perubahan database before-after dapat dilihat pada file:
👉 **[LAPORAN_EVIDENCE.md](./LAPORAN_EVIDENCE.md)**

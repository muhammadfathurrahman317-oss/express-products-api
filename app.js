require('dotenv').config();
const express = require('express');
const productRoutes = require('./routes/productRoutes');

const app = express();

// Middleware untuk parsing JSON request body
app.use(express.json());

// Mounting route produk
app.use('/products', productRoutes);

// Root endpoint untuk health check
app.get('/', (req, res) => {
  res.json({ message: 'Selamat datang di API Produk Express.js dengan Prisma ORM' });
});

// Middleware 404 Not Found
app.use((req, res) => {
  res.status(404).json({ message: 'Rute tidak ditemukan' });
});

// Centralized Error Handling Middleware
app.use((err, req, res, next) => {
  console.error('Unhandled Error:', err);
  res.status(err.status || 500).json({
    message: err.message || 'Terjadi kesalahan pada internal server',
  });
});

module.exports = app;

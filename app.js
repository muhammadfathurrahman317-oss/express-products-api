const express = require('express');
const productRoutes = require('./routes/productRoutes');

const app = express();

// Middleware untuk parsing JSON request body
app.use(express.json());

// Mounting route produk
app.use('/products', productRoutes);

// Root endpoint untuk health check
app.get('/', (req, res) => {
  res.json({ message: 'Selamat datang di API Produk Express.js' });
});

module.exports = app;

const express = require('express');
const router = express.Router();
const {
  getAllProducts,
  getProductById,
  createProduct,
} = require('../controllers/productController');

// Definisi route untuk produk
router.get('/', getAllProducts);
router.get('/:id', getProductById);
router.post('/', createProduct);

module.exports = router;

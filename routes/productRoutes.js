const express = require('express');
const router = express.Router();
const {
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
} = require('../controllers/productController');

// Definisi route untuk produk
router.get('/', getAllProducts);
router.get('/:id', getProductById);
router.post('/', createProduct);

// PUT mendukung URL param (/products/:id) maupun JSON body (/products dengan body { id, ... })
router.put('/:id', updateProduct);
router.put('/', updateProduct);

// DELETE mendukung URL param (/products/:id) maupun JSON body / query
router.delete('/:id', deleteProduct);
router.delete('/', deleteProduct);

module.exports = router;

const products = require('../data/products');

// GET /products - Mengambil seluruh produk
const getAllProducts = (req, res) => {
  res.status(200).json(products);
};

// GET /products/:id - Mengambil produk berdasarkan ID
const getProductById = (req, res) => {
  const id = parseInt(req.params.id, 10);
  const product = products.find((p) => p.id === id);

  if (!product) {
    return res.status(404).json({ message: 'Produk tidak ditemukan' });
  }

  res.status(200).json(product);
};

// POST /products - Menambahkan produk baru
const createProduct = (req, res) => {
  const { name, price } = req.body;

  if (!name || price === undefined || price === null) {
    return res.status(400).json({ message: 'Field name dan price wajib diisi' });
  }

  // Membuat ID baru secara otomatis
  const newId = products.length > 0 ? Math.max(...products.map((p) => p.id)) + 1 : 1;

  const newProduct = {
    id: newId,
    name: String(name),
    price: Number(price),
  };

  products.push(newProduct);

  res.status(201).json(newProduct);
};

module.exports = {
  getAllProducts,
  getProductById,
  createProduct,
};

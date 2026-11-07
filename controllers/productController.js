const prisma = require('../lib/prisma');

// GET /products - Mengambil seluruh produk dari database
const getAllProducts = async (req, res, next) => {
  try {
    const products = await prisma.product.findMany({
      orderBy: { id: 'asc' },
    });
    res.status(200).json(products);
  } catch (error) {
    next(error);
  }
};

// GET /products/:id - Mengambil produk berdasarkan ID
const getProductById = async (req, res, next) => {
  try {
    const id = parseInt(req.params.id, 10);

    if (isNaN(id)) {
      return res.status(400).json({ message: 'ID produk harus berupa angka valid' });
    }

    const product = await prisma.product.findUnique({
      where: { id },
    });

    if (!product) {
      return res.status(404).json({ message: 'Produk tidak ditemukan' });
    }

    res.status(200).json(product);
  } catch (error) {
    next(error);
  }
};

// POST /products - Membuat produk baru
const createProduct = async (req, res, next) => {
  try {
    const { name, price } = req.body;

    // Validasi field name
    if (name === undefined || name === null || String(name).trim() === '') {
      return res.status(400).json({ message: 'Field name wajib diisi' });
    }

    // Validasi field price
    if (price === undefined || price === null || isNaN(Number(price)) || Number(price) < 0) {
      return res.status(400).json({ message: 'Field price wajib diisi dan harus berupa angka non-negatif' });
    }

    const newProduct = await prisma.product.create({
      data: {
        name: String(name).trim(),
        price: Math.round(Number(price)),
      },
    });

    res.status(201).json(newProduct);
  } catch (error) {
    next(error);
  }
};

// PUT /products atau /products/:id - Mengupdate data produk (body sama dengan post + id)
const updateProduct = async (req, res, next) => {
  try {
    const rawId = req.params.id !== undefined ? req.params.id : req.body?.id;
    const id = parseInt(rawId, 10);

    if (!rawId || isNaN(id)) {
      return res.status(400).json({ message: 'ID produk wajib disertakan dan harus berupa angka valid' });
    }

    const { name, price } = req.body || {};

    // Validasi field name
    if (name === undefined || name === null || String(name).trim() === '') {
      return res.status(400).json({ message: 'Field name wajib diisi' });
    }

    // Validasi field price
    if (price === undefined || price === null || isNaN(Number(price)) || Number(price) < 0) {
      return res.status(400).json({ message: 'Field price wajib diisi dan harus berupa angka non-negatif' });
    }

    // Periksa apakah produk ada di database
    const existingProduct = await prisma.product.findUnique({
      where: { id },
    });

    if (!existingProduct) {
      return res.status(404).json({ message: `Produk dengan ID ${id} tidak ditemukan` });
    }

    const updatedProduct = await prisma.product.update({
      where: { id },
      data: {
        name: String(name).trim(),
        price: Math.round(Number(price)),
      },
    });

    res.status(200).json(updatedProduct);
  } catch (error) {
    next(error);
  }
};

// DELETE /products/:id atau /products - Menghapus produk berdasarkan ID
const deleteProduct = async (req, res, next) => {
  try {
    const rawId = req.params.id !== undefined ? req.params.id : (req.body?.id || req.query?.id);
    const id = parseInt(rawId, 10);

    if (!rawId || isNaN(id)) {
      return res.status(400).json({ message: 'ID produk wajib disertakan dan harus berupa angka valid' });
    }

    // Periksa apakah produk ada di database
    const existingProduct = await prisma.product.findUnique({
      where: { id },
    });

    if (!existingProduct) {
      return res.status(404).json({ message: `Produk dengan ID ${id} tidak ditemukan` });
    }

    const deletedProduct = await prisma.product.delete({
      where: { id },
    });

    res.status(200).json({
      message: 'Produk berhasil dihapus',
      data: deletedProduct,
    });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  getAllProducts,
  getProductById,
  createProduct,
  updateProduct,
  deleteProduct,
};

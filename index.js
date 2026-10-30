const app = require('./app');

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server Express berhasil berjalan di http://localhost:${PORT}`);
  console.log(`Endpoint produk: http://localhost:${PORT}/products`);
});

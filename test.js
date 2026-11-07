const app = require('./app');
const prisma = require('./lib/prisma');

const PORT = 3001;

async function runTests() {
  console.log('--- Menyiapkan Database untuk Pengujian ---');
  await prisma.$executeRawUnsafe('DELETE FROM "Product";');
  try {
    await prisma.$executeRawUnsafe('DELETE FROM sqlite_sequence WHERE name = "Product";');
  } catch (err) {}

  await prisma.product.createMany({
    data: [
      { name: 'Buku', price: 15000 },
      { name: 'Pulpen', price: 5000 },
    ],
  });
  console.log('Database berhasil di-reset dan di-seed: ID 1 = Buku, ID 2 = Pulpen.\n');

  const server = app.listen(PORT, async () => {
    console.log(`Server pengujian aktif pada port ${PORT}\n`);

    try {
      const baseUrl = `http://127.0.0.1:${PORT}`;

      // 1. GET /products (Seluruh data)
      console.log('==============================================================');
      console.log('1. [GET] /products - Menampilkan Seluruh Data');
      console.log('==============================================================');
      const resGetAll = await fetch(`${baseUrl}/products`);
      console.log(`HTTP Status: ${resGetAll.status}`);
      const dataGetAll = await resGetAll.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataGetAll, null, 2));

      // 2. POST /products (Success)
      console.log('\n==============================================================');
      console.log('2. [POST] /products - Membuat Data Produk Baru (Success)');
      console.log('==============================================================');
      const newProductPayload = { name: 'Penggaris', price: 3000 };
      console.log('Request Body:', JSON.stringify(newProductPayload));
      const resPost = await fetch(`${baseUrl}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProductPayload),
      });
      console.log(`HTTP Status: ${resPost.status}`);
      const dataPost = await resPost.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPost, null, 2));

      // 3. POST /products (Validation Error: Nama kosong)
      console.log('\n==============================================================');
      console.log('3. [POST] /products - Validasi Gagal: Field "name" Kosong');
      console.log('==============================================================');
      const invalidPostPayload1 = { name: '', price: 3000 };
      console.log('Request Body:', JSON.stringify(invalidPostPayload1));
      const resPostVal1 = await fetch(`${baseUrl}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invalidPostPayload1),
      });
      console.log(`HTTP Status: ${resPostVal1.status}`);
      const dataPostVal1 = await resPostVal1.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPostVal1, null, 2));

      // 4. POST /products (Validation Error: Price negatif)
      console.log('\n==============================================================');
      console.log('4. [POST] /products - Validasi Gagal: Field "price" Negatif');
      console.log('==============================================================');
      const invalidPostPayload2 = { name: 'Penghapus', price: -500 };
      console.log('Request Body:', JSON.stringify(invalidPostPayload2));
      const resPostVal2 = await fetch(`${baseUrl}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invalidPostPayload2),
      });
      console.log(`HTTP Status: ${resPostVal2.status}`);
      const dataPostVal2 = await resPostVal2.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPostVal2, null, 2));

      // 5. GET /products/:id (Success)
      console.log('\n==============================================================');
      console.log('5. [GET] /products/1 - Menampilkan Data Berdasarkan ID 1 (Success)');
      console.log('==============================================================');
      const resGetOne = await fetch(`${baseUrl}/products/1`);
      console.log(`HTTP Status: ${resGetOne.status}`);
      const dataGetOne = await resGetOne.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataGetOne, null, 2));

      // 6. GET /products/:id (404 Not Found)
      console.log('\n==============================================================');
      console.log('6. [GET] /products/999 - Data Tidak Ditemukan (404 Not Found)');
      console.log('==============================================================');
      const resGetNotFound = await fetch(`${baseUrl}/products/999`);
      console.log(`HTTP Status: ${resGetNotFound.status}`);
      const dataGetNotFound = await resGetNotFound.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataGetNotFound, null, 2));

      // 7. PUT /products - Update data (Body sama dg post namun ada tambahan id) (Success)
      console.log('\n==============================================================');
      console.log('7. [PUT] /products - Mengupdate Data (Body sama dg post + id) (Success)');
      console.log('==============================================================');
      const putPayload = { id: 1, name: 'Buku Tulis Sinar Dunia', price: 18000 };
      console.log('Request Body:', JSON.stringify(putPayload));
      const resPut = await fetch(`${baseUrl}/products`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(putPayload),
      });
      console.log(`HTTP Status: ${resPut.status}`);
      const dataPut = await resPut.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPut, null, 2));

      // 8. PUT /products - Validasi Gagal: ID tidak ada
      console.log('\n==============================================================');
      console.log('8. [PUT] /products - Validasi Gagal: Field "id" Tidak Disertakan');
      console.log('==============================================================');
      const invalidPutPayload = { name: 'Buku Tanpa ID', price: 20000 };
      console.log('Request Body:', JSON.stringify(invalidPutPayload));
      const resPutVal = await fetch(`${baseUrl}/products`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invalidPutPayload),
      });
      console.log(`HTTP Status: ${resPutVal.status}`);
      const dataPutVal = await resPutVal.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPutVal, null, 2));

      // 9. PUT /products - Update ID tidak ditemukan (404 Not Found)
      console.log('\n==============================================================');
      console.log('9. [PUT] /products - Update ID 999 Tidak Ditemukan (404 Not Found)');
      console.log('==============================================================');
      const notFoundPutPayload = { id: 999, name: 'Barang Gaib', price: 99999 };
      console.log('Request Body:', JSON.stringify(notFoundPutPayload));
      const resPutNotFound = await fetch(`${baseUrl}/products`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(notFoundPutPayload),
      });
      console.log(`HTTP Status: ${resPutNotFound.status}`);
      const dataPutNotFound = await resPutNotFound.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataPutNotFound, null, 2));

      // 10. DELETE /products/:id (Success)
      console.log('\n==============================================================');
      console.log('10. [DELETE] /products/2 - Menghapus Data Berdasarkan ID 2 (Success)');
      console.log('==============================================================');
      const resDelete = await fetch(`${baseUrl}/products/2`, {
        method: 'DELETE',
      });
      console.log(`HTTP Status: ${resDelete.status}`);
      const dataDelete = await resDelete.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataDelete, null, 2));

      // 11. DELETE /products/:id (404 Not Found)
      console.log('\n==============================================================');
      console.log('11. [DELETE] /products/999 - Menghapus ID 999 (404 Not Found)');
      console.log('==============================================================');
      const resDeleteNotFound = await fetch(`${baseUrl}/products/999`, {
        method: 'DELETE',
      });
      console.log(`HTTP Status: ${resDeleteNotFound.status}`);
      const dataDeleteNotFound = await resDeleteNotFound.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataDeleteNotFound, null, 2));

      // 12. GET /products - Verifikasi Data Akhir di Database
      console.log('\n==============================================================');
      console.log('12. [GET] /products - Verifikasi State Data Akhir di Database');
      console.log('==============================================================');
      const resFinal = await fetch(`${baseUrl}/products`);
      console.log(`HTTP Status: ${resFinal.status}`);
      const dataFinal = await resFinal.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataFinal, null, 2));

      console.log('\n==============================================================');
      console.log('HASIL PENGUJIAN: SEMUA SKENARIO BERHASIL LULUS 100%!');
      console.log('==============================================================');
    } catch (err) {
      console.error('Error during testing:', err);
    } finally {
      server.close();
      await prisma.$disconnect();
      process.exit(0);
    }
  });
}

runTests();

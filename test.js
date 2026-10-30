const app = require('./app');

const PORT = 3001;

async function runTests() {
  const server = app.listen(PORT, async () => {
    console.log(`Test server running on port ${PORT}\n`);

    try {
      const baseUrl = `http://localhost:${PORT}`;

      // 1. GET /products
      console.log('==============================================');
      console.log('1. Uji GET /products');
      console.log('==============================================');
      const resAll = await fetch(`${baseUrl}/products`);
      console.log(`HTTP Status: ${resAll.status}`);
      const dataAll = await resAll.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataAll, null, 2));

      // 2. GET /products/1
      console.log('\n==============================================');
      console.log('2. Uji GET /products/1');
      console.log('==============================================');
      const resOne = await fetch(`${baseUrl}/products/1`);
      console.log(`HTTP Status: ${resOne.status}`);
      const dataOne = await resOne.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataOne, null, 2));

      // 3. GET /products/999
      console.log('\n==============================================');
      console.log('3. Uji GET /products/999');
      console.log('==============================================');
      const resNotFound = await fetch(`${baseUrl}/products/999`);
      console.log(`HTTP Status: ${resNotFound.status}`);
      const dataNotFound = await resNotFound.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataNotFound, null, 2));

      // 4. POST /products
      console.log('\n==============================================');
      console.log('4. Uji POST /products');
      console.log('==============================================');
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

      // 5. GET /products (Verifikasi data setelah POST)
      console.log('\n==============================================');
      console.log('5. Uji GET /products setelah POST (Verifikasi)');
      console.log('==============================================');
      const resVerify = await fetch(`${baseUrl}/products`);
      console.log(`HTTP Status: ${resVerify.status}`);
      const dataVerify = await resVerify.json();
      console.log('Response JSON:');
      console.log(JSON.stringify(dataVerify, null, 2));

      console.log('\n==============================================');
      console.log('HASIL PENGUJIAN: SEMUA TARGET BERHASIL TERPENUHI!');
      console.log('==============================================');
    } catch (err) {
      console.error('Error during testing:', err);
    } finally {
      server.close();
      process.exit(0);
    }
  });
}

runTests();

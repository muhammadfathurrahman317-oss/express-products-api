const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  console.log('Clearing existing product data and resetting ID sequence...');
  await prisma.$executeRawUnsafe('DELETE FROM "Product";');
  try {
    await prisma.$executeRawUnsafe('DELETE FROM sqlite_sequence WHERE name = "Product";');
  } catch (err) {
    // sqlite_sequence might not exist yet if table is empty
  }

  console.log('Seeding initial products...');
  const initialProducts = [
    { name: 'Buku', price: 15000 },
    { name: 'Pulpen', price: 5000 },
  ];

  for (const product of initialProducts) {
    const created = await prisma.product.create({
      data: product,
    });
    console.log(`Created product with id: ${created.id} - ${created.name} (Rp ${created.price})`);
  }

  console.log('Seeding completed successfully!');
}

main()
  .catch((e) => {
    console.error('Error seeding data:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

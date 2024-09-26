import express from "express";
import redis from "redis";
import { promisify } from "util";

// List of products
const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

/**
 * Get a product by its ID
 * @param {number} id - The ID of the product
 * @returns {object} - The product object
 */
function getItemById(id) {
  return listProducts.filter((item) => item.itemId === id)[0];
}

// Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

client.on("error", (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

/**
 * Reserve stock for a product by its ID
 * @param {number} itemId - The ID of the product
 * @param {number} stock - The quantity of stock to reserve
 */
function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

/**
 * Get the current reserved stock for a product by its ID
 * @param {number} itemId - The ID of the product
 * @returns {Promise<number|null>} - The current reserved stock or null if not found
 */
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock;
}

// Express app
const app = express();
const port = 1245;

const notFound = { status: "Product not found" };

app.listen(port, () => {
  console.log(`app listening at http://localhost:${port}`);
});

/**
 * Get the list of products
 */
app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

/**
 * Get a product by its ID
 * @param {number} itemId - The ID of the product
 */
app.get("/list_products/:itemId", async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json(notFound);
    return;
  }

  const currentStock = await getCurrentReservedStockById(itemId);
  const stock =
    currentStock !== null ? currentStock : item.initialAvailableQuantity;

  item.currentQuantity = stock;
  res.json(item);
});

/**
 * Reserve a product by its ID
 * @param {number} itemId - The ID of the product
 */
app.get("/reserve_product/:itemId", async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  const noStock = { status: "Not enough stock available", itemId };
  const reservationConfirmed = { status: "Reservation confirmed", itemId };

  if (!item) {
    res.json(notFound);
    return;
  }

  let currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === null) currentStock = item.initialAvailableQuantity;

  if (currentStock <= 0) {
    res.json(noStock);
    return;
  }

  reserveStockById(itemId, Number(currentStock) - 1);

  res.json(reservationConfirmed);
});

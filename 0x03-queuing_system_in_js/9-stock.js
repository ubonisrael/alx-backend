#!/usr/bin/env node
"use strict";
import Express, { json } from "express";
import util from "util";
import { createClient, print } from "redis";

const client = createClient();

client.on("error", (err) =>
  console.log(`Redis client not connected to the server: ${err}`)
);

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

const getItemValue = util.promisify(client.get).bind(client);

const listProducts = [
  { Id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { Id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { Id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { Id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

const reserveStockById = (itemId, stock) => {
  client.set(itemId, stock, print);
};

const getCurrentReservedStockById = async (itemId) => {
  try {
    const stock = await getItemValue(itemId);
    return stock;
  } catch (err) {
    return err;
  }
};

const getItemById = (id) => listProducts.find((product) => product.Id === Number(id));

const app = Express();

app.get("/list_products", (req, res, next) => {
  res.status(200).json(listProducts);
});

app.get("/list_products/:id", async (req, res, next) => {
  const { id } = req.params;
  const item = getItemById(id);
  const stock = await getCurrentReservedStockById(id);
  if (!stock) {
    res.status(404).json({ status: "Product not found" });
  } else {
    console.log(item.stock, stock);
    const response = {
      itemId: id,
      itemName: item['name'],
      price: item['price'],
      initialAvailableQuantity: item['stock'],
      currentQuantity: item['stock'] - Number(stock),
    };
    res.status(200).json(response);
  }
});

app.get("/reserve_product/:itemId", async (req, res, next) => {
  const { itemId } = req.params;
  const item = getItemById(itemId);
  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    if (!stock || Number(stock) < item['stock']) {
      reserveStockById(itemId, stock ? Number(stock) + 1 : 1);
      res.status(200).json({ status: "Reservation confirmed", itemId });
    } else {
      res.status(400).json({ status: "Not enough stock available", itemId });
    }
  } else {
    res.status(404).json({ status: "Product not found" });
  }
});

app.listen(1245);

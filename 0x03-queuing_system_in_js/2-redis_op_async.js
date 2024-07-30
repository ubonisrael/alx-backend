#!/usr/bin/env node
"use strict";
import redis from "redis";
import util from "util";

const client = redis.createClient();

client.on("error", (err) =>
  console.log(`Redis client not connected to the server: ${err}`)
);

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, redis.print);
};

const getCLientValue = util.promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
    try {
        const reply = await getCLientValue(schoolName)
        console.log(reply)
    } catch(err) {
        console.log(err)
    }
};

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");

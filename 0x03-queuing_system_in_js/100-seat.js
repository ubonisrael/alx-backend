#!/usr/bin/env node
import { createClient, print } from "redis";
import util from "util";
import Express from "express";
import { createQueue } from "kue";

const client = createClient();

let reservationEnabled = true;

const reserveSeat = (number) => {
  client.set("available_seats", number, print);
};

const getCurrentAvailableSeats = async () => {
  const func = util.promisify(client.get).bind(client);
  const result = await func("available_seats");
  return result;
};

const queue = createQueue();

const app = Express();

app.get("/available_seats", async (req, res, next) => {
  const available_seats = await getCurrentAvailableSeats();
  res.status(200).json({ numberOfAvailableSeats: available_seats });
});

app.get("/reserve_seat", async (req, res, next) => {
  if (reservationEnabled) {
    // Creates and queues a job in the queue reserve_seat
    const job = queue
      .create("reserve_seat", {
        details: "reserve a seat",
      })
      .save((err) => {
        if (err) {
          res.status(400).json({ status: "Reservation failed" });
        } else {
          res.status(201).json({ status: "Reservation in process" });
        }
      });
    job
      .on("complete", (result) => {
        console.log(`Seat reservation job #${job.id} completed`);
      })
      .on("failed", (err) => {
        console.log(`Seat reservation job #${job.id} failed: ${err.message}`);
      });

    job.save();
  } else {
    res.status(400).json({ status: "Reservation are blocked" });
  }
});

app.get('/process', (req, res, next) => {
    queue.process('reserve_seat', async(job, done) => {
        let availableSeats = Number(await getCurrentAvailableSeats())
        availableSeats--
        reserveSeat(availableSeats)
        if (availableSeats >= 0) {
            if (availableSeats === 0) reservationEnabled =  false
            done()
        } else {
            done(new Error('Not enough seats available'))
            return
        }
    })
    res.status(200).json({ status: "Queue processing" })
})

app.listen(1245, () => {
  reserveSeat(50);
});

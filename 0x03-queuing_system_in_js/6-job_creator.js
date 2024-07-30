#!/usr/bin/env node
"use strict";
import { createQueue } from "kue";

const queue = createQueue();

const jobData = {
  phoneNumber: "090XXXXXXX",
  message: "I ❤️ u xoxo much",
};

const job = queue.create("push_notification_code", jobData).save((err) => {
  if (err) {
    console.log("Notification job failed");
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

job.on("complete", (result) => {
  console.log("Notification job completed");
});

job.on("failed", (err) => {
  console.log("Notification job failed");
});

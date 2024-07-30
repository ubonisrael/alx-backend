#!/usr/bin/env node
"use strict";

const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error("Jobs is not an array");
  }

  for (const data of jobs) {
    const job = queue.create("push_notification_code_3", data);

    job
      .on("enqueue", () => {
        console.log(`Notification job created: ${job.id}`);
      })
      .on("complete", (result) => {
        console.log(`Notification job #${job.id} completed`);
      })
      .on("failed", (err) => {
        console.log(`Notification job #${job.id} failed: ${err.message}`);
      })
      .on("progress", function (progress, data) {
        console.log(`Notification job #${job.id} ${progress}% complete`);
      });

      job.save()
  }
};

export default createPushNotificationsJobs;

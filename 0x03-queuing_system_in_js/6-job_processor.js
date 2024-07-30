#!/usr/bin/env node
"use strict";
import { createQueue } from "kue";

const queue = createQueue();

const sendNotification = (phoneNumber, message) => {
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

queue.process('push_notification_code', (job, done) => {
    // console.log(job);
    sendNotification(job.data.phoneNumber, job.data.message)
    done()      
})

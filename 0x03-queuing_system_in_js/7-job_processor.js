#!/usr/bin/env node
"use strict";
import { createQueue } from "kue";

const queue = createQueue();

const blackList = ['4153518780', '4153518781']

const sendNotification = (phoneNumber, message, job, done) => {
    let total_time = 10, time_remaining = 10

    const interval = setInterval(() => {
        if (total_time - time_remaining <= total_time * 0.5) {
            job.progress(total_time - time_remaining, total_time)
        }
        if (blackList.includes(phoneNumber)) {
            done(new Error(`Phone number ${phoneNumber} is blacklisted`))
            clearInterval(interval)
            return
        }

        if (total_time === time_remaining) {
            console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
        }

        time_remaining--;
        if (time_remaining === 0) {
            done()
            clearInterval(interval)
        }
    }, 100)
}

queue.process('push_notification_code_2', (job, done) => {
    // console.log(job);
    sendNotification(job.data.phoneNumber, job.data.message, job, done)     
})

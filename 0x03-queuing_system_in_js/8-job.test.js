import { createQueue } from "kue";
import createPushNotificationsJobs from "./8-job";
import { expect } from "chai";
import Sinon from "sinon";

describe("createPushNotificationsJobs", () => {
  const queue = createQueue();
  const spy = Sinon.spy(console)

  before(() => {
    queue.testMode.enter(true);
  });
    afterEach(() => {
      spy.log.resetHistory()
    });
  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it("display error if jobs is not an array", () => {
    expect(
      createPushNotificationsJobs.bind(createPushNotificationsJobs, {}, queue)
    ).to.throw("Jobs is not an array");
  });
  it("create 2 new jobs", (done) => {
    expect(queue.testMode.jobs.length).to.be.equal(0);
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "4153518780",
          message: "This is the code 1234 to verify your account",
        },
        {
          phoneNumber: "2153518780",
          message: "This is the code 1234 to verify your account",
        },
      ],
      queue
    );
    expect(queue.testMode.jobs.length).to.be.equal(2);
    expect(queue.testMode.jobs[0].type).to.be.equal("push_notification_code_3");
    expect(queue.testMode.jobs[0].data).to.be.deep.equal({
      phoneNumber: "4153518780",
      message: "This is the code 1234 to verify your account",
    });
    expect(queue.testMode.jobs[1].type).to.equal("push_notification_code_3");
    expect(queue.testMode.jobs[1].data).to.be.deep.equal({
      phoneNumber: "2153518780",
      message: "This is the code 1234 to verify your account",
    });
    done();
  });

  it('registers the progress event handler for a new job', (done) => {
    queue.testMode.jobs[0].addListener('progress', () => {
      expect(
        spy.log
          .calledWith(`Notification job #${queue.testMode.jobs[0].id} 10% complete`)
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('progress', 10);
  });
  it('registers the fail handler for a new job', (done) => {
    queue.testMode.jobs[0].addListener('failed', () => {
      expect(
        spy.log
          .calledWith(`Notification job #${queue.testMode.jobs[0].id} failed: Failed to send`)
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });
  it('registers the complete handler for a new job', (done) => {
    queue.testMode.jobs[0].addListener('complete', () => {
      expect(
        spy.log
          .calledWith(`Notification job #${queue.testMode.jobs[0].id} completed`)
      ).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('complete');
  });
});

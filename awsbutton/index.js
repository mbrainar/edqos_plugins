'use strict';

console.log('Loading function');

var AWS = require('aws-sdk');
var request = require('request');

let tag = process.env.tag;
let application = process.env.application
let headers = {
    'Content-Type':     'application/x-www-form-urlencoded'
}

exports.handler = (event, context, callback) => {
    // Load the message passed into the Lambda function into a JSON object
    var eventText = JSON.stringify(event, null, 2);
    var messageText = "Received  " + event.clickType + " message from button ID: " + event.serialNumber;
    let url = "http://demoapp.rumrunner.io:5001/api/relevance/";

    // Write the string to the console
    console.log("Message to send: " + messageText);

    if (event.clickType == "SINGLE") {
        console.log("Single click detected. Setting amazon-instant-video to relevant in ed-qos policy.");

        var options = {
          url: url,
          method: "POST",
          headers: headers,
          form: { policy: tag, app: application, relevance: 'Business-Relevant' }
        }

        request(options,
            (error, response, body) => {
            if (!error & response.statusCode == 200) {
              callback(null, 'Successfully set to relevant.');
            } else {
              callback(new Error('Unable to set as relevant.'));
            }
        } );

    } else if (event.clickType == "DOUBLE") {
        console.log("Double click detected. Setting amazon-instant-video to irrelevant in ed-qos policy.");

        var options = {
          url: url,
          method: "POST",
          headers: headers,
          form: { policy: tag, app: application, relevance: 'Business-Irrelevant' }
        }

        request(options,
          (error, response, body) => {
            if (!error & response.statusCode == 200) {
              callback(null, 'Successfully set to relevant.');
            } else {
              callback(new Error('Unable to set as relevant.'));
            }
          });
    }

    callback(null, "The button was pressed, and some things happened.");

};

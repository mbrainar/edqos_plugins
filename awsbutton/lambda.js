'use strict';

console.log('Loading function');

var AWS = require('aws-sdk');

let tag = "test";
let application = "amazon-instant-video";
let paramroot = "policy=test&app=amazon-instant-video&relevance=";

exports.handler = (event, context, callback) => {
    // Load the message passed into the Lambda function into a JSON object
    var eventText = JSON.stringify(event, null, 2);
    var messageText = "Received  " + event.clickType + " message from button ID: " + event.serialNumber;
    let url = "http://demoapp.rumrunner.io:5001/api/relevance";

    // Write the string to the console
    console.log("Message to send: " + messageText);

    if (event.clickType == "SINGLE") {
        console.log("Single click detected. Setting amazon-instant-video to relevant in ed-qos policy.");
        let xhr = new XMLHttpRequest();

        var params = paramroot + "Business-Relevant";
        xhr.open('POST', url, true);
        xhr.onreadystatechange=handler;
        xhr.responsetype='json';
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
        xhr.send(params);

    } else if (event.clickType == "DOUBLE") {
        console.log("Double click detected. Setting amazon-instant-video to irrelevant in ed-qos policy.");
        let xhr = new XMLHttpRequest();

        var params = paramroot + "Business-Irrelevant";
        xhr.open('POST', url, true);
        xhr.onreadystatechange=handler;
        xhr.responsetype='json';
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
        xhr.send(params);
    }
    function handler() {
      if (this.readyState == this.DONE ) {
        if (this.status == 200) {
          callback(null, "The button was pressed, and some things happened.");
        } else {
          callback(1, "The button was pressed, and no things happened. Sorry man.");
        }
      }
    }

};

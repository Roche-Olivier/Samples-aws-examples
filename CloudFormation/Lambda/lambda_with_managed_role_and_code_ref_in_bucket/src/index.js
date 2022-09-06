const aws = require("aws-sdk");

// Set the region 
aws.config.update({ region: 'af-south-1' });

// Create S3 service object
const s3 = new aws.S3({ apiVersion: '2006-03-01' });

exports.handler = async(event) => {
    return "hello from lambda"
};
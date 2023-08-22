const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// Cloud Function action
async function main(params) {
    const couchUrl = 'https://6b1e2b53-8193-4d87-a59c-62b629530127-bluemix.cloudantnosqldb.appdomain.cloud';
    const iamApiKey = 'klrYHIbvrBFwi-BzzoUYVVHMkVyg7GpIRiC5gpXMSm_y';

    // Create an instance of CloudantV1 with IAM authentication
    const authenticator = new IamAuthenticator({
        apikey: iamApiKey,
    });

    const cloudant = new CloudantV1({
        authenticator,
        serviceUrl: couchUrl,
    });

    try {
        // Use the Cloudant instance to interact with the database
        const response = await cloudant.getAllDbs();

        return {
            statusCode: 200,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(response.result)
        };
    } catch (error) {
        console.error(error);
        return {
            statusCode: 500,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Internal server error', details: error.message })
        };
    }
}

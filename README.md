# Chimera Slack Notification

This template demonstrates how to develop and deploy a simple SQS-based producer-consumer service running on AWS Lambda using the Serverless Framework and the [Lift](https://github.com/getlift/lift) plugin. The messages are then forwarded to slack.

### Requirement

-   NodeJs
-   Yarn (Install globally, you can also use npm CLI tool)
-   Serverless
-   Docker

### Install Serverless

```
yarn global add serverless
```

### Deployment

Ensure proper `AWS_PROFILE` with credential is set in terminal session.

Install dependencies with:

```
yarn
```

Then deploy:

```
yarn deploy
```

After running deploy, you should see output similar to:

```bash
Deploying chimera-slack-notification to stage dev (us-west-2)

✔ Service deployed to stack chimera-slack-notification-dev (67s)

functions:
  jobsWorker: chimera-slack-notification-dev-jobsWorker (1.3 MB)
jobs: https://sqs.us-west-2.amazonaws.com/436445528296/chimera-slack-notification-dev-jobs
```

### Why Docker

Lambda runs on Amazon Linux under the hood and sometimes, packaging dependencies with other operating system sometimes lead to cryptographic errors. Hence the need to package with an Amazon Linux docker image.

If you want to package and deploy without using docker, run the following:

To ensure serverless loads AWS credentials from config file

```
export AWS_SDK_LOAD_CONFIG=1
```

Delete the generated package

```
rm -rf ./.serverless-docker
```

Package the lambda

```
sls package -p .serverless-docker
```

Deploy to AWS

```
sls deploy -p .serverless-docker
```

### Destroy Deployment

Run

```
yarn destroy
```

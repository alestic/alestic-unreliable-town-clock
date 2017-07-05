# TownClock.io - Unreliable Town Clock

This repository contains an AWS Lambda function that powers the public
SNS topic with quarter hour chimes anybody can use to trigger AWS Lambda
functions or SQS.

For more information on what the service does and how to use it,
please read the following article:

> Schedule Recurring AWS Lambda Invocations With The Unreliable Town Clock (UTC)

> https://alestic.com/2015/05/aws-lambda-recurring-schedule/

Notes:

- This repository does not explain all of the steps necessary to set
  up your own TownClock. This assumes the pre-existence of the SNS
  topic, AWS Lambda function, CloudWatch Scheuduled Event Rule, and
  IAM permissions.

# s3-monitoring-lambda

This Terraform module deploys a AWS Lambda function to monitor a S3 bucket.

The following resources will be created:
- AWS Lambda function 
- CloudWatch/EventBridge event rule and target
- IAM role

## Usage
Usage example with Slack webhook.
```hcl
module s3_unmoved_alarm {
    for_each    = { for alarm in local.workspace.unmoved_s3_alarm : alarm.name => alarm }
    source      = "./unmoved_alarm"
    name        = each.value.name
    cron_start  = each.value.cron_start
    cron_step   = each.value.cron_step
    cron_stop   = each.value.cron_stop
    cron_rest   = each.value.cron_rest
    bucket_name = "bucket"
    webhook_url = "https://hooks.slack.com/services/?/?/?"
}
```

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.
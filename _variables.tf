variable "name" {
  default = "default-alarm"
}

variable "cron_start" {
  description = "Define hour of the day when to start triggering alarms"
}

variable "enable_start" {
  default = true
}

variable "cron_stop" {
  description = "Define hour of the day when to stop triggering alarms"
}

variable "enable_stop" {
  default = true
}

variable "cron_step" {
  description = "Define interval in minutes for triggering an alarm"
}

variable "cron_rest" {
  description = "The remaining part of the cron expression for triggering an alarm"
}

variable "output_name" {
  description = "Name to function's deployment package into local filesystem"
  default = "lambda_dir.zip"
}

variable "bucket_name" {
  description = "Name of the bucket to monitor"
}

variable "webhook_url" {
  description = "URL to the Slack webhook"
}

variable "sns_email" {
  description = "Email address for SNS notification"
}
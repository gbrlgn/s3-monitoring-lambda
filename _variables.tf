variable "bucket_name" {
  description = "Name of the bucket to monitor"
}

variable "cron_start" {
  description = "Define hour of the day when to start triggering alarms"
}

variable "cron_stop" {
  description = "Define hour of the day when to stop triggering alarms"
}

variable "cron_step" {
  description = "Define interval in minutes for triggering an alarm"
}

variable "cron_rest" {
  description = "The remaining part of the cron expression for triggering an alarm"
}

variable "enable_start" {
  default = true
}

variable "enable_stop" {
  default = true
}

variable "name" {
  default = "default-alarm"
}

variable "output_name" {
  description = "Name to function's deployment package into local filesystem"
  default = "lambda_dir.zip"
}

variable "sns_email" {
  description = "Email address for SNS notification"
}

variable "webhook_url" {
  description = "URL to the Slack webhook"
}
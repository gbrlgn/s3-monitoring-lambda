resource "aws_cloudwatch_event_rule" "s3_alarm_lambda_start" {
  name                = "s3-alarm-lambda-start-${var.name}"
  description         = "Run Lambda checking for unmoved files every 5 minutes and notify of such files via Slack"
  schedule_expression = "cron(${var.cron_step} ${var.cron_start}-${var.cron_stop} ${var.cron_rest})"
  is_enabled          = var.enable_start
  tags                = { Environment = var.name }
}

resource "aws_cloudwatch_event_target" "s3_alarm_lambda_start_target" {
  rule      = aws_cloudwatch_event_rule.s3_alarm_lambda_start.name
  target_id = "s3-alarm-lambda-start-${var.name}"
  arn       = aws_lambda_function.s3_alarm_lambda.arn

  input = <<EOI
    {
      "action": "start"
    }
    EOI
}
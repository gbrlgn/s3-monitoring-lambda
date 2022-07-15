resource "aws_cloudwatch_event_rule" "s3_monitoring_lambda_start" {
  name                = "s3-monitoring-lambda-start-${var.name}"
  description         = "Run Lambda every 5 minutes"
  schedule_expression = "cron(${var.cron_step} ${var.cron_start}-${var.cron_stop} ${var.cron_rest})"
  is_enabled          = var.enable_start
  tags                = { Environment = var.name }
}

resource "aws_cloudwatch_event_target" "s3_monitoring_lambda_start_target" {
  rule      = aws_cloudwatch_event_rule.s3_monitoring_lambda_start.name
  target_id = "s3-monitoring-lambda-start-${var.name}"
  arn       = aws_lambda_function.s3_monitoring_lambda.arn

  input = <<EOI
    {
      "action": "start"
    }
    EOI
}
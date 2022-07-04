data "archive_file" "create_dist_pkg" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_function"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "s3_alarm_lambda" {
  function_name = "${var.name}-s3-alarm-${var.name}"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "unmoved_alarm.lambda_handler"
  filename      = data.archive_file.create_dist_pkg.output_path
  runtime       = "python3.9"
  timeout       = 15
  tags          = { Environment = var.name }
  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
      WEBHOOK_URL = var.webhook_url
      SNS_ARN     = aws_sns_topic.s3_monitoring.arn
    }
  }
}

resource "aws_lambda_permission" "s3_alarm_lambda_start_perm" {
  statement_id  = "AllowExecutionFromCloudWatchStart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_alarm_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.s3_alarm_lambda_start.arn
}

output "arn" {
  value = aws_lambda_function.s3_alarm_lambda.arn
}

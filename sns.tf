resource "aws_sns_topic" "s3_monitoring" {
  name = "s3_monitoring"
}

resource "aws_sns_topic_subscription" "s3_monitoring_target" {
  topic_arn = aws_sns_topic.s3_monitoring.arn
  protocol  = "email"
  endpoint  = var.sns_email
}
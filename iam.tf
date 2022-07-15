resource "aws_iam_role" "s3_monitoring_role" {
  name = "iam_for_lambda"
  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      },
      {
        "Action": [
          "sns:Publish",
          "sns:Subscribe"
        ],
        "Effect": "Allow",
        "Resource": [
            "${aws_sns_topic.s3_monitoring.arn}"
        ]
      }
    ]
  }
  EOF
}
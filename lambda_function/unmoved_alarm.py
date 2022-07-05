"""This module requires os for environment variable resolution, boto3 for AWS
integration, datetime and timezone for last_modified attribute calculations,
botocore's exceptions to use the ClientError exception and Slack's SDK to create
webhooks. BUCKET_NAME, WEBHOOK_URL and SNS_ARN must be passed as environment
variables via Terraform's module declaration.
"""


import os
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from slack_sdk.webhook import WebhookClient


bucket_name = os.environ["BUCKET_NAME"]
webhook = os.environ["WEBHOOK_URL"]
sns_arn = os.environ["SNS_ARN"]


def lambda_handler(event, context):
    """This function accesses a S3 bucket via Session and creates a generator
    for all its objects, filtering out the ones with the last_modified key set
    to more than 5 minutes from the start of the Lambda function's execution.
    The time each object is resting unmodified is then calculated and set to a
    variable. If the access and filtering doesn't raise any exceptions, the
    send_alert function is called passing a webhook, the object and bucket
    names and the number of minutes the object has rested unmodified. In case
    of exceptions, the send_error function is called by passing a webhook and
    either a specific error message string or a string of the error object.
    """
    try:
        s3 = boto3.session.Session().resource("s3")
        bucket = s3.Bucket(bucket_name)
        gn_objects = (obj for obj in bucket.objects.all())
        now = datetime.now(timezone.utc)
        timestamps = filter(
            lambda obj: ((now - obj.last_modified)
                         .total_seconds() / 60.0) > 5,
            gn_objects
        )
        for x in timestamps:
            if x.key != "/":
                x_mins = int((now - x.last_modified)
                             .total_seconds() / 60.0)
                send_alert(webhook, x.key, x.bucket_name, x_mins)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            msg = "[LAMBDA] Erro: Bucket não encontrado ({bucket_name})."
        elif e.response['Error']['Code'] == 'NoSuchKey':
            msg = "[LAMBDA] Erro: Nome errado do objeto."
        elif e.response['Error']['Code'] == 'InternalError':
            msg = "[LAMBDA] Erro: Erro interno no S3."
        else:
            msg = str(e.response['Error'])
        send_error(webhook, msg)


def send_alert(wh, obj_k, obj_bn, obj_mins):
    """This function sends a notification via webhook or email, by using SNS,
    and takes a webhook object, a S3 object's key, its bucket name and the
    number of minutes passed since it was last modified. The function then
    resolves the object's path and name by splitting slash characters and then
    formats the notification string to be sent by the webhook and by SNS.
    """
    headers = {"Content-Type": "application/json"}
    data = {"text": "Lambda webhook"}

    obj_name = (str(obj_k.split("/")[-1]) if "/" in obj_k
                else str(obj_k))

    if "/" in obj_k:
        dir_split = obj_k.split("/")
        obj_dir = ""
        for i in range(len(dir_split) - 1):
            obj_dir = obj_dir + dir_split[i] + "/"
    else:
        obj_dir = "raiz"  # root dir

    webhook = WebhookClient(wh)
    if webhook is not None:
        try:
            wh_response = webhook.send(
                text=f'''
                [LAMBDA] Atenção: O objeto {obj_name} está há {obj_mins} minutos no diretório {obj_dir} do bucket {obj_bn}.
                '''
            )
            print(wh_response)
        except Exception as e:
            print(str(e))

    try:
        sns = boto3.client("sns")
        em_response = sns.publish(
            TopicArn=sns_arn,
            Message=f'''
            Atenção: O objeto {obj_name} está há {obj_mins} minutos no diretório {obj_dir} do bucket {obj_bn}.
            ''',
            Subject="[LAMBDA]"
        )
        print(em_response)
    except Exception as e:
        print(str(e))


def send_error(wh, err_msg):
    """This function sends an error notification via webhook or email, much
    like send_alert, and takes a webhook and an error message string. This
    message can and should be customized, e.g. lambda_handler's except clause,
    but can also receive an error object converted into string by using the str
    function or similar.
    """
    headers = {"Content-Type": "application/json"}
    data = {"text": "Lambda webhook error"}

    webhook = WebhookClient(wh)
    if webhook is not None:
        try:
            wh_response = webhook.send(text=err_msg)
            print(wh_response)
        except Exception as e:
            print(str(e))

    try:
        sns = boto3.client("sns")
        em_response = sns.publish(
            TopicArn=sns_arn,
            Message=f'''
            {err_msg}.
            ''',
            Subject="[LAMBDA]"
        )
        print(em_response)
    except Exception as e:
        print(str(e))

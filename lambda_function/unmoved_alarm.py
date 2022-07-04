import os
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from slack_sdk.webhook import WebhookClient


def lambda_handler(event, context):
    global timestamps, now
    bucket_name = os.environ["BUCKET_NAME"]
    webhook = os.environ["WEBHOOK_URL"]

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
                x_mins = int((now - x.last_modified).total_seconds() / 60.0)
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
        obj_dir = "raiz"

    webhook = WebhookClient(wh)
    if webhook is not None:
        try:
            response = webhook.send(
                text=f'''
                [LAMBDA] Atenção: O objeto {obj_name} está há {obj_mins} minutos no diretório {obj_dir} do bucket {obj_bn}.
                '''
            )
            print(response)
        except Exception as e:
            print(str(e))


def send_error(wh, err_msg):
    headers = {"Content-Type": "application/json"}
    data = {"text": "Lambda webhook error"}

    webhook = WebhookClient(wh)
    if webhook is not None:
        try:
            response = webhook.send(text=err_msg)
            print(response)
        except Exception as e:
            print(str(e))

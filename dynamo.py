from functools import lru_cache
from boto3 import resource
from botocore.config import Config
from boto3.dynamodb.conditions import Key


@lru_cache()
def get_dynamo_resource(region):
    account_config = Config(
        region_name=region,
        retries={
            'max_attempts': 5,
            'mode': 'standard'
        }
    )
    return resource('dynamodb', config=account_config)


def get_alert(dynamo_db_resource, alert_name):
    table = dynamo_db_resource.Table('GrafanaWebhook')
    response = table.get_item(
        Key={
            'AlertName': alert_name
        }
    )
    return response.get('Item')

from os import getenv
from sqs import send_message
from flask import Flask, request, Response
from dynamo import get_dynamo_resource, get_alert
import logging

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger()


@app.route('/notify/<alert_name>', methods=['POST'])
def notify(alert_name):
    log.info(f"{alert_name} - starting process")
    log.info(f"{alert_name} - get dynamodb information")
    dynamo_resource = get_dynamo_resource(getenv("AWS_DEFAULT_REGION"))
    alert = get_alert(dynamo_resource, alert_name)
    log.info(f"{alert_name} - sending message to queue {alert.get('QueueName')}")
    send_message(request.get_json(), alert)
    return Response(status=201)


if __name__ == '__main__':
    app.run()

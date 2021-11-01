from os import getenv
from sqs import send_message
from flask import Flask, request, Response
from dynamo import get_dynamo_resource, get_alert
app = Flask(__name__)


@app.route('/notify/<alert_name>', methods=['POST'])
def notify(alert_name):
    dynamo_resource = get_dynamo_resource(getenv("AWS_DEFAULT_REGION"))
    alert = get_alert(dynamo_resource, alert_name)
    send_message(request.get_json(), alert)
    return Response(status=201)


if __name__ == '__main__':
    app.run()

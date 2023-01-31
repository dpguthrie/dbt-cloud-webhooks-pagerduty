# stdlib
import hashlib
import hmac
import os
from typing import Dict

# third party
from dbtc import dbtCloudClient
from fastapi import FastAPI, HTTPException, Request, Response
from requests import Session


app = FastAPI(title='PagerDuty')


STATUSES = {
    'fail': 'critical',
    'error': 'critical',
}
RESOURCES = ['models', 'tests', 'seeds', 'snapshots']
EVENTS_URL = 'https://events.pagerduty.com/v2/enqueue'


def build_payload(response: Dict, resource: Dict) -> Dict:
    if resource['resourceType'] == 'model':
        summary = resource['error']
    else:
        summary = f'Test failure - {resource["name"]}'
    return {
        'routing_key': os.environ['PD_ROUTING_KEY'],
        'event_action': 'trigger',
        'dedup_key': f'Run ID {resource["runId"]}',
        'payload': {
            'timestamp': response['timestamp'],
            'severity': STATUSES[resource['status']],
            'source': 'https://cloud.getdbt.com',
            'summary': summary
        },
    }


def verify_signature(request_body: bytes, auth_header: str):
    app_secret = os.environ['DBT_CLOUD_AUTH_TOKEN'].encode('utf-8')
    signature = hmac.new(app_secret, request_body, hashlib.sha256).hexdigest()
    return signature == auth_header


@app.post('/', status_code=204)
async def pagerduty_webhook(request: Request):
    request_body = await request.body()
    auth_header = request.headers.get('authorization', None)
    if not verify_signature(request_body, auth_header):
        raise HTTPException(status_code=403, detail='Message not authenticated')
    
    response = await request.json()
    webhook_data = response['data']
    if webhook_data.get('runStatus', None) == 'Errored':
        client = dbtCloudClient()
        run_id = int(webhook_data['runId'])
        job_id = int(webhook_data['jobId'])
        session = Session()
        session.headers = {'Content-Type': 'application/json'}
        for resource in RESOURCES:
            method = f'get_{resource}'
            data = getattr(client.metadata, method)(job_id, run_id=run_id)['data']
            try:
                resource_list = data[resource]
            except TypeError:
                
                # No actual data was returned
                pass
            else:
                for item in resource_list:
                    if item['status'] in STATUSES.keys():
                        payload = build_payload(response, item)
                        session.post(EVENTS_URL, json=payload)

    return
    
    
if __name__ == '__main__':
    app.run()

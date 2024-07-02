# Lambda function to check if the bucket with the name exists
import boto3
import requests

# Use the default credentials and config for the session.
# Get this from "C:\Users\user_name\.aws\config" and "C:\Users\user_name\.aws\credentials"
_external_account_no = 'XXXXXXXXXXXX'
_external_account_role_name = 'XXXXXXXXXXXXXXXX'
_external_account_role_arn = 'arn:aws:iam::'+_external_account_no+':role/'+_external_account_role_name
_base_region_name = 'XX-XXXXX-X'
_base_profile_name = 'XXXXXXXXX'
_account_session = boto3.Session(profile_name=_base_profile_name,region_name = _base_region_name)

# Request parameters
_api_host_id = "xxxxxxx.execute-api.af-south-1.amazonaws.com"
_endpoint = "/xxxx"
_signed_headers = 'host'
_method = 'PUT'
_service = 'execute-api'
_server_url = "https://xxxx"
_algorithm = 'AWS4-HMAC-SHA256'
_credential_scope = ""
_request_body = '{"field": "1"}'

# ---- assume role ------
stsclient = _account_session.client('sts')
response = stsclient.assume_role(
    ExternalId=_external_account_no,
    RoleArn=_external_account_role_arn,
    RoleSessionName='_AssumeRoleSession',
)
_access_key = response["Credentials"]['AccessKeyId']
_secret_access_key = response["Credentials"]['SecretAccessKey']
_session_token = response["Credentials"]['SessionToken']

import datetime
# Create a datetime object for signing
t = datetime.datetime.utcnow()
_amzdate = t.strftime('%Y%m%dT%H%M%SZ')
_datestamp = t.strftime('%Y%m%d')

import hashlib
# Create the canonical request
canonical_headers = 'host:' + _api_host_id + '\n'
payload_hash = hashlib.sha256(_request_body.encode('utf-8')).hexdigest()
_canonical_request = (_method + '\n' + _endpoint + '\n' + '' + '\n' + canonical_headers + '\n' + _signed_headers + '\n' + payload_hash)

import hmac
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey():
    kDate = sign(("AWS4" + _secret_access_key).encode("utf-8"), _datestamp)
    kRegion = sign(kDate, _base_region_name)
    kService = sign(kRegion, _service)
    kSigning = sign(kService, "aws4_request")
    return kSigning

_credential_scope = _datestamp + '/' + _base_region_name + '/' + _service + '/aws4_request'
string_to_sign = (_algorithm + '\n' +  _amzdate + '\n' +  _credential_scope + '\n' + hashlib.sha256(_canonical_request.encode('utf-8')).hexdigest())


# Sign the string
signing_key = getSignatureKey()
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

# Add signing information to the request
authorization_header = (_algorithm + ' ' + 'Credential=' + _access_key + '/' + _credential_scope + ', ' + 'SignedHeaders=' + _signed_headers + ', ' + 'Signature=' + signature)

# Make the request
headers = {'Host': _api_host_id,
           'x-amz-date': _amzdate,
           'x-amz-security-token': _session_token,
           'Authorization': authorization_header}

request_url = '' + _server_url + _endpoint

print(request_url)
print(headers)

response = requests.get(request_url, headers=headers, timeout=5, verify=False, allow_redirects=True, data= _request_body)

print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)
# print(response.text)
print(response.json())
# response.raise_for_status()


# print(response.text)
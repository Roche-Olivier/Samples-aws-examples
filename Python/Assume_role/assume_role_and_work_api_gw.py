# Lambda function to check if the bucket with the name exists
import json
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
_http_method = "XXX"
_canonical_uri = '/xxxxx'
_api_host_id = "xxxxxx.execute-api.xxxx.amazonaws.com"
_service = 'execute-api'
_server_url = "xxxx"
_algorithm = 'AWS4-HMAC-SHA256'
_request_body = json.dumps({"xxx": "1","xxx": "111111"})



# ---- assume role ------
stsclient = _account_session.client('sts')
response = stsclient.assume_role(
    ExternalId=_external_account_no,
    RoleArn=_external_account_role_arn,
    RoleSessionName='_AssumeRoleSession',
)
_assumed_access_key = response["Credentials"]['AccessKeyId']
_secret_access_key = response["Credentials"]['SecretAccessKey']
_session_token = response["Credentials"]['SessionToken']

import datetime
# Create a datetime object for signing
t = datetime.datetime.utcnow()
_amzdate = t.strftime('%Y%m%dT%H%M%SZ')
_datestamp = t.strftime('%Y%m%d')

# https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html
import hashlib
import hmac
def hashed_value(val):
    return hashlib.sha256(val.encode('utf-8')).hexdigest()
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
def sign_hex(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).hexdigest()
def getSignatureKey():
    kDate = sign(("AWS4" + _secret_access_key).encode("utf-8"), _datestamp)
    kRegion = sign(kDate, _base_region_name)
    kService = sign(kRegion, _service)
    kSigning = sign(kService, "aws4_request")
    return kSigning

# Canonical Request
HTTPMethod = _http_method+ '\n'
CanonicalURI = _canonical_uri+ '\n'
CanonicalQueryString = ''+ '\n'
CanonicalHeaders = 'Host:'+_api_host_id+"\n"
SignedHeaders = 'Host'+"\n"
HashedPayload = hashed_value(_request_body)
_canonical_request = (HTTPMethod + CanonicalURI + CanonicalQueryString + CanonicalHeaders + SignedHeaders + HashedPayload)

# String To sign
Algorithm = _algorithm + '\n'
TimeStamp = _amzdate + '\n'
Scope = _datestamp + '/' + _base_region_name + '/' + _service + '/aws4_request'+ '\n'
HexCanonicalRequest = hashed_value(_canonical_request)
_string_to_sign = (Algorithm +  TimeStamp +  Scope + HexCanonicalRequest)

# Signature
signing_key = getSignatureKey()
signature = sign_hex(signing_key, _string_to_sign)

# Add signing information to the request
auth_header_part1 = ''+_algorithm + ' Credential=' + _assumed_access_key+ '/'+_datestamp+ '/'+_base_region_name+ '/'+_service+ '/aws4_request, '
auth_header_part2 = 'SignedHeaders=Host, '
auth_header_part3 = 'Signature='+signature
authorization_header = (auth_header_part1 + auth_header_part2 + auth_header_part3)
print(authorization_header)
# Make the request
headers = {'Host': _api_host_id,
           'x-amz-date': _amzdate,
           'x-amz-security-token': _session_token,
           'Authorization': authorization_header}

request_url = 'https://' + _server_url + _canonical_uri

print(request_url)
print(headers)

response = requests.put(request_url, headers=headers, timeout=5, verify=False, allow_redirects=True, json=_request_body)

print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)
# print(response.text)
print(response.json())
# response.raise_for_status()


# print(response.text)
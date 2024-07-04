import requests
import datetime
import hashlib
import hmac
import boto3
# https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html

# Request parameters
_region = 'xxxxx'
_service = 'execute-api'
_http_method = "xxxxx"
_canonical_uri = '/xxxxx/'
_api_id = 'xxxxx'
_api_host_id = _api_id+'.'+_service+'.'+_region+'.amazonaws.com'
_server_url = "xxxxx"
_protocol = 'https://'
_algorithm = 'AWS4-HMAC-SHA256'
_request_body = '{"field1": "xxxxx","field2": "xxxxx"}'

# user parameters
_external_account_no = 'xxxxx'
_external_account_role_name = 'xxxxx'
_external_account_role_arn = 'arn:aws:iam::'+_external_account_no+':role/'+_external_account_role_name
_caller_profile_name = 'xxxxx'

_account_session = boto3.Session(profile_name=_caller_profile_name,region_name = _region)

# ---- assume role ------
stsclient = _account_session.client('sts')
response = stsclient.assume_role(
    ExternalId=_external_account_no,
    RoleArn=_external_account_role_arn,
    RoleSessionName='_AssumeRoleSession',
)
_assumed_access_key = response["Credentials"]['AccessKeyId']
_assumed_secret_access_key = response["Credentials"]['SecretAccessKey']
_assumed_session_token = response["Credentials"]['SessionToken']

# Create a datetime object for signing
t = datetime.datetime.utcnow()
_amzdate = t.strftime('%Y%m%dT%H%M%SZ')
_datestamp = t.strftime('%Y%m%d')

def hashed_value(val):
    return hashlib.sha256(val.encode('utf-8')).hexdigest()
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
def sign_hex(key, msg):
    return hmac.new(key, (msg).encode("utf-8"), hashlib.sha256).hexdigest()
def getSignatureKey():
    kDate = sign(("AWS4" + _assumed_secret_access_key).encode("utf-8"), _datestamp)
    kRegion = sign(kDate, _region)
    kService = sign(kRegion, _service)
    kSigning = sign(kService, "aws4_request")
    return kSigning

# Canonical Request
HTTPMethod = _http_method+ '\n'
CanonicalURI = _canonical_uri+ '\n'
CanonicalQueryString = ''+ '\n'
CanonicalHeaders = 'host:'+_api_host_id+'\n'+'\n' # There is 2 newlines here, the one delimits the end of the header, and the other the end of the field
SignedHeaders = 'host'+'\n'
HashedPayload = hashed_value(_request_body)
_canonical_request = (HTTPMethod + CanonicalURI + CanonicalQueryString + CanonicalHeaders + SignedHeaders + HashedPayload)

# String To sign
Algorithm = _algorithm + '\n'
TimeStamp = _amzdate + '\n'
Scope = _datestamp + '/' + _region + '/' + _service + '/aws4_request'+ '\n'
HexCanonicalRequest = hashed_value(_canonical_request)
_string_to_sign = (Algorithm +  TimeStamp +  Scope + HexCanonicalRequest)

# Signature
signing_key = getSignatureKey()
signature = sign_hex(signing_key,_string_to_sign )

# Add signing information to the request
auth_header_part1 = ''+_algorithm + ' Credential=' + _assumed_access_key+ '/'+_datestamp+ '/'+_region+ '/'+_service+ '/aws4_request, '
auth_header_part2 = 'SignedHeaders=host, '
auth_header_part3 = 'Signature='+signature
authorization_header = (auth_header_part1 + auth_header_part2 + auth_header_part3)

# Make the request
headers = {'host': _api_host_id,
           'x-amz-date': _amzdate,
           'x-amz-security-token': _assumed_session_token,
           'authorization': authorization_header}

request_url = _protocol + _server_url + _canonical_uri
response = requests.put(request_url, headers=headers, timeout=5, verify=False, allow_redirects=True, data=_request_body)


if response.status_code == 200 :
    if response.json() is None:
        print(response.status_code)
        print("No Object received back.")    
    else:
        print(response.status_code)
        print(response.json())    
else:
    if response.json() is None:
        if response.text is None:
            print("No Object received back.")    
        else:
            print(response.status_code)   
            print(response.text)    
    else:
        print(response.status_code)   
        print(response.json())   

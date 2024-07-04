# Use the current AWS env.
# Assume a foreign role.
# Create a new session with the new role.

import boto3

# ---- assume role ------
_external_account_no = 'XXXXXXXXXXXX'
_external_account_role_name = 'XXXXXXXXXXXXXXXX'
_external_account_role_arn = 'arn:aws:iam::'+_external_account_no+':role/'+_external_account_role_name
_base_region_name = 'XX-XXXXX-X'
_base_profile_name = 'XXXXXXXXX'

_account_session = boto3.Session(profile_name=_base_profile_name,region_name = _base_region_name)
 
def assume_company_role():
    stsclient = _account_session.client('sts')
    response = stsclient.assume_role(
        ExternalId=_external_account_no,
        RoleArn=_external_account_role_arn,
        RoleSessionName='_AssumeRoleSession',
    )
    return response["Credentials"]
    
def new_company_session(temp_credentials):
    # Create an S3 resource that can access the account with the temporary credentials.
    new_session = boto3.Session(
        aws_access_key_id=temp_credentials['AccessKeyId'],
        aws_secret_access_key=temp_credentials['SecretAccessKey'],
        aws_session_token=temp_credentials['SessionToken'],
        region_name = _base_region_name
    )
    return new_session

temp_credentials = assume_company_role()
new_session = new_company_session(temp_credentials)

# You now have a session object that you can use to access the other aws services
# as the example below : 
# external_s3 = new_session.client('s3')
# ------------------------- End of example code execution -------------------------- 
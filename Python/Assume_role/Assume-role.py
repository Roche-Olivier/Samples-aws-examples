# Use the current AWS env.
# Assume a foreign role.

import boto3

# ---- assume role ------
_external_account_no = 'XXXXXXXXXXXX'
_external_account_role_name = 'XXXXXXXXXXXXXXXX'
_external_account_role_arn = 'arn:aws:iam::'+_external_account_no+':role/'+_external_account_role_name
_base_region_name = 'XX-XXXXX-X'
_base_profile_name = 'XXXXXXXXX'

_account_session = boto3.Session(profile_name=_base_profile_name,region_name = _base_region_name)
 
# This function does the session STS connection to assume the role
def assume_company_role():
    stsclient = _account_session.client('sts')
    response = stsclient.assume_role(
        ExternalId=_external_account_no,
        RoleArn=_external_account_role_arn,
        RoleSessionName='_AssumeRoleSession',
    )
    return response["Credentials"]
   
temp_credentials = assume_company_role() 

print(temp_credentials['AccessKeyId'])
print(temp_credentials['SecretAccessKey'])
print(temp_credentials['SessionToken'])
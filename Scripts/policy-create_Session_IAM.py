# Use the current AWS env.
# Assume a foreign role.
# Create a new session with the new role.
# Create a iam instance on the session 
# Perform operations on IAM
# Print the results

import boto3
import json
# ---- assume role ------
_external_account_no = 'XXXXXXXXXXXX'
_external_account_role_name = 'XXXXXXXXXXXXXXXX'
_external_account_role_arn = 'arn:aws:iam::'+_external_account_no+':role/'+_external_account_role_name
_base_region_name = 'XX-XXXXX-X'
_base_profile_name = 'XXXXXXXXX'

_account_session = boto3.Session(profile_name=_base_profile_name,region_name = _base_region_name)

# Assumes the company role with the external account-id and external role name.
def assume_company_role():
    stsclient = _account_session.client('sts')
    response = stsclient.assume_role(
        ExternalId=_external_account_no,
        RoleArn=_external_account_role_arn,
        RoleSessionName='_AssumeRoleSession',
    )
    return response["Credentials"]
    
# Create an session that can access the account with the external credentials.
def new_company_session(temp_credentials):
    new_session = boto3.Session(
        aws_access_key_id=temp_credentials['AccessKeyId'],
        aws_secret_access_key=temp_credentials['SecretAccessKey'],
        aws_session_token=temp_credentials['SessionToken'],
        region_name = _base_region_name
    )
    return new_session

# Run the application
temp_credentials = assume_company_role()
new_session = new_company_session(temp_credentials)

# Create IAM client on the session of the external company
iam = new_session.client('iam')

# Create a policy with json formatting in the policy structure.
my_managed_policy = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "RESOURCE_ARN"
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": "RESOURCE_ARN"
        }
    ]
})

response = iam.create_policy(
  PolicyName = 'example-temp-policy',
  PolicyDocument = my_managed_policy
)
print(response) 



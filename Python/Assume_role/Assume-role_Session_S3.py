# Use the current AWS env.
# Assume a foreign role.
# Create a new session with the new role.
# Create a s3 instance on the session 
# Perform operations on S3
# Print the results

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
external_s3 = new_session.client('s3')
external_response = external_s3.list_buckets()
for bucket in external_response['Buckets']:
    print(bucket['Name'] ) 
# ------------------------- End of example code execution -------------------------- 
        
# -------------------------------------- More --------------------------------------        
# Other examples of s3 methods
# You can do a create a s3 session object for the assumed role.
def get_company_s3_client(new_session):
    external_s3 = new_session.client('s3')
    return external_s3

# Then use that variable you created as input parm into the methods below
# ------------------------------------ Examples ------------------------------------  
def list_bucket_object(s3):
    external_response = s3.list_buckets()
    for bucket in external_response['Buckets']:
        print(bucket['Name'] ) 
    
def create_bucket(s3,bucket_name):
    s3.create_bucket(Bucket=bucket_name)

def setup_bucket_versioning(s3,bucket_name,enabled):
    if enabled == True:
        s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
    else:
        s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})

def create_s3_object_from_file(s3,bucket_name):
    s3.upload_file('test.txt', bucket_name, 'test.txt')

def create_s3_object(s3,bucket_name, filename, inner_text):
    s3.put_object(Bucket= bucket_name, Key=filename, Body=inner_text)

def delete_s3_object(s3,bucket_name, key):
    s3.delete_object(Bucket=bucket_name,Key=key)

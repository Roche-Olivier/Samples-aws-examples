# Lambda function to check if the bucket with the name exists
import boto3

# Use the default credentials and config for the session.
# Get this from "C:\Users\user_name\.aws\config" and "C:\Users\user_name\.aws\credentials"
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
        region_name = 'af-south-1'
    )
    return new_session

def get_company_s3_client(new_session):
    external_s3 = new_session.client('s3')
    return external_s3
    
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

temp_credentials = assume_company_role()
new_session = new_company_session(temp_credentials)
company_s3_client = get_company_s3_client(new_session)
list_bucket_object(company_s3_client)

# Lambda function to check if the bucket with the name test-my-bucket123 exists
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == 'XXXXXXXXXXXXXXXX':
            
            # delete an object from XXXXXXXXXXXXXXXX
            s3.delete_object(Bucket='XXXXXXXXXXXXXXXX',Key='test.txt')
            
            # add versioning to the created bucket
            s3.put_bucket_versioning(Bucket='XXXXXXXXXXXXXXXX', VersioningConfiguration={'Status': 'Enabled'})
            
            return True
        else:
            # create test-my-bucket123 bucket
            s3.create_bucket(Bucket='XXXXXXXXXXXXXXXX')
            
            # add versioning to the created bucket
            s3.put_bucket_versioning(Bucket='XXXXXXXXXXXXXXXX', VersioningConfiguration={'Status': 'Enabled'})
            
            
            #upload test file to the bucket
            s3.upload_file('test.txt', 'XXXXXXXXXXXXXXXX', 'test.txt')
            
            # Create a new object with the name 'test.txt' in the 'test-my-bucket123' bucket
            s3.put_object(Bucket='XXXXXXXXXXXXXXXX', Key='new_test.txt', Body='This is a test file.')
            
    return False
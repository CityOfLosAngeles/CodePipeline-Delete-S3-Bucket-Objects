import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
codePipelineClient = boto3.client('codepipeline')

# Python 3.7

# THIS SCRIPT SHOULD NOT BE USED WITH VERSIONED BUCKETS
# 1. It won't work
# 2. It's a bad use case for versioned buckets

def lambda_handler(event, context):
    
    # Get CodePipeline jobID to pass into 
    # put_job_success_result() or put_job_failure_result()
    # WITHOUT THIS CODEPIPELINE WILL TIME OUT
    job_id = event['CodePipeline.job']['id']
    
    # Get name of bucket through user parameter defined
    # in CodePipeline step
    bucketName = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']
    
    try:
        # Get Bucket as Object using boto3 s3 client
        targetBucket = s3.Bucket(bucketName)
    
        # Get iterator of ALL OBJECTs and run their delete() function
        targetBucket.objects.all().delete()
        
    except ClientError as err:
        # Should basically NEVER reach here.
        # If it does, READ LOGS and CHECK IAM POLICY
        print("Error: %s" % err)
        
        # Return a JobFailureResult to CodePipeline
        return codePipelineClient.put_job_failure_result(
            jobId=job_id,
            failureDetails={'type': 'JobFailed', 'message': 'Failed to delete all objects in bucket ' + bucketName + '\n' }
        )
    
    # Return a JobSuccessResult to CodePipeline
    # without this, CodePipeline hangs then times out and fails after 1 hr
    return codePipelineClient.put_job_success_result(jobId=job_id)

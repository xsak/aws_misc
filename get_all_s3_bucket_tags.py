import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
s3_re = boto3.resource('s3')

for bucket in s3_re.buckets.all():
    s3_bucket = bucket
    s3_bucket_name = s3_bucket.name
    bucket_tagging = s3_re.BucketTagging(s3_bucket_name)
    try:
        response = s3.get_bucket_tagging(Bucket=s3_bucket_name)
        print(f"Bucket: {bucket.name}\nTags:")
        # print(response)
        for tag1 in response['TagSet']:
            print(f"  - {tag1['Key']} : {tag1['Value']}")
    except ClientError:
        print (f"{bucket.name} - does not have tags")
    print("______")

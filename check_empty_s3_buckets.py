import boto3
s3 = boto3.client('s3')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for bckt in s3.list_buckets()['Buckets']:
    try:
        print(f"DEBUG: Bucket: {bckt['Name']} -- length: {len(s3.list_objects(Bucket=bckt['Name'])['Contents'])}")
    except Exception as e:
        print(f"{bcolors.WARNING}Bucket {bckt['Name']}{bcolors.ENDC} seems empty")

import boto3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_all_aws_regions() -> list:
    aws = boto3.client('ec2','eu-central-1')
    regions = aws.describe_regions()
    return [u['RegionName'] for u in regions['Regions']]


def get_regional_rds_list(aws_client, region):
    rds_list = aws_client.describe_db_instances()['DBInstances']
    return [u['DBInstanceIdentifier'] for u in rds_list if 'DBInstanceIdentifier' in u]


def print_regional_rds_tags(aws_client, db_arn: str):
    print('DB instance arn: {}'.format(db_arn))
    print(get_regional_rds_tags(aws_client,db_arn))


def get_regional_rds_tags(aws_client, db_arn: str):
    return aws_client.list_tags_for_resource(ResourceName=db_arn)['TagList']


def check_for_needed_tags(tag_list: list):
    reference_tag_keys = ["name", "owner", "unit", "email", "project"]
    resource_tags = [u['Key'].lower() for u in tag_list]
    print(f"Existing tags:  {tag_list}")
    if all(k in resource_tags for k in reference_tag_keys):
        print(f" * {bcolors.OKGREEN}RESULT{bcolors.ENDC}: all needed tags are present.")
    else:
        print(f" * {bcolors.FAIL}RESULT{bcolors.ENDC}: some tags are missing!!!")

def check_rds_tags():
    db_instance_list = []
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    for region in get_all_aws_regions():
        print(f"_________________{region}_________________")
        awsrds = boto3.client('rds', region)
        regional_rds_list = get_regional_rds_list(awsrds, region)
        for i in regional_rds_list:
            if i: # only if list is not empty
                db_instance_list.append(i)
                db_arn='arn:aws:rds:' + region + ':' + account_id + ':db:' + i
                rds_tags = get_regional_rds_tags(awsrds,db_arn)
                print(" *** RDS: {}".format(db_arn))
                check_for_needed_tags(rds_tags)
                print("__")


if __name__ == "__main__":
    check_rds_tags()

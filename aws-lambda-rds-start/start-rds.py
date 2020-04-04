import boto3
import botocore
import yaml
import datetime
from pprint import pprint


def get_rds_cluster_status(rds_db_cluster_object, rds_db_cluster_name):
    """
    Returns the status of the RDS as string
    """
    return \
        rds_db_cluster_object.describe_db_clusters(DBClusterIdentifier=rds_db_cluster_name)['DBClusters'][0]['Status']


def get_rds_config_from_s3(config_s3_bucket,config_s3_file) -> dict:
    """
    Returns the config yaml from S3 as a dict
    
    parameters:
      - config_s3_bucket : S3 bucket of config file
      - config_s3_key : S3 key of config file

    """
    aws_s3 = boto3.client('s3')
    rds_config = {}
    aws_s3_response = {}
    try:
        aws_s3_response = aws_s3.get_object(
            Bucket=config_s3_bucket,
            Key=config_s3_file )
    except Exception as err:
        print('Error: Problem occurred during downloading configuration file.')
        print(err)
    try:
        rds_config = yaml.safe_load(aws_s3_response['Body'])
    except yaml.YAMLError as yerr:
        print('Error: Problem loading yaml data from S3')
        raise yerr
    return rds_config


def time_in_range(start, end, x):
    """
    Return true if x is in the range [start, end]
    https://stackoverflow.com/questions/10747974/how-to-check-if-the-current-time-is-in-range-in-python
    """
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def weekday_or_weekend():
    if datetime.datetime.today().weekday() < 5:
        return 'weekdays'
    else:
        return 'weekends'

def is_it_weekend():
    if datetime.datetime.today().weekday() < 5:
        return False
    else:
        return True

def start_rds():
    region = 'eu-central-1'
    db_cluster_name = 'test-db'
    config_bucket = 'mybucket.temp'
    config_key = 'test.yml'
    
    rds_config = get_rds_config_from_s3(config_bucket, config_key)
    config_timerange = \
        str(rds_config[db_cluster_name][weekday_or_weekend()])
    ( config_start_time, config_stop_time ) = config_timerange.strip().split('-')
    rds_start_time = datetime.datetime.strptime(config_start_time, "%H:%M")
    rds_stop_time = datetime.datetime.strptime(config_stop_time, "%H:%M")
    print(f"DEBUG: config_timerange: {config_timerange} - rds_start_time: {rds_start_time} - rds_stop_time: {rds_stop_time}")
    print(f"DEBUG: config_start_time: {config_start_time} - config_stop_time: {config_stop_time}")

    if time_in_range(rds_start_time, rds_stop_time, datetime.datetime.now()):
        print('DEBUG: in timerange!')

    aws_rds = boto3.client('rds', region)
    status = get_rds_cluster_status(aws_rds, db_cluster_name)
    print(f"DB: {db_cluster_name} - status: {status}")
    if status == 'stopped':
        print(f"Trying to start db cluster: {db_cluster_name}")
        response = aws_rds.start_db_cluster(DBClusterIdentifier=db_cluster_name)
        pprint(response)
    else:
        print("DB cannot be started as it is not in stopped state.")


if __name__ == "__main__":
    start_rds()

import boto3
from pprint import pprint


def stop_rds():
    region = 'eu-central-1'
    db_cluster_name = 'test-db'

    aws_rds = boto3.client('rds', region)
    status = aws_rds.describe_db_clusters(DBClusterIdentifier=db_cluster_name)['DBClusters'][0]['Status']
    print(f"DB: {db_cluster_name} - status: {status}")
    if status == 'available':
        print(f"Trying to stop db cluster: {db_cluster_name}")
        response = aws_rds.stop_db_cluster(DBClusterIdentifier=db_cluster_name)
        pprint(response)
    else:
        print("DB cannot be stopped as it is not in available state.")


if __name__ == "__main__":
    stop_rds()

import boto3


def get_all_ebs_volumes():
    client = boto3.client('ec2', region_name='eu-central-1')

    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    for region in ec2_regions:
        print(f"DEBUG: Processing region: {region}")
        conn = boto3.resource('ec2', region_name=region)
        all_volumes = conn.volumes.all()
        for volume in all_volumes:
            # print(f"DEBUG: Processing Volume: {volume}")
            print(f" * Vol ID: {volume.id}, Vol State: {volume.state}, Vol Type: {volume.volume_type}, Vol size: {volume.size}, Region: {region},")
            for attachm in volume.attachments:
                print(f"    - Vol attached Instance: {attachm['InstanceId']}, Region: {region}")


if __name__ == "__main__":
    get_all_ebs_volumes()

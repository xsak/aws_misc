import boto3


def get_all_ec2_instances():
    client = boto3.client('ec2', region_name='eu-central-1')
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2_regions:
        conn = boto3.resource('ec2', region_name=region)
        instances = conn.instances.filter()
        for instance in instances:
            # if instance.state["Name"] == "running":
            #     print (instance.id, instance.instance_type, region)
            print(f"Instance ID: {instance.id}, Instance Type: {instance.instance_type}, Instance Platform: {instance.platform}, Region: {region}, Instance State: {instance.state}")
            print(instance.tags)
            print("____")


if __name__ == "__main__":
    get_all_ec2_instances()

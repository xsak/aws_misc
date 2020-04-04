import boto3


def get_name_tag(tag_list):
    if tag_list is None:
        return "-"
    else:
        for u in tag_list:
            if u.get('Key', '').lower() == 'name':
                return u.get('Value', '-')
        return "-"

def get_available_volumes():
    client = boto3.client('ec2', region_name='eu-central-1')

    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

    for region in ec2_regions:
        print(f"DEBUG: Processing region: {region}")
        conn = boto3.resource('ec2', region_name=region)
        all_volumes = conn.volumes.all()
        for volume in all_volumes:
            if volume.state != 'in-use':
                name_tag = get_name_tag(volume.tags)
                print(f" * Vol ID: {volume.id}, Vol State: {volume.state}, Vol Type: {volume.volume_type}, Vol size: {volume.size}, Region: {region}, Name: {name_tag}")


if  __name__ == "__main__":
    get_available_volumes()

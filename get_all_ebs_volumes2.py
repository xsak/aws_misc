import boto3


def get_name_tag(tag_list):
    if tag_list is None:
        return ""
    else:
        for u in tag_list:
            if u.get('Key', '').lower() == 'name':
                return u.get('Value', '')
        return ""


def get_owner_tag(tag_list):
    if tag_list is None:
        return ""
    else:
        for u in tag_list:
            if u.get('Key', '').lower() == 'owner':
                return u.get('Value', '')
        return ""


def get_all_ebs_volumes():
    """
    Function to get a CSV-like output of all the EBS volumes from all regions with name and owner tags.
    """
    client = boto3.client('ec2', region_name='eu-central-1')

    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    print(f"Vol ID,Vol State, Vol Type, Vol size, Region, NameTag, OwnerTag")
    for region in ec2_regions:
        #print(f"DEBUG: Processing region: {region}")
        conn = boto3.resource('ec2', region_name=region)
        all_volumes = conn.volumes.all()
        for volume in all_volumes:
            # print(f"DEBUG: Processing Volume: {volume}")
            name_tag = get_name_tag(volume.tags)
            owner_tag = get_owner_tag(volume.tags)
            print(f"{volume.id},{volume.state},{volume.volume_type},{volume.size},{region},{name_tag},{owner_tag}")


if __name__ == "__main__":
    get_all_ebs_volumes()
